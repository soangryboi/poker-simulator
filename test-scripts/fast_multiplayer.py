from poker import Card
from simulate import simulate_multiplayer, simulate_multiplayer_with_community

def fast_3_players():
    print("=== 빠른 3명 플레이어 시뮬레이션 ===")
    
    my_hand = [Card('A', 'S'), Card('A', 'D')]
    player1 = [Card('K', 'S'), Card('K', 'D')]
    player2 = [Card('Q', 'S'), Card('Q', 'D')]
    
    print(f"내 핸드: {my_hand}")
    print(f"플레이어 1: {player1}")
    print(f"플레이어 2: {player2}")
    
    # 1,000번만 시뮬레이션 (빠름)
    win, tie, loss = simulate_multiplayer(my_hand, [player1, player2], trials=1000)
    
    print(f"\n=== 결과 (1,000번 시뮬레이션) ===")
    print(f"승률: {win:.2f}%")
    print(f"무승부: {tie:.2f}%")
    print(f"패배: {loss:.2f}%")

def fast_4_players():
    print("\n=== 빠른 4명 플레이어 시뮬레이션 ===")
    
    my_hand = [Card('T', 'S'), Card('T', 'D')]
    player1 = [Card('A', 'S'), Card('K', 'D')]
    player2 = [Card('Q', 'S'), Card('J', 'D')]
    player3 = [Card('9', 'S'), Card('8', 'D')]
    
    print(f"내 핸드: {my_hand}")
    print(f"플레이어 1: {player1}")
    print(f"플레이어 2: {player2}")
    print(f"플레이어 3: {player3}")
    
    # 500번만 시뮬레이션 (매우 빠름)
    win, tie, loss = simulate_multiplayer(my_hand, [player1, player2, player3], trials=500)
    
    print(f"\n=== 결과 (500번 시뮬레이션) ===")
    print(f"승률: {win:.2f}%")
    print(f"무승부: {tie:.2f}%")
    print(f"패배: {loss:.2f}%")

def ultra_fast_test():
    print("\n=== 초고속 테스트 (100번 시뮬레이션) ===")
    
    my_hand = [Card('A', 'S'), Card('A', 'D')]
    player1 = [Card('K', 'S'), Card('K', 'D')]
    
    win, tie, loss = simulate_multiplayer(my_hand, [player1], trials=100)
    
    print(f"내 핸드: {my_hand} vs 플레이어: {player1}")
    print(f"승률: {win:.2f}%, 무승부: {tie:.2f}%, 패배: {loss:.2f}%")

if __name__ == "__main__":
    print("🚀 빠른 멀티웨이 시뮬레이션 시작!")
    
    ultra_fast_test()
    fast_3_players()
    fast_4_players()
    
    print("\n✅ 모든 테스트 완료!") 