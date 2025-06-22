from poker import Card, evaluate_hand

def test_basic_hands():
    print("=== 기본 핸드 테스트 ===")
    
    # 페어 테스트
    pair_hand = [Card('A', 'S'), Card('A', 'D'), Card('K', 'H'), Card('Q', 'C'), Card('J', 'S')]
    score = evaluate_hand(pair_hand)
    print(f"페어 핸드: {score}")
    
    # 플러시 테스트
    flush_hand = [Card('A', 'S'), Card('K', 'S'), Card('Q', 'S'), Card('J', 'S'), Card('9', 'S')]
    score = evaluate_hand(flush_hand)
    print(f"플러시 핸드: {score}")
    
    # 7장 카드 테스트 (내 핸드 2장 + 커뮤니티 5장)
    seven_cards = [Card('A', 'S'), Card('A', 'D'), Card('K', 'H'), Card('Q', 'C'), Card('J', 'S'), Card('10', 'H'), Card('9', 'D')]
    score = evaluate_hand(seven_cards)
    print(f"7장 카드 핸드: {score}")
    
    print("=== 테스트 완료 ===")

if __name__ == "__main__":
    test_basic_hands() 