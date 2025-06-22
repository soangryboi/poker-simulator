import random
from poker import Card, Deck, evaluate_hand, compare_hands

def simulate_vs(my_hand, opp_hand, trials=10000):
    """
    두 플레이어의 핸드로 시뮬레이션
    """
    wins = ties = losses = 0
    
    for _ in range(trials):
        # 덱 생성 및 사용된 카드 제거
        deck = Deck()
        used_cards = my_hand + opp_hand
        deck.cards = [c for c in deck.cards if c not in used_cards]
        
        # 5장의 커뮤니티 카드 뽑기
        community = deck.draw(5)
        
        # 각 플레이어의 7장 카드로 핸드 평가
        my_score = evaluate_hand(my_hand + community)
        opp_score = evaluate_hand(opp_hand + community)
        
        # 승패 결정
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

def simulate_multiplayer_fast(my_hand, other_hands, trials=1000):
    """
    최적화된 다중 플레이어 시뮬레이션 (빠른 버전)
    """
    wins = ties = losses = 0
    
    # 사용된 카드 미리 계산
    used_cards = set(my_hand)
    for hand in other_hands:
        used_cards.update(hand)
    
    # 덱에서 사용된 카드 제거 (set 사용으로 빠름)
    all_cards = []
    for rank in "23456789TJQKA":
        for suit in "SHDC":
            card = Card(rank, suit)
            if card not in used_cards:
                all_cards.append(card)
    
    for _ in range(trials):
        # 커뮤니티 카드 랜덤 선택
        community = random.sample(all_cards, 5)
        
        # 내 핸드 평가
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
        
        # 승패 결정
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

def simulate_multiplayer(my_hand, other_hands, trials=10000):
    """
    다중 플레이어 시뮬레이션 (내 핸드 vs 여러 상대)
    """
    wins = ties = losses = 0
    num_players = len(other_hands) + 1
    
    for _ in range(trials):
        # 덱 생성 및 사용된 카드 제거
        deck = Deck()
        used_cards = my_hand
        for hand in other_hands:
            used_cards.extend(hand)
        deck.cards = [c for c in deck.cards if c not in used_cards]
        
        # 5장의 커뮤니티 카드 뽑기
        community = deck.draw(5)
        
        # 내 핸드 평가
        my_score = evaluate_hand(my_hand + community)
        
        # 다른 플레이어들의 핸드 평가
        other_scores = []
        for hand in other_hands:
            score = evaluate_hand(hand + community)
            other_scores.append(score)
        
        # 승패 결정 (내가 이기려면 모든 상대를 이겨야 함)
        my_wins_this_round = 0
        my_ties_this_round = 0
        
        for opp_score in other_scores:
            result = compare_hands(my_score, opp_score)
            if result == 1:
                my_wins_this_round += 1
            elif result == 0:
                my_ties_this_round += 1
        
        # 모든 상대를 이기면 승리, 모든 상대와 무승부면 무승부, 하나라도 지면 패배
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

def simulate_multiplayer_with_community(my_hand, other_hands, known_community, trials=10000):
    """
    커뮤니티 카드가 일부 알려진 다중 플레이어 시뮬레이션
    """
    wins = ties = losses = 0
    
    for _ in range(trials):
        # 덱 생성 및 사용된 카드 제거
        deck = Deck()
        used_cards = my_hand + known_community
        for hand in other_hands:
            used_cards.extend(hand)
        deck.cards = [c for c in deck.cards if c not in used_cards]
        
        # 남은 커뮤니티 카드 뽑기
        remaining_community = deck.draw(5 - len(known_community))
        full_community = known_community + remaining_community
        
        # 내 핸드 평가
        my_score = evaluate_hand(my_hand + full_community)
        
        # 다른 플레이어들의 핸드 평가
        other_scores = []
        for hand in other_hands:
            score = evaluate_hand(hand + full_community)
            other_scores.append(score)
        
        # 승패 결정
        my_wins_this_round = 0
        my_ties_this_round = 0
        
        for opp_score in other_scores:
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

def simulate_with_community(my_hand, opp_hand, known_community, trials=10000):
    """
    커뮤니티 카드가 일부 알려진 상황에서 시뮬레이션
    """
    wins = ties = losses = 0
    
    for _ in range(trials):
        # 덱 생성 및 사용된 카드 제거
        deck = Deck()
        used_cards = my_hand + opp_hand + known_community
        deck.cards = [c for c in deck.cards if c not in used_cards]
        
        # 남은 커뮤니티 카드 뽑기
        remaining_community = deck.draw(5 - len(known_community))
        full_community = known_community + remaining_community
        
        # 각 플레이어의 7장 카드로 핸드 평가
        my_score = evaluate_hand(my_hand + full_community)
        opp_score = evaluate_hand(opp_hand + full_community)
        
        # 승패 결정
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