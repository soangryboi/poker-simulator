print("멀티웨이 테스트 시작...")

try:
    from poker import Card
    print("✓ Card import 성공")
    
    from simulate import simulate_multiplayer
    print("✓ simulate_multiplayer import 성공")
    
    # 간단한 3명 플레이어 테스트
    my_hand = [Card('A', 'S'), Card('A', 'D')]
    player1 = [Card('K', 'S'), Card('K', 'D')]
    player2 = [Card('Q', 'S'), Card('Q', 'D')]
    
    print(f"내 핸드: {my_hand}")
    print(f"플레이어 1: {player1}")
    print(f"플레이어 2: {player2}")
    
    # 100번만 시뮬레이션 (빠른 테스트)
    win, tie, loss = simulate_multiplayer(my_hand, [player1, player2], trials=100)
    
    print(f"\n=== 3명 플레이어 결과 ===")
    print(f"승률: {win:.2f}%")
    print(f"무승부: {tie:.2f}%")
    print(f"패배: {loss:.2f}%")
    
    print("\n✓ 멀티웨이 테스트 성공!")
    
except Exception as e:
    print(f"✗ 오류: {e}")
    import traceback
    traceback.print_exc() 