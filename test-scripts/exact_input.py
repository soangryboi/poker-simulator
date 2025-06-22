from exact_probability import *
from poker import Card

def parse_card(card_str):
    ranks = "23456789TJQKA"
    suits = "SHDC"
    
    # 10 카드 처리 (3자리: 10s, 10h, 10d, 10c)
    if card_str.upper().startswith("10"):
        if len(card_str) != 3:
            raise ValueError("10 카드 형식이 잘못되었습니다. 예: 10S")
        rank, suit = "T", card_str[2].upper()
    # 일반 카드 처리 (2자리: AS, KD, QH, JC 등)
    elif len(card_str) == 2:
        rank, suit = card_str[0].upper(), card_str[1].upper()
    else:
        raise ValueError("카드 형식이 잘못되었습니다. 예: AS, 10S")
    
    if rank not in ranks or suit not in suits:
        raise ValueError("올바른 카드가 아닙니다.")
    return Card(rank, suit)

def parse_cards(card_strs):
    return [parse_card(cs) for cs in card_strs]

def main():
    print("=== 정확한 포커 확률 계산기 ===")
    print("프리플랍, 플랍, 턴, 리버 모든 상황에서 정확한 확률 계산!")
    print()
    
    try:
        # 내 핸드 입력
        my_input = input("내 카드 2장 입력 (예: AS KD 또는 10S QH): ").strip().split()
        if len(my_input) != 2:
            print("카드 2장을 정확히 입력하세요.")
            return
        my_hand = parse_cards(my_input)
        
        # 상대 핸드들 입력
        other_hands = []
        player_num = 1
        while True:
            opp_input = input(f"상대 {player_num} 카드 2장 입력 (엔터로 종료): ").strip()
            if not opp_input:
                break
            opp_cards = opp_input.split()
            if len(opp_cards) != 2:
                print("카드 2장을 정확히 입력하세요.")
                continue
            other_hands.append(parse_cards(opp_cards))
            player_num += 1
        
        if not other_hands:
            print("최소 1명의 상대가 필요합니다.")
            return
        
        # 보드 카드 입력
        comm_input = input("보드 카드 입력 (0~5장, 예: 3C 7D QH 또는 10S 5C): ").strip().split()
        known_community = parse_cards(comm_input) if comm_input else []
        
        # 중복 카드 검사
        all_cards = my_hand + known_community
        for hand in other_hands:
            all_cards.extend(hand)
        
        if len(set(all_cards)) != len(all_cards):
            print("중복된 카드가 있습니다.")
            return
        
        print(f"\n=== 입력 확인 ===")
        print(f"내 핸드: {my_hand}")
        for i, hand in enumerate(other_hands, 1):
            print(f"상대 {i} 핸드: {hand}")
        if known_community:
            print(f"보드: {known_community}")
        
        print(f"\n=== 정확한 확률 계산 결과 ===")
        
        # 상황에 따른 계산
        if len(known_community) == 5:
            # 리버 상황 - 정확한 계산
            print("🎯 리버 상황 (정확한 계산)")
            if len(other_hands) == 1:
                win, tie, loss = exact_river_probability(my_hand, other_hands[0], known_community)
            else:
                win, tie, loss = exact_multiplayer_river(my_hand, other_hands, known_community)
            
        elif len(known_community) == 4:
            # 턴 상황 - 정확한 계산
            print("🎯 턴 상황 (정확한 계산)")
            if len(other_hands) == 1:
                win, tie, loss = exact_turn_probability(my_hand, other_hands[0], known_community)
            else:
                win, tie, loss = exact_multiplayer_turn(my_hand, other_hands, known_community)
            
        elif len(known_community) == 3:
            # 플랍 상황 - 정확한 계산
            print("🎯 플랍 상황 (정확한 계산)")
            if len(other_hands) == 1:
                win, tie, loss = exact_flop_probability(my_hand, other_hands[0], known_community)
            else:
                # 다중 플레이어 플랍은 시뮬레이션 사용
                print("다중 플레이어 플랍은 시뮬레이션으로 계산합니다.")
                win, tie, loss = exact_multiplayer_preflop(my_hand, other_hands, trials=10000)
            
        elif len(known_community) in [1, 2]:
            # 보드 카드가 1장이나 2장인 경우 - 정확한 계산
            print(f"🎯 보드 카드 {len(known_community)}장 상황 (정확한 계산)")
            if len(other_hands) == 1:
                win, tie, loss = exact_partial_community_probability(my_hand, other_hands[0], known_community)
            else:
                win, tie, loss = exact_multiplayer_partial_community(my_hand, other_hands, known_community)
            
        else:
            # 프리플랍 상황 - 시뮬레이션
            print("🎯 프리플랍 상황 (고정밀 시뮬레이션)")
            if len(other_hands) == 1:
                win, tie, loss = exact_preflop_probability(my_hand, other_hands[0], trials=50000)
            else:
                win, tie, loss = exact_multiplayer_preflop(my_hand, other_hands, trials=50000)
        
        print(f"승률: {win:.2f}%")
        print(f"무승부: {tie:.2f}%")
        print(f"패배: {loss:.2f}%")
            
    except Exception as e:
        print(f"입력 오류: {e}")

if __name__ == "__main__":
    main() 