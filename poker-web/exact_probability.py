from poker import Card, evaluate_hand, compare_hands
from itertools import combinations
import random

def exact_river_probability(my_hand, opp_hand, community):
    """
    리버 상황에서의 정확한 승률 계산
    커뮤니티 카드가 5장 모두 공개된 경우
    """
    my_score = evaluate_hand(my_hand + community)
    opp_score = evaluate_hand(opp_hand + community)
    
    result = compare_hands(my_score, opp_score)
    
    if result == 1:
        return 100.0, 0.0, 0.0  # 승리
    elif result == -1:
        return 0.0, 0.0, 100.0  # 패배
    else:
        return 0.0, 100.0, 0.0  # 무승부

def exact_turn_probability(my_hand, opp_hand, community):
    """
    턴 상황에서의 정확한 승률 계산
    커뮤니티 카드가 4장 공개된 경우
    """
    wins = ties = losses = 0
    
    # 사용된 카드들
    used_cards = set(my_hand + opp_hand + community)
    
    # 남은 카드들
    remaining_cards = []
    for rank in "23456789TJQKA":
        for suit in "SHDC":
            card = Card(rank, suit)
            if card not in used_cards:
                remaining_cards.append(card)
    
    # 남은 1장의 카드로 모든 경우 계산
    for river_card in remaining_cards:
        full_community = community + [river_card]
        my_score = evaluate_hand(my_hand + full_community)
        opp_score = evaluate_hand(opp_hand + full_community)
        
        result = compare_hands(my_score, opp_score)
        if result == 1:
            wins += 1
        elif result == -1:
            losses += 1
        else:
            ties += 1
    
    total = wins + ties + losses
    win_rate = wins / total * 100
    tie_rate = ties / total * 100
    loss_rate = losses / total * 100
    
    return win_rate, tie_rate, loss_rate

def exact_flop_probability(my_hand, opp_hand, community):
    """
    플랍 상황에서의 정확한 승률 계산
    커뮤니티 카드가 3장 공개된 경우
    """
    wins = ties = losses = 0
    
    # 사용된 카드들
    used_cards = set(my_hand + opp_hand + community)
    
    # 남은 카드들
    remaining_cards = []
    for rank in "23456789TJQKA":
        for suit in "SHDC":
            card = Card(rank, suit)
            if card not in used_cards:
                remaining_cards.append(card)
    
    # 남은 2장의 카드 조합으로 모든 경우 계산
    for turn_card, river_card in combinations(remaining_cards, 2):
        full_community = community + [turn_card, river_card]
        my_score = evaluate_hand(my_hand + full_community)
        opp_score = evaluate_hand(opp_hand + full_community)
        
        result = compare_hands(my_score, opp_score)
        if result == 1:
            wins += 1
        elif result == -1:
            losses += 1
        else:
            ties += 1
    
    total = wins + ties + losses
    win_rate = wins / total * 100
    tie_rate = ties / total * 100
    loss_rate = losses / total * 100
    
    return win_rate, tie_rate, loss_rate

def exact_partial_community_probability(my_hand, opp_hand, community):
    """
    커뮤니티 카드가 1장이나 2장인 경우의 정확한 승률 계산
    """
    wins = ties = losses = 0
    
    # 사용된 카드들
    used_cards = set(my_hand + opp_hand + community)
    
    # 남은 카드들
    remaining_cards = []
    for rank in "23456789TJQKA":
        for suit in "SHDC":
            card = Card(rank, suit)
            if card not in used_cards:
                remaining_cards.append(card)
    
    # 남은 카드들로 5장이 되도록 조합 계산
    needed_cards = 5 - len(community)
    for additional_cards in combinations(remaining_cards, needed_cards):
        full_community = community + list(additional_cards)
        my_score = evaluate_hand(my_hand + full_community)
        opp_score = evaluate_hand(opp_hand + full_community)
        
        result = compare_hands(my_score, opp_score)
        if result == 1:
            wins += 1
        elif result == -1:
            losses += 1
        else:
            ties += 1
    
    total = wins + ties + losses
    win_rate = wins / total * 100
    tie_rate = ties / total * 100
    loss_rate = losses / total * 100
    
    return win_rate, tie_rate, loss_rate

