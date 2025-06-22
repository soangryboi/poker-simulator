from user_input import parse_card

def test_10_cards():
    print("=== 10 카드 입력 테스트 ===")
    
    # 테스트 케이스들
    test_cards = [
        "10S", "10H", "10D", "10C",  # 10 카드들
        "AS", "KD", "QH", "JC",      # 일반 카드들
        "10s", "10h", "10d", "10c"   # 소문자 10 카드들
    ]
    
    for card_str in test_cards:
        try:
            card = parse_card(card_str)
            print(f"✓ {card_str} -> {card}")
        except Exception as e:
            print(f"✗ {card_str} -> 오류: {e}")

if __name__ == "__main__":
    test_10_cards() 