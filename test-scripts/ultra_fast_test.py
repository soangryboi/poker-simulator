from poker import Card
from simulate import simulate_multiplayer_fast

def ultra_fast_3_players():
    print("⚡ 초고속 3명 플레이어 테스트 (100번 시뮬레이션)")
    
    my_hand = [Card('A', 'S'), Card('A', 'D')]
    player1 = [Card('K', 'S'), Card('K', 'D')]
    player2 = [Card('Q', 'S'), Card('Q', 'D')]
    
    win, tie, loss = simulate_multiplayer_fast(my_hand, [player1, player2], trials=100)
    
    print(f"내 핸드: {my_hand}")
    print(f"플레이어 1: {player1}")
    print(f"플레이어 2: {player2}")
    print(f"결과: 승률 {win:.1f}%, 무승부 {tie:.1f}%, 패배 {loss:.1f}%")

def ultra_fast_4_players():
    print("\n⚡ 초고속 4명 플레이어 테스트 (200번 시뮬레이션)")
    
    my_hand = [Card('T', 'S'), Card('T', 'D')]
    player1 = [Card('A', 'S'), Card('K', 'D')]
    player2 = [Card('Q', 'S'), Card('J', 'D')]
    player3 = [Card('9', 'S'), Card('8', 'D')]
    
    win, tie, loss = simulate_multiplayer_fast(my_hand, [player1, player2, player3], trials=200)
    
    print(f"내 핸드: {my_hand}")
    print(f"플레이어 1: {player1}")
    print(f"플레이어 2: {player2}")
    print(f"플레이어 3: {player3}")
    print(f"결과: 승률 {win:.1f}%, 무승부 {tie:.1f}%, 패배 {loss:.1f}%")

if __name__ == "__main__":
    print("🚀 초고속 멀티웨이 시뮬레이션!")
    print("=" * 50)
    
    ultra_fast_3_players()
    ultra_fast_4_players()
    
    print("\n✅ 완료! (1-2초 내에 실행됨)") 