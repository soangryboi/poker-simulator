from poker import Card
from simulate import evaluate_hand, compare_hands

def test_specific_case():
    my_hand = [Card('A', 'S'), Card('A', 'D')]
    opp_hand = [Card('Q', 'C'), Card('Q', 'D')]
    community_cards = [Card('K', 'C'), Card('5', 'C'), Card('3', 'C'), Card('2', 'C')]
    
    remaining_cards = [Card(r, s) for r in "23456789TJQKA" for s in "SHDC"]
    exclude = my_hand + opp_hand + community_cards
    remaining_cards = [c for c in remaining_cards if c not in exclude]

    win = 0
    tie = 0
    loss = 0

    for river_card in remaining_cards:
        my_score = evaluate_hand(my_hand + community_cards + [river_card])
        opp_score = evaluate_hand(opp_hand + community_cards + [river_card])
        result = compare_hands(my_score, opp_score)
        if result == 1:
            win += 1
        elif result == 0:
            tie += 1
        else:
            loss += 1

    total = win + tie + loss
    print(f"승리 횟수: {win}, 무승부: {tie}, 패배 횟수: {loss}, 총 경우의 수: {total}")
    print(f"승률: {win/total*100:.2f}%, 무승부율: {tie/total*100:.2f}%, 패배율: {loss/total*100:.2f}%")

if __name__ == "__main__":
    test_specific_case()
