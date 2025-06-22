from user_input import parse_cards
from simulate import simulate_with_community

def test_10_card_simulation():
    print("=== 10 카드 시뮬레이션 테스트 ===")
    
    # 내 카드: 10S 10D (10 스페이드, 10 다이아몬드)
    my_hand = parse_cards(["10S", "10D"])
    print(f"내 카드: {my_hand}")
    
    # 상대 카드: AS KD (에이스 스페이드, 킹 다이아몬드)
    opp_hand = parse_cards(["AS", "KD"])
    print(f"상대 카드: {opp_hand}")
    
    # 커뮤니티 카드: 10H 5C 3C (10 하트, 5 클럽, 3 클럽)
    community = parse_cards(["10H", "5C", "3C"])
    print(f"커뮤니티 카드: {community}")
    
    # 시뮬레이션 실행
    win, tie, loss = simulate_with_community(my_hand, opp_hand, community, trials=10000)
    
    print(f"\n=== 결과 ===")
    print(f"승률: {win:.2f}%")
    print(f"무승부: {tie:.2f}%")
    print(f"패배: {loss:.2f}%")

if __name__ == "__main__":
    test_10_card_simulation() 