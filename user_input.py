from poker import Card
from simulate import simulate_vs

def parse_card(card_str):
    ranks = "23456789TJQKA"
    suits = "SHDC"
    if len(card_str) != 2:
        raise ValueError("카드 형식이 잘못되었습니다. 예: AS")
    rank, suit = card_str[0].upper(), card_str[1].upper()
    if rank not in ranks or suit not in suits:
        raise ValueError("올바른 카드가 아닙니다.")
    return Card(rank, suit)

def main():
    try:
        my_input = input("내 카드 2장 입력 (예: AS KD): ").strip().split()
        opp_input = input("상대 카드 2장 입력 (예: QC 9H): ").strip().split()

        if len(my_input) != 2 or len(opp_input) != 2:
            print("카드 2장을 정확히 입력하세요.")
            return

        my_hand = [parse_card(c) for c in my_input]
        opp_hand = [parse_card(c) for c in opp_input]

        if len(set(my_hand + opp_hand)) != 4:
            print("중복된 카드가 있습니다.")
            return

        win, tie, loss = simulate_vs(my_hand, opp_hand, trials=10000)
        print(f"승률: {win:.2f}%, 무승부: {tie:.2f}%, 패배: {loss:.2f}%")

    except Exception as e:
        print("입력 오류:", e)

if __name__ == "__main__":
    main()
