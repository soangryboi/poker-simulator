from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
import sys
import os

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# CORS 설정 강화
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
    }
})

@app.after_request
def after_request(response):
    """모든 응답에 CORS 헤더 추가"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# 현재 디렉토리 확인
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Files in current directory: {os.listdir('.')}")

# exact_probability 모듈 import 시도
try:
    from exact_probability import (
        exact_river_probability, exact_turn_probability, exact_flop_probability,
        exact_partial_community_probability, exact_preflop_probability,
        exact_multiplayer_river, exact_multiplayer_turn, exact_multiplayer_partial_community,
        exact_multiplayer_preflop,
        exact_multiplayer_river_individual, exact_multiplayer_turn_individual,
        exact_multiplayer_flop_individual, exact_multiplayer_preflop_individual
    )
    logger.info("Successfully imported exact_probability module")
except ImportError as e:
    logger.error(f"Failed to import exact_probability: {e}")
    exact_probability = None

# poker 모듈 import 시도
try:
    from poker import Card
    logger.info("Successfully imported poker module")
except ImportError as e:
    logger.error(f"Failed to import poker module: {e}")
    Card = None

def parse_card(card_str):
    """카드 문자열을 Card 객체로 변환"""
    if Card is None:
        raise ImportError("poker module is not available")
    
    card_str = card_str.upper().strip()
    
    # 10 카드 처리
    if card_str.startswith('10'):
        rank = 'T'
        suit = card_str[2]
    else:
        rank = card_str[0]
        suit = card_str[1]
    
    return Card(rank, suit)

def parse_hand(hand_str):
    """핸드 문자열을 Card 객체 리스트로 변환"""
    cards = hand_str.split()
    return [parse_card(card) for card in cards]

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        return f"Error: {str(e)}", 500

@app.route('/calculator')
def calculator():
    try:
        return render_template('poker_calculator.html')
    except Exception as e:
        logger.error(f"Error in calculator route: {e}")
        return f"Error: {str(e)}", 500

@app.route('/calculate', methods=['POST', 'OPTIONS'])
def calculate_probability():
    # OPTIONS 요청 처리 (CORS preflight)
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    try:
        # 모듈 import 상태 확인
        if exact_probability is None:
            return jsonify({'error': 'exact_probability 모듈을 불러올 수 없습니다'}), 500
        
        if Card is None:
            return jsonify({'error': 'poker 모듈을 불러올 수 없습니다'}), 500
        
        import time
        
        start_time = time.time()
        
        data = request.json
        if data is None:
            return jsonify({'error': '잘못된 요청 데이터입니다'}), 400
        
        # 입력 데이터 파싱
        my_hand_str = data.get('my_hand', '')
        opponents_str = data.get('opponents', [])
        community_str = data.get('community', '')
        
        # 카드 파싱
        my_hand = parse_hand(my_hand_str)
        opponents = [parse_hand(opp) for opp in opponents_str if opp.strip()]
        community = parse_hand(community_str) if community_str.strip() else []
        
        # 중복 카드 검증
        all_cards = my_hand + community
        for opp in opponents:
            all_cards.extend(opp)
        
        if len(set(all_cards)) != len(all_cards):
            return jsonify({'error': '중복된 카드가 있습니다'}), 400
        
        # 상황에 따른 계산
        if len(community) == 5:  # 리버
            if len(opponents) == 1:
                win, tie, loss = exact_river_probability(my_hand, opponents[0], community)
                win_rates = [win / 100, (100 - win - tie) / 100]
                tie_rate = tie / 100
            else:
                win_rates, tie_rate = exact_multiplayer_river_individual(my_hand, opponents, community)
        elif len(community) == 4:  # 턴
            if len(opponents) == 1:
                win, tie, loss = exact_turn_probability(my_hand, opponents[0], community)
                win_rates = [win / 100, (100 - win - tie) / 100]
                tie_rate = tie / 100
            else:
                win_rates, tie_rate = exact_multiplayer_turn_individual(my_hand, opponents, community)
        elif len(community) == 3:  # 플랍
            if len(opponents) == 1:
                win, tie, loss = exact_flop_probability(my_hand, opponents[0], community)
                win_rates = [win / 100, (100 - win - tie) / 100]
                tie_rate = tie / 100
            else:
                win_rates, tie_rate = exact_multiplayer_flop_individual(my_hand, opponents, community)
        elif len(community) in [1, 2]:  # 부분 보드 - 허용하지 않음
            return jsonify({'error': '보드 카드는 3장(플랍), 4장(턴), 5장(리버) 또는 아예 선택하지 않아야 합니다. 1장 또는 2장만 선택할 수 없습니다.'}), 400
        else:  # 프리플랍
            if len(opponents) == 1:
                win, tie, loss = exact_preflop_probability(my_hand, opponents[0])
                win_rates = [win / 100, (100 - win - tie) / 100]
                tie_rate = tie / 100
            else:
                win_rates, tie_rate = exact_multiplayer_preflop_individual(my_hand, opponents)
        
        calculation_time = time.time() - start_time
        
        response = jsonify({
            'win_rates': win_rates,
            'tie_rate': tie_rate,
            'total_players': len(opponents) + 1,
            'community_cards': len(community),
            'calculation_time': calculation_time
        })
        
        return response
        
    except Exception as e:
        logger.error(f"Error in calculate route: {e}")
        logger.error(f"Exception type: {type(e)}")
        logger.error(f"Exception args: {e.args}")
        response = jsonify({'error': f'서버 오류: {str(e)}'})
        return response, 500

@app.route('/test')
def test():
    return jsonify({'status': 'ok', 'message': 'Server is running'})

@app.route('/diagnose')
def diagnose():
    """서버 상태와 모듈 상태를 진단"""
    import os
    
    diagnosis = {
        'server_status': 'running',
        'current_directory': os.getcwd(),
        'files_in_directory': os.listdir('.'),
        'exact_probability_imported': exact_probability is not None,
        'poker_imported': Card is not None,
        'python_version': sys.version
    }
    
    return jsonify(diagnosis)

if __name__ == '__main__':
    app.run(debug=True)