def exact_preflop_probability(my_hand, opp_hand, trials=50000):
    """
    프리플랍 상황에서의 승률 계산 (시뮬레이션 사용)
    커뮤니티 카드가 없는 경우
    """
    wins = ties = losses = 0
    
    # 사용된 카드들
    used_cards = set(my_hand + opp_hand)
    
    # 남은 카드들
    remaining_cards = []
    for rank in "23456789TJQKA":
        for suit in "SHDC":
            card = Card(rank, suit)
            if card not in used_cards:
                remaining_cards.append(card)
    
    # 시뮬레이션으로 계산 (정확한 계산은 너무 느림)
    for _ in range(trials):
        # 5장의 커뮤니티 카드 랜덤 선택
        community = random.sample(remaining_cards, 5)
        
        my_score = evaluate_hand(my_hand + community)
        opp_score = evaluate_hand(opp_hand + community)
        
        result = compare_hands(my_score, opp_score)
        if result == 1:
            wins += 1
        elif result == -1:
            losses += 1
        else:
            ties += 1
    
    total = wins + ties + losses
    win_rate = wins / total * 100
    tie_rate = ties / total * 100
    loss_rate = losses / total * 100
    
    return win_rate, tie_rate, loss_rate

def exact_multiplayer_river(my_hand, other_hands, community):
    """
    다중 플레이어 리버 상황에서의 정확한 승률 계산
    """
    my_score = evaluate_hand(my_hand + community)
    
    # 다른 플레이어들의 핸드 평가
    my_wins_this_round = 0
    my_ties_this_round = 0
    
    for hand in other_hands:
        opp_score = evaluate_hand(hand + community)
        result = compare_hands(my_score, opp_score)
        if result == 1:
            my_wins_this_round += 1
        elif result == 0:
            my_ties_this_round += 1
    
    # 모든 상대를 이기면 승리, 모든 상대와 무승부면 무승부, 하나라도 지면 패배
    if my_wins_this_round == len(other_hands):
        return 100.0, 0.0, 0.0
    elif my_wins_this_round + my_ties_this_round == len(other_hands):
        return 0.0, 100.0, 0.0
    else:
        return 0.0, 0.0, 100.0

def exact_multiplayer_turn(my_hand, other_hands, community):
    """
    다중 플레이어 턴 상황에서의 정확한 승률 계산
    """
    wins = ties = losses = 0
    
    # 사용된 카드들
    used_cards = set(my_hand + community)
    for hand in other_hands:
        used_cards.update(hand)
    
    # 남은 카드들
    remaining_cards = []
    for rank in "23456789TJQKA":
        for suit in "SHDC":
            card = Card(rank, suit)
            if card not in used_cards:
                remaining_cards.append(card)
    
    # 남은 1장의 카드로 모든 경우 계산
    for river_card in remaining_cards:
        full_community = community + [river_card]
        my_score = evaluate_hand(my_hand + full_community)
        
        my_wins_this_round = 0
        my_ties_this_round = 0
        
        for hand in other_hands:
            opp_score = evaluate_hand(hand + full_community)
            result = compare_hands(my_score, opp_score)
            if result == 1:
                my_wins_this_round += 1
            elif result == 0:
                my_ties_this_round += 1
        
        if my_wins_this_round == len(other_hands):
            wins += 1
        elif my_wins_this_round + my_ties_this_round == len(other_hands):
            ties += 1
        else:
            losses += 1
    
    total = wins + ties + losses
    win_rate = wins / total * 100
    tie_rate = ties / total * 100
    loss_rate = losses / total * 100
    
    return win_rate, tie_rate, loss_rate

