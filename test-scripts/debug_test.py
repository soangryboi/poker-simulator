print("=== 디버그 테스트 시작 ===")

try:
    print("1. poker 모듈 import 테스트...")
    from poker import Card, Deck, evaluate_hand, compare_hands
    print("✓ poker 모듈 import 성공")
    
    print("2. simulate 모듈 import 테스트...")
    from simulate import simulate_multiplayer
    print("✓ simulate 모듈 import 성공")
    
    print("3. 카드 생성 테스트...")
    card1 = Card('A', 'S')
    card2 = Card('K', 'D')
    print(f"✓ 카드 생성 성공: {card1}, {card2}")
    
    print("4. 간단한 시뮬레이션 테스트...")
    my_hand = [Card('A', 'S'), Card('A', 'D')]
    other_hands = [[Card('K', 'S'), Card('K', 'D')]]
    
    win, tie, loss = simulate_multiplayer(my_hand, other_hands, trials=100)
    print(f"✓ 시뮬레이션 성공: 승률 {win:.2f}%")
    
    print("=== 모든 테스트 통과! ===")
    
except Exception as e:
    print(f"✗ 오류 발생: {e}")
    import traceback
    traceback.print_exc() 