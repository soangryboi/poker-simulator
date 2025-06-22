import random
from poker import Card, evaluate_hand, compare_hands

class Deck:
    def __init__(self):
        ranks = "23456789TJQKA"
        suits = "SHDC"
        self.cards = [Card(r, s) for r in ranks for s in suits]

    def shuffle(self):
        random.shuffle(self.cards)

    def remove(self, cards):
        self.cards = [c for c in self.cards if c not in cards]

    def draw(self, n):
        drawn = self.cards[:n]
        self.cards = self.cards[n:]
        return drawn

def simulate_vs(my_hand, opp_hand, trials=10000):
    wins = ties = losses = 0
    for _ in range(trials):
        deck = Deck()
        deck.remove(my_hand + opp_hand)
        deck.shuffle()
        community = deck.draw(5)

        my_score = evaluate_hand(my_hand + community)
        opp_score = evaluate_hand(opp_hand + community)
        result = compare_hands(my_score, opp_score)

        if result == 1:
            wins += 1
        elif result == 0:
            ties += 1
        else:
            losses += 1

    return wins/trials*100, ties/trials*100, losses/trials*100
