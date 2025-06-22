from flask import Flask, request, jsonify
from flask_cors import CORS
from exact_probability import (
    exact_river_probability, exact_turn_probability, exact_flop_probability,
    exact_partial_community_probability, exact_preflop_probability,
    exact_multiplayer_river, exact_multiplayer_turn, exact_multiplayer_partial_community,
    exact_multiplayer_preflop
)
from poker import Card
import re

app = Flask(__name__)
CORS(app)

def parse_card(card_str):
    """카드 문자열을 Card 객체로 변환"""
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

@app.route('/calculate', methods=['POST'])
def calculate_probability():
    try:
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
            else:
                win, tie, loss = exact_multiplayer_river(my_hand, opponents, community)
        elif len(community) == 4:  # 턴
            if len(opponents) == 1:
                win, tie, loss = exact_turn_probability(my_hand, opponents[0], community)
            else:
                win, tie, loss = exact_multiplayer_turn(my_hand, opponents, community)
        elif len(community) == 3:  # 플랍
            if len(opponents) == 1:
                win, tie, loss = exact_flop_probability(my_hand, opponents[0], community)
            else:
                win, tie, loss = exact_multiplayer_partial_community(my_hand, opponents, community)
        elif len(community) in [1, 2]:  # 부분 보드
            if len(opponents) == 1:
                win, tie, loss = exact_partial_community_probability(my_hand, opponents[0], community)
            else:
                win, tie, loss = exact_multiplayer_partial_community(my_hand, opponents, community)
        else:  # 프리플랍
            if len(opponents) == 1:
                win, tie, loss = exact_preflop_probability(my_hand, opponents[0])
            else:
                win, tie, loss = exact_multiplayer_preflop(my_hand, opponents)
        
        return jsonify({
            'win': round(win, 2),
            'tie': round(tie, 2),
            'loss': round(loss, 2),
            'total_players': len(opponents) + 1,
            'community_cards': len(community)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000) 