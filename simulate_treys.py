import random
from treys import Card, Deck, Evaluator

evaluator = Evaluator()

def parse_input(cards_str):
    cards = cards_str.strip().split()
    formatted = []
    for card in cards:
        card = card.strip()
        if len(card) != 2:
            raise ValueError(f"잘못된 카드 형식: {card}")
        rank = card[0].upper()
        suit = card[1].lower()
        formatted.append(Card.new(rank + suit))
    return formatted



def simulate_with_community(my_hand_str, opp_hand_str, known_community_str, trials=10000):
    my_hand = parse_input(my_hand_str)
    opp_hand = parse_input(opp_hand_str)
    known_community = parse_input(known_community_str)

    wins = ties = losses = 0

    for _ in range(trials):
        deck = Deck()
        used = my_hand + opp_hand + known_community
        deck.cards = [c for c in deck.cards if c not in used]

        remaining = deck.draw(5 - len(known_community))
        full_board = known_community + remaining

        my_score = evaluator.evaluate(full_board, my_hand)
        opp_score = evaluator.evaluate(full_board, opp_hand)

        if my_score < opp_score:
            wins += 1
        elif my_score > opp_score:
            losses += 1
        else:
            ties += 1

    total = wins + ties + losses
    win_rate = wins / total * 100
    tie_rate = ties / total * 100
    loss_rate = losses / total * 100

    return win_rate, tie_rate, loss_rate


if __name__ == "__main__":
    my = input("내 카드 2장 입력 (예: AS AD): ")
    opp = input("상대 카드 2장 입력 (예: QC QD): ")
    comm = input("커뮤니티 카드 입력 (0~5장, 예: KC 5C 3C 2C): ")

    win, tie, lose = simulate_with_community(my, opp, comm)
    print(f"승률: {win:.2f}%, 무승부: {tie:.2f}%, 패배: {lose:.2f}%")
