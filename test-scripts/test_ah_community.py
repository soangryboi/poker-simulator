from exact_probability import exact_partial_community_probability
from poker import Card

def test_ah_community():
    print("=== AH 보드 카드 테스트 ===")
    
    # 내 핸드: AS AD (에이스 페어)
    my_hand = [Card('A', 'S'), Card('A', 'D')]
    print(f"내 핸드: {my_hand}")
    
    # 상대 핸드: KS KD (킹 페어)
    opp_hand = [Card('K', 'S'), Card('K', 'D')]
    print(f"상대 핸드: {opp_hand}")
    
    # 보드: AH (에이스 하트)
    community = [Card('A', 'H')]
    print(f"보드: {community}")
    
    print("\n🎯 보드 카드 1장 상황 (정확한 계산)")
    win, tie, loss = exact_partial_community_probability(my_hand, opp_hand, community)
    
    print(f"승률: {win:.2f}%")
    print(f"무승부: {tie:.2f}%")
    print(f"패배: {loss:.2f}%")

if __name__ == "__main__":
    test_ah_community() 