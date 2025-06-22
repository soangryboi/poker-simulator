from collections import Counter

# 카드 클래스
class Card:
    def __init__(self, rank, suit):
        self.rank = rank.upper()
        self.suit = suit.upper()

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        return hash((self.rank, self.suit))

# 덱 클래스
class Deck:
    def __init__(self):
        ranks = "23456789TJQKA"
        suits = "SHDC"
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def draw(self, n=1):
        drawn = self.cards[:n]
        self.cards = self.cards[n:]
        return drawn

# 핸드 랭크 상수
RANK_ORDER = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
HAND_RANKS = {
    "High Card": 0,
    "One Pair": 1,
    "Two Pair": 2,
    "Three of a Kind": 3,
    "Straight": 4,
    "Flush": 5,
    "Full House": 6,
    "Four of a Kind": 7,
    "Straight Flush": 8,
}

def check_straight(ranks):
    ranks_set = set(ranks)
    if {14, 2, 3, 4, 5}.issubset(ranks_set):  # A-2-3-4-5
        return True, 5
    for high in range(14, 4, -1):
        if set(range(high, high-5, -1)).issubset(ranks_set):
            return True, high
    return False, None

def evaluate_hand(cards):
    ranks = sorted([RANK_ORDER[c.rank] for c in cards], reverse=True)
    suits = [c.suit for c in cards]

    is_flush = any(suits.count(s) >= 5 for s in suits)
    is_straight, top_straight = check_straight(ranks)

    counts = Counter(ranks)
    counts_by_num = counts.most_common()

    if is_flush and is_straight:
        return (HAND_RANKS["Straight Flush"], [top_straight])
    if counts_by_num[0][1] == 4:
        four = counts_by_num[0][0]
        kickers = [r for r in ranks if r != four]
        return (HAND_RANKS["Four of a Kind"], [four] + kickers)
    if counts_by_num[0][1] == 3 and counts_by_num[1][1] >= 2:
        return (HAND_RANKS["Full House"], [counts_by_num[0][0], counts_by_num[1][0]])
    if is_flush:
        flush_cards = [r for r, s in zip(ranks, suits) if suits.count(s) >= 5]
        return (HAND_RANKS["Flush"], sorted(flush_cards, reverse=True)[:5])
    if is_straight:
        return (HAND_RANKS["Straight"], [top_straight])
    if counts_by_num[0][1] == 3:
        three = counts_by_num[0][0]
        kickers = [r for r in ranks if r != three]
        return (HAND_RANKS["Three of a Kind"], [three] + kickers[:2])
    if counts_by_num[0][1] == 2 and counts_by_num[1][1] == 2:
        high_pair, low_pair = counts_by_num[0][0], counts_by_num[1][0]
        kicker = [r for r in ranks if r != high_pair and r != low_pair]
        return (HAND_RANKS["Two Pair"], [high_pair, low_pair] + kicker[:1])
    if counts_by_num[0][1] == 2:
        pair = counts_by_num[0][0]
        kickers = [r for r in ranks if r != pair]
        return (HAND_RANKS["One Pair"], [pair] + kickers[:3])
    return (HAND_RANKS["High Card"], ranks[:5])

def compare_hands(score1, score2):
    if score1[0] != score2[0]:
        return 1 if score1[0] > score2[0] else -1
    for a, b in zip(score1[1], score2[1]):
        if a != b:
            return 1 if a > b else -1
    return 0