def exact_multiplayer_partial_community(my_hand, other_hands, community):
    """
    다중 플레이어에서 커뮤니티 카드가 1장이나 2장인 경우의 정확한 승률 계산
    """
    wins = ties = losses = 0
    
    # 사용된 카드들
    used_cards = set(my_hand + community)
    for hand in other_hands:
        used_cards.update(hand)
    
    # 남은 카드들
    remaining_cards = []
    for rank in "23456789TJQKA":
        for suit in "SHDC":
            card = Card(rank, suit)
            if card not in used_cards:
                remaining_cards.append(card)
    
    # 남은 카드들로 5장이 되도록 조합 계산
    needed_cards = 5 - len(community)
    for additional_cards in combinations(remaining_cards, needed_cards):
        full_community = community + list(additional_cards)
        my_score = evaluate_hand(my_hand + full_community)
        
        my_wins_this_round = 0
        my_ties_this_round = 0
        
        for hand in other_hands:
            opp_score = evaluate_hand(hand + full_community)
            result = compare_hands(my_score, opp_score)
            if result == 1:
                my_wins_this_round += 1
            elif result == 0:
                my_ties_this_round += 1
        
        if my_wins_this_round == len(other_hands):
            wins += 1
        elif my_wins_this_round + my_ties_this_round == len(other_hands):
            ties += 1
        else:
            losses += 1
    
    total = wins + ties + losses
    win_rate = wins / total * 100
    tie_rate = ties / total * 100
    loss_rate = losses / total * 100
    
    return win_rate, tie_rate, loss_rate

def exact_multiplayer_preflop(my_hand, other_hands, trials=50000):
    """
    다중 플레이어 프리플랍 상황에서의 승률 계산
    """
    wins = ties = losses = 0
    
    # 사용된 카드들
    used_cards = set(my_hand)
    for hand in other_hands:
        used_cards.update(hand)
    
    # 남은 카드들
    remaining_cards = []
    for rank in "23456789TJQKA":
        for suit in "SHDC":
            card = Card(rank, suit)
            if card not in used_cards:
                remaining_cards.append(card)
    
    # 시뮬레이션으로 계산
    for _ in range(trials):
        community = random.sample(remaining_cards, 5)
        my_score = evaluate_hand(my_hand + community)
        
        my_wins_this_round = 0
        my_ties_this_round = 0
        
        for hand in other_hands:
            opp_score = evaluate_hand(hand + community)
            result = compare_hands(my_score, opp_score)
            if result == 1:
                my_wins_this_round += 1
            elif result == 0:
                my_ties_this_round += 1
        
        if my_wins_this_round == len(other_hands):
            wins += 1
        elif my_wins_this_round + my_ties_this_round == len(other_hands):
            ties += 1
        else:
            losses += 1
    
    total = wins + ties + losses
    win_rate = wins / total * 100
    tie_rate = ties / total * 100
    loss_rate = losses / total * 100
    
    return win_rate, tie_rate, loss_rate

def calculate_individual_win_rates(hands, community):
    """
    모든 플레이어의 개별 승률을 계산
    hands: [플레이어1_핸드, 플레이어2_핸드, ...]
    community: 커뮤니티 카드
    returns: [플레이어1_승률, 플레이어2_승률, ...], 무승부_확률
    """
    if len(hands) == 0:
        return [], 0.0
    
    # 각 플레이어의 핸드 점수 계산
    scores = []
    for hand in hands:
        score = evaluate_hand(hand + community)
        scores.append(score)
    
    # 승자 결정
    best_score = max(scores)
    winners = [i for i, score in enumerate(scores) if score == best_score]
    
    # 개별 승률 계산
    win_rates = []
    for i in range(len(hands)):
        if i in winners:
            win_rate = 1.0 / len(winners)  # 승자들끼리 균등 분배
        else:
            win_rate = 0.0
        win_rates.append(win_rate)
    
    # 무승부 확률 (승자가 2명 이상일 때)
    tie_rate = 1.0 if len(winners) > 1 else 0.0
    
    return win_rates, tie_rate

def exact_multiplayer_river_individual(my_hand, other_hands, community):
    """
    다중 플레이어 리버 상황에서 각 플레이어의 개별 승률 계산
    """
    all_hands = [my_hand] + other_hands
    win_rates, tie_rate = calculate_individual_win_rates(all_hands, community)
    
    return win_rates, tie_rate

