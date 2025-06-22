from poker import Card
from simulate import simulate_vs

def main():
    my_hand = [Card('A', 'S'), Card('A', 'D')]
    opp_hand = [Card('K', 'H'), Card('K', 'C')]

    win, tie, loss = simulate_vs(my_hand, opp_hand, trials=10000)
    print(f"내 승률: {win:.2f}%, 무승부: {tie:.2f}%, 패배: {loss:.2f}%")

if __name__ == "__main__":
    main()
