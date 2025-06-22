from poker import Card
from simulate import simulate_multiplayer, simulate_multiplayer_with_community

def test_3_players():
    print("=== 3명 플레이어 시뮬레이션 테스트 ===")
    
    # 내 핸드: AS AD (에이스 페어)
    my_hand = [Card('A', 'S'), Card('A', 'D')]
    print(f"내 핸드: {my_hand}")
    
    # 플레이어 1: KS KD (킹 페어)
    player1 = [Card('K', 'S'), Card('K', 'D')]
    print(f"플레이어 1: {player1}")
    
    # 플레이어 2: QS QD (퀸 페어)
    player2 = [Card('Q', 'S'), Card('Q', 'D')]
    print(f"플레이어 2: {player2}")
    
    other_hands = [player1, player2]
    
    # 시뮬레이션 실행
    win, tie, loss = simulate_multiplayer(my_hand, other_hands, trials=10000)
    
    print(f"\n=== 결과 ===")
    print(f"승률: {win:.2f}%")
    print(f"무승부: {tie:.2f}%")
    print(f"패배: {loss:.2f}%")

def test_4_players():
    print("\n=== 4명 플레이어 시뮬레이션 테스트 ===")
    
    # 내 핸드: 10S 10D (10 페어)
    my_hand = [Card('T', 'S'), Card('T', 'D')]
    print(f"내 핸드: {my_hand}")
    
    # 플레이어 1: AS KD (에이스 킹)
    player1 = [Card('A', 'S'), Card('K', 'D')]
    print(f"플레이어 1: {player1}")
    
    # 플레이어 2: QS JD (퀸 잭)
    player2 = [Card('Q', 'S'), Card('J', 'D')]
    print(f"플레이어 2: {player2}")
    
    # 플레이어 3: 9S 8D (9 8)
    player3 = [Card('9', 'S'), Card('8', 'D')]
    print(f"플레이어 3: {player3}")
    
    other_hands = [player1, player2, player3]
    
    # 시뮬레이션 실행
    win, tie, loss = simulate_multiplayer(my_hand, other_hands, trials=10000)
    
    print(f"\n=== 결과 ===")
    print(f"승률: {win:.2f}%")
    print(f"무승부: {tie:.2f}%")
    print(f"패배: {loss:.2f}%")

def test_4_players_with_community():
    print("\n=== 4명 플레이어 + 커뮤니티 카드 시뮬레이션 테스트 ===")
    
    # 내 핸드: AS AD (에이스 페어)
    my_hand = [Card('A', 'S'), Card('A', 'D')]
    print(f"내 핸드: {my_hand}")
    
    # 플레이어 1: KS KD (킹 페어)
    player1 = [Card('K', 'S'), Card('K', 'D')]
    print(f"플레이어 1: {player1}")
    
    # 플레이어 2: QS QD (퀸 페어)
    player2 = [Card('Q', 'S'), Card('Q', 'D')]
    print(f"플레이어 2: {player2}")
    
    # 플레이어 3: JS JD (잭 페어)
    player3 = [Card('J', 'S'), Card('J', 'D')]
    print(f"플레이어 3: {player3}")
    
    # 커뮤니티 카드: 10S 5C 3C (10 스페이드, 5 클럽, 3 클럽)
    community = [Card('T', 'S'), Card('5', 'C'), Card('3', 'C')]
    print(f"커뮤니티 카드: {community}")
    
    other_hands = [player1, player2, player3]
    
    # 시뮬레이션 실행
    win, tie, loss = simulate_multiplayer_with_community(my_hand, other_hands, community, trials=10000)
    
    print(f"\n=== 결과 ===")
    print(f"승률: {win:.2f}%")
    print(f"무승부: {tie:.2f}%")
    print(f"패배: {loss:.2f}%")

if __name__ == "__main__":
    test_3_players()
    test_4_players()
    test_4_players_with_community() 