def exact_multiplayer_turn_individual(my_hand, other_hands, community):
    """
    다중 플레이어 턴 상황에서 각 플레이어의 개별 승률 계산
    """
    all_hands = [my_hand] + other_hands
    total_win_rates = [0.0] * len(all_hands)
    total_tie_rate = 0.0
    total_scenarios = 0
    
    # 사용된 카드들
    used_cards = set()
    for hand in all_hands:
        used_cards.update(hand)
    used_cards.update(community)
    
    # 남은 카드들
    remaining_cards = []
    for rank in "23456789TJQKA":
        for suit in "SHDC":
            card = Card(rank, suit)
            if card not in used_cards:
                remaining_cards.append(card)
    
    # 남은 1장의 카드로 모든 경우 계산
    for river_card in remaining_cards:
        full_community = community + [river_card]
        win_rates, tie_rate = calculate_individual_win_rates(all_hands, full_community)
        
        for i in range(len(all_hands)):
            total_win_rates[i] += win_rates[i]
        total_tie_rate += tie_rate
        total_scenarios += 1
    
    # 평균 계산
    final_win_rates = [rate / total_scenarios for rate in total_win_rates]
    final_tie_rate = total_tie_rate / total_scenarios
    
    return final_win_rates, final_tie_rate

def exact_multiplayer_flop_individual(my_hand, other_hands, community):
    """
    다중 플레이어 플랍 상황에서 각 플레이어의 개별 승률 계산
    """
    all_hands = [my_hand] + other_hands
    total_win_rates = [0.0] * len(all_hands)
    total_tie_rate = 0.0
    total_scenarios = 0
    
    # 사용된 카드들
    used_cards = set()
    for hand in all_hands:
        used_cards.update(hand)
    used_cards.update(community)
    
    # 남은 카드들
    remaining_cards = []
    for rank in "23456789TJQKA":
        for suit in "SHDC":
            card = Card(rank, suit)
            if card not in used_cards:
                remaining_cards.append(card)
    
    # 남은 2장의 카드 조합으로 모든 경우 계산
    for turn_card, river_card in combinations(remaining_cards, 2):
        full_community = community + [turn_card, river_card]
        win_rates, tie_rate = calculate_individual_win_rates(all_hands, full_community)
        
        for i in range(len(all_hands)):
            total_win_rates[i] += win_rates[i]
        total_tie_rate += tie_rate
        total_scenarios += 1
    
    # 평균 계산
    final_win_rates = [rate / total_scenarios for rate in total_win_rates]
    final_tie_rate = total_tie_rate / total_scenarios
    
    return final_win_rates, final_tie_rate

def exact_multiplayer_preflop_individual(my_hand, other_hands, trials=50000):
    """
    다중 플레이어 프리플랍 상황에서 각 플레이어의 개별 승률 계산
    """
    all_hands = [my_hand] + other_hands
    
    # 플레이어 수에 따라 시뮬레이션 횟수 조정
    if len(all_hands) <= 3:
        adjusted_trials = 50000
    elif len(all_hands) <= 5:
        adjusted_trials = 30000
    elif len(all_hands) <= 7:
        adjusted_trials = 20000
    else:  # 8명 이상
        adjusted_trials = 15000
    
    total_win_rates = [0.0] * len(all_hands)
    total_tie_rate = 0.0
    
    # 사용된 카드들
    used_cards = set()
    for hand in all_hands:
        used_cards.update(hand)
    
    # 남은 카드들
    remaining_cards = []
    for rank in "23456789TJQKA":
        for suit in "SHDC":
            card = Card(rank, suit)
            if card not in used_cards:
                remaining_cards.append(card)
    
    # 시뮬레이션으로 계산
    for _ in range(adjusted_trials):
        community = random.sample(remaining_cards, 5)
        win_rates, tie_rate = calculate_individual_win_rates(all_hands, community)
        
        for i in range(len(all_hands)):
            total_win_rates[i] += win_rates[i]
        total_tie_rate += tie_rate
    
    # 평균 계산
    final_win_rates = [rate / adjusted_trials for rate in total_win_rates]
    final_tie_rate = total_tie_rate / adjusted_trials
    
    return final_win_rates, final_tie_rate

