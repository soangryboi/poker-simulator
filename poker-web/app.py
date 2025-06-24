from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
import sys
import os
from icm_gto_calculator import ICMGTOCalculator
import pandas as pd
from push_fold_chart_parser import PushFoldChart

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# CORS 설정 강화 (모바일 브라우저 지원)
CORS(app, 
     resources={r"/*": {"origins": "*"}},
     supports_credentials=True,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept", "Origin"])

@app.after_request
def after_request(response):
    """모든 응답에 CORS 헤더 추가"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With,Accept,Origin')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Max-Age', '86400')
    return response

# 계산기 인스턴스
icm_gto_calculator = ICMGTOCalculator()

# 서버 시작 시 push/fold 차트 로드
push_chart = PushFoldChart('../holdemresources_hu_push_int.csv')

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        return f"Error: {str(e)}", 500

@app.route('/poker_calculator')
def poker_calculator():
    return render_template('poker_calculator.html')

@app.route('/icm_gto')
def icm_gto_page():
    return render_template('icm_gto.html')

# API 엔드포인트들
@app.route('/icm_gto/calculate', methods=['POST'])
def icm_gto_calculate():
    data = request.get_json()
    hand = data.get('hand', '')
    position = data.get('position', '')
    stack_size = float(data.get('stack_size', 10))
    opponent_stack = float(data.get('opponent_stack', 10))
    pot_size = data.get('pot_size')  # None이면 자동 계산
    
    # ICM GTO 계산
    result = icm_gto_calculator.calculate_icm_ev(
        hand, position, stack_size, opponent_stack, pot_size
    )
    
    return jsonify({
        'hand': result.hand,
        'position': result.position,
        'stack_size': result.stack_size,
        'pot_size': result.pot_size,
        'ev_push': round(result.ev_push, 2),
        'ev_fold': round(result.ev_fold, 2),
        'recommendation': result.recommendation,
        'win_rate': round(result.win_rate * 100, 1),
        'icm_factor': round(result.icm_factor, 2),
        'explanation': result.explanation,
        'chart_source': result.chart_source,
        'calling_range': result.calling_range[:20]  # 처음 20개만
    })

@app.route('/icm_gto/calling_range', methods=['POST'])
def calling_range_calculate():
    data = request.get_json()
    hand = data.get('hand', '')
    position = data.get('position', '')
    stack_size = float(data.get('stack_size', 10))
    opponent_stack = float(data.get('opponent_stack', 10))
    pot_size = data.get('pot_size')  # None이면 자동 계산
    
    # 콜링 레인지 계산
    result = icm_gto_calculator.calculate_calling_range(
        hand, position, stack_size, opponent_stack, pot_size
    )
    
    return jsonify({
        'hand': result.hand,
        'position': result.position,
        'stack_size': result.stack_size,
        'pot_size': result.pot_size,
        'should_call': result.should_call,
        'ev_call': round(result.ev_call, 2),
        'ev_fold': round(result.ev_fold, 2),
        'explanation': result.explanation,
        'calling_range': result.calling_range[:20]  # 처음 20개만
    })

@app.route('/test_aks')
def test_aks():
    """AKs 계산 테스트"""
    result = icm_gto_calculator.test_aks_calculation()
    return jsonify(result)

@app.route('/aof_chart')
def aof_chart():
    hands = [
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
        "AKs", "AKo", "AQs", "AQo", "AJs", "AJo", "ATs", "ATo",
        "KQs", "KQo", "KJs", "KJo", "QJs", "QJo", "JTs", "JTo"
    ]
    stack_sizes = [5, 10, 15, 20]
    gto_call_freq = {5: 0.55, 10: 0.40, 15: 0.30, 20: 0.22}
    hand_vs_range_winrate = {
        "AA": 0.85, "KK": 0.82, "QQ": 0.80, "JJ": 0.77, "TT": 0.75, "99": 0.72, "88": 0.69, "77": 0.66,
        "66": 0.63, "55": 0.60, "44": 0.57, "33": 0.54, "22": 0.51,
        "AKs": 0.66, "AKo": 0.65, "AQs": 0.63, "AQo": 0.62, "AJs": 0.60, "AJo": 0.59, "ATs": 0.57, "ATo": 0.56,
        "KQs": 0.58, "KQo": 0.57, "KJs": 0.56, "KJo": 0.55, "QJs": 0.55, "QJo": 0.54, "JTs": 0.52, "JTo": 0.51
    }
    def calc_ev(hand, stack, call_freq, winrate):
        pot = stack * 2
        fold_freq = 1 - call_freq
        ev = fold_freq * pot + call_freq * (winrate * pot - (1 - winrate) * stack)
        return ev
    result = []
    for stack in stack_sizes:
        row = []
        for hand in hands:
            winrate = hand_vs_range_winrate.get(hand, 0.35)
            call_freq = gto_call_freq[stack]
            ev = calc_ev(hand, stack, call_freq, winrate)
            row.append(f'<span class="O">O</span>' if ev > 0 else f'<span class="X">X</span>')
        result.append(row)
    df = pd.DataFrame(result, columns=hands, index=[f"{bb}BB" for bb in stack_sizes])
    table_html = df.to_html(classes="poker-chart", border=1, escape=False)
    return render_template('aof_chart.html', table=table_html)

@app.route('/aof_matrix')
def aof_matrix():
    ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    stack_options = [1, 2, 3, 5, 10, 15, 20]
    stack = int(request.args.get('stack', 10))
    gto_call_freq = {1: 0.75, 2: 0.65, 3: 0.60, 5: 0.55, 10: 0.40, 15: 0.30, 20: 0.22}
    hand_vs_range_winrate = {
        "AA": 0.85, "KK": 0.82, "QQ": 0.80, "JJ": 0.77, "TT": 0.75, "99": 0.72, "88": 0.69, "77": 0.66,
        "66": 0.63, "55": 0.60, "44": 0.57, "33": 0.54, "22": 0.51,
        "AKs": 0.66, "AKo": 0.65, "AQs": 0.63, "AQo": 0.62, "AJs": 0.60, "AJo": 0.59, "ATs": 0.57, "ATo": 0.56,
        "KQs": 0.58, "KQo": 0.57, "KJs": 0.56, "KJo": 0.55, "QJs": 0.55, "QJo": 0.54, "JTs": 0.52, "JTo": 0.51
    }
    def calc_ev(hand, stack, call_freq, winrate):
        pot = stack * 2
        fold_freq = 1 - call_freq
        ev = fold_freq * pot + call_freq * (winrate * pot - (1 - winrate) * stack)
        return ev
    call_freq = gto_call_freq.get(stack, 0.4)
    matrix = []
    for i, r1 in enumerate(ranks):
        row = []
        for j, r2 in enumerate(ranks):
            if i < j:
                hand = r1 + r2 + 's'
            elif i > j:
                hand = r2 + r1 + 'o'
            else:
                hand = r1 + r2
            winrate = hand_vs_range_winrate.get(hand, 0.35)
            ev = calc_ev(hand, stack, call_freq, winrate)
            ev_disp = f"{ev:+.2f}"  # +1.23, -0.45
            if ev > 0.01:
                cls = 'ev-pos'
            elif ev < -0.01:
                cls = 'ev-neg'
            else:
                cls = 'ev-zero'
            row.append({'ev': ev_disp, 'cls': cls})
        matrix.append(row)
    return render_template('aof_matrix.html', matrix=matrix, ranks=ranks, stack=stack, stack_options=stack_options)

# API: 핸드/스택별 푸시 여부 반환
@app.route('/api/should_push', methods=['POST'])
def api_should_push():
    data = request.get_json()
    hand = data.get('hand', '')
    stack = int(data.get('stack', 10))
    result = push_chart.should_push(hand, stack)
    return jsonify({'push': result})

# 웹: 푸시/폴드 차트 매트릭스
@app.route('/push_fold_chart')
def push_fold_chart():
    ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    try:
        input_stack = float(request.args.get('stack', 10))
    except Exception:
        input_stack = 10
    # 가장 가까운 스택 찾기
    stack_options = sorted(push_chart.chart.keys())
    nearest_stack = min(stack_options, key=lambda x: abs(x - input_stack))
    matrix = []
    for i, r1 in enumerate(ranks):
        row = []
        for j, r2 in enumerate(ranks):
            if i < j:
                hand = r1 + r2 + 's'
            elif i > j:
                hand = r2 + r1 + 'o'
            else:
                hand = r1 + r2
            is_push = push_chart.should_push(hand, nearest_stack)
            cell = {'val': hand if is_push else '', 'cls': 'push' if is_push else 'fold'}
            row.append(cell)
        matrix.append(row)
    return render_template('push_fold_matrix.html', matrix=matrix, ranks=ranks, stack=input_stack, nearest_stack=nearest_stack)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
