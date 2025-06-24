"""
ICM GTO Calculator for Heads-Up Situations
Based on MyPokerCoaching ICM Strategy and GTO Solver Charts
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import math

@dataclass
class ICMResult:
    """ICM 계산 결과"""
    hand: str
    position: str
    stack_size: float
    pot_size: float
    ev_push: float
    ev_fold: float
    ev_call: float
    recommendation: str
    win_rate: float
    tie_rate: float
    fold_rate: float
    icm_factor: float
    explanation: str
    chart_source: str
    calling_range: List[str]

@dataclass
class CallingRangeResult:
    """콜링 레인지 계산 결과"""
    hand: str
    position: str
    stack_size: float
    pot_size: float
    should_call: bool
    ev_call: float
    ev_fold: float
    calling_range: List[str]
    explanation: str

class ICMGTOCalculator:
    """ICM GTO 계산기 - 헤즈업 전용"""
    
    def __init__(self):
        self.icm_charts = self._load_icm_charts()
        self.calling_charts = self._load_calling_charts()
        
    def _load_icm_charts(self) -> Dict:
        """MyPokerCoaching ICM 차트 로드 (헤즈업 전용)"""
        return {
            "SB_vs_BB": {
                "10BB": {
                    "push_hands": [
                        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
                        "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                        "AKo", "AQo", "AJo", "ATo", "A9o", "A8o", "A7o", "A6o", "A5o", "A4o", "A3o", "A2o",
                        "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
                        "KQo", "KJo", "KTo", "K9o", "K8o", "K7o", "K6o", "K5o", "K4o", "K3o", "K2o",
                        "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s",
                        "QJo", "QTo", "Q9o", "Q8o", "Q7o", "Q6o", "Q5o", "Q4o", "Q3o", "Q2o",
                        "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s", "J3s", "J2s",
                        "JTo", "J9o", "J8o", "J7o", "J6o", "J5o", "J4o", "J3o", "J2o",
                        "T9s", "T8s", "T7s", "T6s", "T5s", "T4s", "T3s", "T2s",
                        "T9o", "T8o", "T7o", "T6o", "T5o", "T4o", "T3o", "T2o",
                        "98s", "97s", "96s", "95s", "94s", "93s", "92s",
                        "98o", "97o", "96o", "95o", "94o", "93o", "92o",
                        "87s", "86s", "85s", "84s", "83s", "82s",
                        "87o", "86o", "85o", "84o", "83o", "82o",
                        "76s", "75s", "74s", "73s", "72s",
                        "76o", "75o", "74o", "73o",
                        "65s", "64s", "63s", "62s",
                        "65o", "64o", "63o", "62o",
                        "54s", "53s", "52s",
                        "54o", "53o", "52o",
                        "43s", "42s",
                        "43o", "42o",
                        "32s", "32o"
                    ],
                    "fold_hands": [
                        "72o", "82o", "92o", "T2o", "J2o", "Q2o", "K2o", "A2o",
                        "73o", "83o", "93o", "T3o", "J3o", "Q3o", "K3o", "A3o",
                        "74o", "84o", "94o", "T4o", "J4o", "Q4o", "K4o", "A4o",
                        "75o", "85o", "95o", "T5o", "J5o", "Q5o", "K5o", "A5o",
                        "76o", "86o", "96o", "T6o", "J6o", "Q6o", "K6o", "A6o",
                        "87o", "97o", "T7o", "J7o", "Q7o", "K7o", "A7o",
                        "98o", "T8o", "J8o", "Q8o", "K8o", "A8o",
                        "T9o", "J9o", "Q9o", "K9o", "A9o",
                        "JTo", "QTo", "KTo", "ATo",
                        "QJo", "KJo", "AJo",
                        "KQo", "AQo",
                        "AKo"
                    ]
                },
                "15BB": {
                    "push_hands": [
                        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
                        "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                        "AKo", "AQo", "AJo", "ATo", "A9o", "A8o", "A7o", "A6o", "A5o", "A4o", "A3o", "A2o",
                        "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
                        "KQo", "KJo", "KTo", "K9o", "K8o", "K7o", "K6o", "K5o", "K4o", "K3o", "K2o",
                        "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s",
                        "QJo", "QTo", "Q9o", "Q8o", "Q7o", "Q6o", "Q5o", "Q4o", "Q3o", "Q2o",
                        "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s", "J3s", "J2s",
                        "JTo", "J9o", "J8o", "J7o", "J6o", "J5o", "J4o", "J3o", "J2o",
                        "T9s", "T8s", "T7s", "T6s", "T5s", "T4s", "T3s", "T2s",
                        "T9o", "T8o", "T7o", "T6o", "T5o", "T4o", "T3o", "T2o",
                        "98s", "97s", "96s", "95s", "94s", "93s", "92s",
                        "98o", "97o", "96o", "95o", "94o", "93o", "92o",
                        "87s", "86s", "85s", "84s", "83s", "82s",
                        "87o", "86o", "85o", "84o", "83o", "82o",
                        "76s", "75s", "74s", "73s", "72s",
                        "76o", "75o", "74o", "73o",
                        "65s", "64s", "63s", "62s",
                        "65o", "64o", "63o", "62o",
                        "54s", "53s", "52s",
                        "54o", "53o", "52o",
                        "43s", "42s",
                        "43o", "42o",
                        "32s", "32o"
                    ],
                    "fold_hands": [
                        "72o", "82o", "92o", "T2o", "J2o", "Q2o", "K2o", "A2o",
                        "73o", "83o", "93o", "T3o", "J3o", "Q3o", "K3o", "A3o",
                        "74o", "84o", "94o", "T4o", "J4o", "Q4o", "K4o", "A4o",
                        "75o", "85o", "95o", "T5o", "J5o", "Q5o", "K5o", "A5o",
                        "76o", "86o", "96o", "T6o", "J6o", "Q6o", "K6o", "A6o",
                        "87o", "97o", "T7o", "J7o", "Q7o", "K7o", "A7o",
                        "98o", "T8o", "J8o", "Q8o", "K8o", "A8o",
                        "T9o", "J9o", "Q9o", "K9o", "A9o",
                        "JTo", "QTo", "KTo", "ATo",
                        "QJo", "KJo", "AJo",
                        "KQo", "AQo",
                        "AKo"
                    ]
                }
            }
        }
    
    def _load_calling_charts(self) -> Dict:
        """콜링 레인지 차트 로드 (헤즈업 전용)"""
        return {
            "BB_vs_SB": {
                "10BB": {
                    "call_hands": [
                        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
                        "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                        "AKo", "AQo", "AJo", "ATo", "A9o", "A8o", "A7o", "A6o", "A5o", "A4o", "A3o", "A2o",
                        "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
                        "KQo", "KJo", "KTo", "K9o", "K8o", "K7o", "K6o", "K5o", "K4o", "K3o", "K2o",
                        "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s",
                        "QJo", "QTo", "Q9o", "Q8o", "Q7o", "Q6o", "Q5o", "Q4o", "Q3o", "Q2o",
                        "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s", "J3s", "J2s",
                        "JTo", "J9o", "J8o", "J7o", "J6o", "J5o", "J4o", "J3o", "J2o",
                        "T9s", "T8s", "T7s", "T6s", "T5s", "T4s", "T3s", "T2s",
                        "T9o", "T8o", "T7o", "T6o", "T5o", "T4o", "T3o", "T2o",
                        "98s", "97s", "96s", "95s", "94s", "93s", "92s",
                        "98o", "97o", "96o", "95o", "94o", "93o", "92o",
                        "87s", "86s", "85s", "84s", "83s", "82s",
                        "87o", "86o", "85o", "84o", "83o", "82o",
                        "76s", "75s", "74s", "73s", "72s",
                        "76o", "75o", "74o", "73o",
                        "65s", "64s", "63s", "62s",
                        "65o", "64o", "63o", "62o",
                        "54s", "53s", "52s",
                        "54o", "53o", "52o",
                        "43s", "42s",
                        "43o", "42o",
                        "32s", "32o"
                    ],
                    "fold_hands": [
                        "72o", "82o", "92o", "T2o", "J2o", "Q2o", "K2o", "A2o",
                        "73o", "83o", "93o", "T3o", "J3o", "Q3o", "K3o", "A3o",
                        "74o", "84o", "94o", "T4o", "J4o", "Q4o", "K4o", "A4o",
                        "75o", "85o", "95o", "T5o", "J5o", "Q5o", "K5o", "A5o",
                        "76o", "86o", "96o", "T6o", "J6o", "Q6o", "K6o", "A6o",
                        "87o", "97o", "T7o", "J7o", "Q7o", "K7o", "A7o",
                        "98o", "T8o", "J8o", "Q8o", "K8o", "A8o",
                        "T9o", "J9o", "Q9o", "K9o", "A9o",
                        "JTo", "QTo", "KTo", "ATo",
                        "QJo", "KJo", "AJo",
                        "KQo", "AQo",
                        "AKo"
                    ]
                }
            }
        }
    
    def calculate_icm_ev(self, 
                        hand: str, 
                        position: str, 
                        stack_size: float, 
                        opponent_stack: float,
                        pot_size: Optional[float] = None) -> ICMResult:
        """
        ICM 기반 EV 계산 (헤즈업 전용)
        
        Args:
            hand: 핸드 (예: "AKs", "QQ")
            position: 포지션 ("SB", "BB")
            stack_size: 내 스택 사이즈 (BB 단위)
            opponent_stack: 상대 스택 사이즈 (BB 단위)
            pot_size: 팟 사이즈 (None이면 자동 계산)
        
        Returns:
            ICMResult: 계산 결과
        """
        
        # 팟 사이즈 자동 계산 (내가 올인하면 2배)
        if pot_size is None:
            pot_size = stack_size * 2
        
        # 차트에서 가장 가까운 스택 사이즈 찾기
        chart_key = self._get_chart_key(position)
        stack_key = self._get_stack_key(stack_size)
        
        # ICM 팩터 계산
        icm_factor = self._calculate_icm_factor(stack_size, opponent_stack, pot_size)
        
        # 승률 계산 (ICM 조정 없이 실제 승률 사용)
        win_rate, tie_rate = self._calculate_icm_win_rates(hand, position, stack_size, icm_factor)
        fold_rate = 1 - win_rate - tie_rate
        
        # EV 계산 (ICM 조정)
        ev_push = self._calculate_icm_push_ev(win_rate, tie_rate, stack_size, pot_size, icm_factor)
        ev_fold = -pot_size * 0.5 * icm_factor  # 폴드 시 손실 (ICM 조정)
        
        # 핵심 로직: 승률이 50% 이상이면 무조건 올인, 50% 미만이면 무조건 폴드
        if win_rate >= 0.5:
            recommendation = "PUSH"
            is_push_hand = True
        else:
            # 승률이 50% 미만이면 무조건 폴드
            recommendation = "FOLD"
            is_push_hand = False
        
        # 콜링 레인지 계산
        calling_range = self._get_calling_range(position, stack_size)
        
        # 설명 생성
        explanation = self._generate_icm_explanation(
            hand, position, stack_size, opponent_stack, win_rate, tie_rate, 
            ev_push, ev_fold, recommendation, is_push_hand, icm_factor
        )
        
        return ICMResult(
            hand=hand,
            position=position,
            stack_size=stack_size,
            pot_size=pot_size,
            ev_push=ev_push,
            ev_fold=ev_fold,
            ev_call=0,  # 콜링 EV는 별도 계산
            recommendation=recommendation,
            win_rate=win_rate,
            tie_rate=tie_rate,
            fold_rate=fold_rate,
            icm_factor=icm_factor,
            explanation=explanation,
            chart_source="MyPokerCoaching ICM",
            calling_range=calling_range
        )
    
    def calculate_calling_range(self, 
                              hand: str, 
                              position: str, 
                              stack_size: float, 
                              opponent_stack: float,
                              pot_size: Optional[float] = None) -> CallingRangeResult:
        """
        콜링 레인지 계산 (상대가 올인했을 때)
        
        Args:
            hand: 내 핸드
            position: 내 포지션
            stack_size: 내 스택
            opponent_stack: 상대 스택
            pot_size: 팟 사이즈
        
        Returns:
            CallingRangeResult: 콜링 결정
        """
        
        # 팟 사이즈 자동 계산
        if pot_size is None:
            pot_size = stack_size * 2
        
        # ICM 팩터 계산
        icm_factor = self._calculate_icm_factor(stack_size, opponent_stack, pot_size)
        
        # 승률 계산 (ICM 조정 없이 실제 승률 사용)
        win_rate, tie_rate = self._calculate_icm_win_rates(hand, position, stack_size, icm_factor)
        
        # EV 계산
        ev_call = self._calculate_call_ev(win_rate, tie_rate, stack_size, pot_size, icm_factor)
        ev_fold = -pot_size * 0.5 * icm_factor
        
        # 핵심 로직: 승률이 50% 이상이면 무조건 콜, 50% 미만이면 무조건 폴드
        if win_rate >= 0.5:
            should_call = True
        else:
            # 승률이 50% 미만이면 무조건 폴드
            should_call = False
        
        # 콜링 레인지 가져오기
        calling_range = self._get_calling_range(position, stack_size)
        
        # 설명 생성
        explanation = self._generate_calling_explanation(
            hand, position, stack_size, opponent_stack, win_rate, tie_rate,
            ev_call, ev_fold, should_call, icm_factor
        )
        
        return CallingRangeResult(
            hand=hand,
            position=position,
            stack_size=stack_size,
            pot_size=pot_size,
            should_call=should_call,
            ev_call=ev_call,
            ev_fold=ev_fold,
            calling_range=calling_range,
            explanation=explanation
        )
    
    def _calculate_icm_factor(self, stack_size: float, opponent_stack: float, pot_size: float) -> float:
        """ICM 팩터 계산"""
        total_chips = stack_size + opponent_stack
        my_equity = stack_size / total_chips
        pot_equity = pot_size / total_chips
        
        # ICM 팩터 (토너먼트 상황에서의 가치)
        icm_factor = 1.0 + (pot_equity * 0.3)  # 팟이 클수록 ICM 영향 증가
        return icm_factor
    
    def _calculate_icm_win_rates(self, hand: str, position: str, stack_size: float, icm_factor: float) -> Tuple[float, float]:
        """승률 계산 (ICM 조정 없이 실제 승률 사용)"""
        # 기본 승률 (실제 헤즈업 승률)
        base_win_rate = self._get_hand_strength(hand)
        
        # 포지션 보너스 (헤즈업 전용)
        position_bonus = {
            "SB": 0.01,  # SB는 약간의 보너스
            "BB": 0.0    # BB는 보너스 없음
        }
        
        # 실제 승률 사용 (ICM 조정 제거)
        win_rate = base_win_rate + position_bonus.get(position, 0.0)
        win_rate = max(0.1, min(0.95, win_rate))  # 10%~95% 범위
        tie_rate = 0.02
        
        return win_rate, tie_rate
    
    def _calculate_icm_push_ev(self, win_rate: float, tie_rate: float, 
                             stack_size: float, pot_size: float, icm_factor: float) -> float:
        """ICM 조정된 Push EV 계산"""
        pot_after_push = pot_size + stack_size
        ev = (win_rate * pot_after_push) + (tie_rate * pot_after_push / 2) - stack_size
        return ev * icm_factor
    
    def _calculate_call_ev(self, win_rate: float, tie_rate: float,
                          stack_size: float, pot_size: float, icm_factor: float) -> float:
        """콜 EV 계산"""
        ev = (win_rate * pot_size) + (tie_rate * pot_size / 2) - stack_size
        return ev * icm_factor
    
    def _get_hand_strength(self, hand: str) -> float:
        """내 핸드 vs 랜덤 핸드 승률만 반환 (헤즈업 기준)"""
        hand_upper = hand.upper().strip()
        if hand_upper == "AA":
            return 0.85
        elif hand_upper == "KK":
            return 0.82
        elif hand_upper == "QQ":
            return 0.80
        elif hand_upper == "JJ":
            return 0.77
        elif hand_upper == "TT":
            return 0.75
        elif hand_upper == "99":
            return 0.72
        elif hand_upper == "88":
            return 0.69
        elif hand_upper == "77":
            return 0.66
        elif hand_upper == "66":
            return 0.63
        elif hand_upper == "55":
            return 0.60
        elif hand_upper == "44":
            return 0.57
        elif hand_upper == "33":
            return 0.54
        elif hand_upper == "22":
            return 0.51
        elif hand_upper == "AKS":
            return 0.66
        elif hand_upper == "AKO":
            return 0.65
        elif hand_upper == "AQS":
            return 0.63
        elif hand_upper == "AQO":
            return 0.62
        elif hand_upper == "AJS":
            return 0.60
        elif hand_upper == "AJO":
            return 0.59
        elif hand_upper == "KQS":
            return 0.58
        elif hand_upper == "KQO":
            return 0.57
        # 기타 핸드들은 0.35로 통일
        return 0.35
    
    def _get_chart_key(self, position: str) -> str:
        """포지션을 차트 키로 변환 (헤즈업 전용)"""
        if position == "SB":
            return "SB_vs_BB"
        elif position == "BB":
            return "SB_vs_BB"  # BB에서도 같은 차트 사용
        else:
            return "SB_vs_BB"  # 기본값
    
    def _get_calling_chart_key(self, position: str) -> str:
        """콜링 차트 키 변환"""
        if position == "BB":
            return "BB_vs_SB"
        else:
            return "BB_vs_SB"
    
    def _get_stack_key(self, stack_size: float) -> str:
        """스택 사이즈를 차트 키로 변환"""
        if stack_size <= 10:
            return "10BB"
        elif stack_size <= 15:
            return "15BB"
        else:
            return "15BB"
    
    def _get_calling_range(self, position: str, stack_size: float) -> List[str]:
        """콜링 레인지 가져오기"""
        chart_key = self._get_calling_chart_key(position)
        stack_key = self._get_stack_key(stack_size)
        
        if chart_key in self.calling_charts and stack_key in self.calling_charts[chart_key]:
            return self.calling_charts[chart_key][stack_key]["call_hands"]
        return []
    
    def _calculate_default_icm_ev(self, hand: str, position: str, 
                                stack_size: float, opponent_stack: float, pot_size: float) -> ICMResult:
        """기본 ICM EV 계산"""
        icm_factor = self._calculate_icm_factor(stack_size, opponent_stack, pot_size)
        win_rate, tie_rate = self._calculate_icm_win_rates(hand, position, stack_size, icm_factor)
        
        ev_push = self._calculate_icm_push_ev(win_rate, tie_rate, stack_size, pot_size, icm_factor)
        ev_fold = -pot_size * 0.5 * icm_factor
        
        recommendation = "PUSH" if ev_push > ev_fold else "FOLD"
        
        explanation = f"차트에 없는 상황이므로 기본 ICM 계산을 사용했습니다."
        
        return ICMResult(
            hand=hand,
            position=position,
            stack_size=stack_size,
            pot_size=pot_size,
            ev_push=ev_push,
            ev_fold=ev_fold,
            ev_call=0,
            recommendation=recommendation,
            win_rate=win_rate,
            tie_rate=tie_rate,
            fold_rate=1-win_rate-tie_rate,
            icm_factor=icm_factor,
            explanation=explanation,
            chart_source="Default ICM",
            calling_range=[]
        )
    
    def _calculate_default_calling_ev(self, hand: str, position: str,
                                    stack_size: float, opponent_stack: float, pot_size: float) -> CallingRangeResult:
        """기본 콜링 EV 계산"""
        icm_factor = self._calculate_icm_factor(stack_size, opponent_stack, pot_size)
        win_rate, tie_rate = self._calculate_icm_win_rates(hand, position, stack_size, icm_factor)
        
        ev_call = self._calculate_call_ev(win_rate, tie_rate, stack_size, pot_size, icm_factor)
        ev_fold = -pot_size * 0.5 * icm_factor
        
        should_call = ev_call > ev_fold
        
        explanation = f"차트에 없는 상황이므로 기본 계산을 사용했습니다."
        
        return CallingRangeResult(
            hand=hand,
            position=position,
            stack_size=stack_size,
            pot_size=pot_size,
            should_call=should_call,
            ev_call=ev_call,
            ev_fold=ev_fold,
            calling_range=[],
            explanation=explanation
        )
    
    def _generate_icm_explanation(self, hand: str, position: str, stack_size: float,
                                opponent_stack: float, win_rate: float, tie_rate: float,
                                ev_push: float, ev_fold: float, recommendation: str,
                                is_push_hand: bool, icm_factor: float) -> str:
        """ICM 설명 생성"""
        explanation = f"{hand} 핸드, {position} 포지션, {stack_size}BB 스택에서 "
        explanation += f"승률 {win_rate:.1%}, 타이율 {tie_rate:.1%}입니다. "
        explanation += f"ICM 팩터는 {icm_factor:.2f}입니다. "
        
        if win_rate >= 0.5:
            explanation += f"승률이 50% 이상이므로 무조건 PUSH를 추천합니다. "
            explanation += f"헤즈업에서 승률이 절반 이상이면 올인이 항상 +EV입니다. "
        else:
            explanation += f"승률이 50% 미만이므로 무조건 FOLD를 추천합니다. "
            explanation += f"헤즈업에서 승률이 절반 미만이면 폴드가 더 나은 선택입니다. "
        
        explanation += f"Push EV: {ev_push:.2f}BB, Fold EV: {ev_fold:.2f}BB입니다."
        
        return explanation
    
    def _generate_calling_explanation(self, hand: str, position: str, stack_size: float,
                                    opponent_stack: float, win_rate: float, tie_rate: float,
                                    ev_call: float, ev_fold: float, should_call: bool,
                                    icm_factor: float) -> str:
        """콜링 설명 생성"""
        explanation = f"상대가 올인했을 때 {hand} 핸드로 "
        explanation += f"승률 {win_rate:.1%}, 타이율 {tie_rate:.1%}입니다. "
        explanation += f"ICM 팩터는 {icm_factor:.2f}입니다. "
        
        if win_rate >= 0.5:
            explanation += f"승률이 50% 이상이므로 무조건 CALL을 추천합니다. "
            explanation += f"헤즈업에서 승률이 절반 이상이면 콜이 항상 +EV입니다. "
        else:
            explanation += f"승률이 50% 미만이므로 무조건 FOLD를 추천합니다. "
            explanation += f"헤즈업에서 승률이 절반 미만이면 폴드가 더 나은 선택입니다. "
        
        explanation += f"Call EV: {ev_call:.2f}BB, Fold EV: {ev_fold:.2f}BB입니다."
        
        return explanation
    
    def test_aks_calculation(self):
        """AKs 계산 테스트"""
        hand = "AKs"
        position = "SB"
        stack_size = 10.0
        opponent_stack = 10.0
        pot_size = 20.0
        
        # 승률 계산
        icm_factor = self._calculate_icm_factor(stack_size, opponent_stack, pot_size)
        win_rate, tie_rate = self._calculate_icm_win_rates(hand, position, stack_size, icm_factor)
        
        # EV 계산
        ev_push = self._calculate_icm_push_ev(win_rate, tie_rate, stack_size, pot_size, icm_factor)
        ev_fold = -pot_size * 0.5 * icm_factor
        
        # 결정
        if win_rate >= 0.5:
            recommendation = "PUSH"
            is_push_hand = True
        else:
            is_push_hand = ev_push > ev_fold
            recommendation = "PUSH" if is_push_hand else "FOLD"
        
        print(f"=== AKs 테스트 결과 ===")
        print(f"핸드: {hand}")
        print(f"포지션: {position}")
        print(f"스택: {stack_size}BB")
        print(f"팟: {pot_size}BB")
        print(f"승률: {win_rate:.1%}")
        print(f"타이율: {tie_rate:.1%}")
        print(f"ICM 팩터: {icm_factor:.2f}")
        print(f"Push EV: {ev_push:.2f}BB")
        print(f"Fold EV: {ev_fold:.2f}BB")
        print(f"추천: {recommendation}")
        print(f"승률 50% 이상: {win_rate >= 0.5}")
        print(f"Push > Fold: {ev_push > ev_fold}")
        
        return {
            'hand': hand,
            'win_rate': win_rate,
            'recommendation': recommendation,
            'ev_push': ev_push,
            'ev_fold': ev_fold
        } 