# 테스트 함수
def test_exact_probabilities():
    print("=== 정확한 확률 계산 테스트 ===")
    
    my_hand = [Card('A', 'S'), Card('A', 'D')]
    opp_hand = [Card('K', 'S'), Card('K', 'D')]
    
    print(f"내 핸드: {my_hand}")
    print(f"상대 핸드: {opp_hand}")
    
    # 프리플랍 테스트
    print("\n--- 프리플랍 (시뮬레이션 50,000번) ---")
    win, tie, loss = exact_preflop_probability(my_hand, opp_hand, trials=50000)
    print(f"프리플랍 승률: {win:.2f}%, 무승부: {tie:.2f}%, 패배: {loss:.2f}%")
    
    # 리버 테스트
    community = [Card('T', 'S'), Card('5', 'C'), Card('3', 'C'), Card('2', 'H'), Card('7', 'D')]
    win, tie, loss = exact_river_probability(my_hand, opp_hand, community)
    print(f"\n--- 리버 (정확한 계산) ---")
    print(f"보드: {community}")
    print(f"리버 승률: {win:.2f}%, 무승부: {tie:.2f}%, 패배: {loss:.2f}%")
    
    # 턴 테스트
    community = [Card('T', 'S'), Card('5', 'C'), Card('3', 'C'), Card('2', 'H')]
    win, tie, loss = exact_turn_probability(my_hand, opp_hand, community)
    print(f"\n--- 턴 (정확한 계산) ---")
    print(f"보드: {community}")
    print(f"턴 승률: {win:.2f}%, 무승부: {tie:.2f}%, 패배: {loss:.2f}%")
    
    # 플랍 테스트
    community = [Card('T', 'S'), Card('5', 'C'), Card('3', 'C')]
    win, tie, loss = exact_flop_probability(my_hand, opp_hand, community)
    print(f"\n--- 플랍 (정확한 계산) ---")
    print(f"보드: {community}")
    print(f"플랍 승률: {win:.2f}%, 무승부: {tie:.2f}%, 패배: {loss:.2f}%")

def test_multiplayer_probabilities():
    print("\n=== 다중 플레이어 정확한 확률 계산 테스트 ===")
    
    my_hand = [Card('A', 'S'), Card('A', 'D')]
    player1 = [Card('K', 'S'), Card('K', 'D')]
    player2 = [Card('Q', 'S'), Card('Q', 'D')]
    
    print(f"내 핸드: {my_hand}")
    print(f"플레이어 1: {player1}")
    print(f"플레이어 2: {player2}")
    
    # 3명 플레이어 프리플랍
    print("\n--- 3명 플레이어 프리플랍 ---")
    win, tie, loss = exact_multiplayer_preflop(my_hand, [player1, player2], trials=50000)
    print(f"승률: {win:.2f}%, 무승부: {tie:.2f}%, 패배: {loss:.2f}%")
    
    # 3명 플레이어 턴
    community = [Card('T', 'S'), Card('5', 'C'), Card('3', 'C'), Card('2', 'H')]
    print(f"\n--- 3명 플레이어 턴 ---")
    print(f"보드: {community}")
    win, tie, loss = exact_multiplayer_turn(my_hand, [player1, player2], community)
    print(f"승률: {win:.2f}%, 무승부: {tie:.2f}%, 패배: {loss:.2f}%")
    
    # 3명 플레이어 리버
    community = [Card('T', 'S'), Card('5', 'C'), Card('3', 'C'), Card('2', 'H'), Card('7', 'D')]
    print(f"\n--- 3명 플레이어 리버 ---")
    print(f"보드: {community}")
    win, tie, loss = exact_multiplayer_river(my_hand, [player1, player2], community)
    print(f"승률: {win:.2f}%, 무승부: {tie:.2f}%, 패배: {loss:.2f}%")

if __name__ == "__main__":
    test_exact_probabilities()
    test_multiplayer_probabilities() 