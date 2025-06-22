from poker import Card
from simulate import simulate_multiplayer, simulate_multiplayer_with_community

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

def parse_player_hands():
    """여러 플레이어의 핸드를 입력받는 함수"""
    hands = []
    
    # 내 핸드 입력
    my_input = input("내 카드 2장 입력 (예: AS KD 또는 10S QH): ").strip().split()
    if len(my_input) != 2:
        raise ValueError("카드 2장을 정확히 입력하세요.")
    my_hand = parse_cards(my_input)
    hands.append(my_hand)
    
    # 다른 플레이어들의 핸드 입력
    while True:
        try:
            player_input = input(f"플레이어 {len(hands)} 카드 2장 입력 (엔터로 종료): ").strip()
            if not player_input:
                break
                
            player_cards = player_input.split()
            if len(player_cards) != 2:
                print("카드 2장을 정확히 입력하세요.")
                continue
                
            player_hand = parse_cards(player_cards)
            hands.append(player_hand)
            
        except Exception as e:
            print(f"입력 오류: {e}")
            continue
    
    return hands

def main():
    try:
        print("=== 다중 플레이어 포커 시뮬레이션 ===")
        print("내 핸드와 다른 플레이어들의 핸드를 입력하세요.")
        print("다른 플레이어 입력을 마치려면 엔터를 누르세요.\n")
        
        # 플레이어 핸드들 입력
        all_hands = parse_player_hands()
        
        if len(all_hands) < 2:
            print("최소 2명의 플레이어가 필요합니다.")
            return
        
        my_hand = all_hands[0]
        other_hands = all_hands[1:]
        
        print(f"\n총 {len(all_hands)}명의 플레이어가 참가합니다.")
        print(f"내 핸드: {my_hand}")
        for i, hand in enumerate(other_hands, 1):
            print(f"플레이어 {i} 핸드: {hand}")
        
        # 커뮤니티 카드 입력 (선택사항)
        comm_input = input("\n커뮤니티 카드 입력 (0~5장, 예: 3C 7D QH 또는 10S 5C): ").strip().split()
        known_community = parse_cards(comm_input) if comm_input else []
        
        if known_community:
            print(f"커뮤니티 카드: {known_community}")
        
        # 중복 카드 검사
        all_cards = my_hand + known_community
        for hand in other_hands:
            all_cards.extend(hand)
        
        if len(set(all_cards)) != len(all_cards):
            print("중복된 카드가 있습니다.")
            return
        
        # 시뮬레이션 실행
        print(f"\n{10000}번 시뮬레이션 중...")
        
        if known_community:
            win, tie, loss = simulate_multiplayer_with_community(my_hand, other_hands, known_community, trials=10000)
        else:
            win, tie, loss = simulate_multiplayer(my_hand, other_hands, trials=10000)
        
        print(f"\n=== 결과 ===")
        print(f"승률: {win:.2f}%")
        print(f"무승부: {tie:.2f}%")
        print(f"패배: {loss:.2f}%")
        
        # 플레이어 수에 따른 승률 해석
        if len(other_hands) == 1:
            print("\n2명 플레이어: 일반적인 헤드업 상황")
        elif len(other_hands) == 2:
            print("\n3명 플레이어: 멀티웨이 팟")
        elif len(other_hands) == 3:
            print("\n4명 플레이어: 큰 팟 상황")
        else:
            print(f"\n{len(all_hands)}명 플레이어: 매우 복잡한 상황")

    except Exception as e:
        print("입력 오류:", e)

if __name__ == "__main__":
    main() 