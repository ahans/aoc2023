from collections import Counter


def hand_rank(hand, p2=False):
    counter = Counter(hand)
    num_jokers = counter["J"] if "J" in counter and p2 else 0
    match sorted(counter.values(), reverse=True):
        case [1, 1, 1, 1, 1]:
            return 1 + num_jokers
        case [2, 1, 1, 1]:
            return 2 + min(num_jokers, 1) * 2
        case [2, 2, 1]:
            return 3 + (min(num_jokers, 1) * (num_jokers + 1))
        case [3, 1, 1]:
            return 4 + (min(num_jokers, 1) * (3 - num_jokers % 2))
        case [3, 2]:
            return 5 + min(num_jokers, 2)
        case [4, 1]:
            return 6 + min(num_jokers, 1)
        case [5]:
            return 7


cards_rank = "".join(reversed("AKQJT98765432"))
cards_rank2 = "".join(reversed("AKQT98765432J"))


def card_rank(card, p2=False):
    if p2:
        return cards_rank2.index(card)
    return cards_rank.index(card)


parts = [[], []]
for line in open("../inputs/07.txt").read().strip().splitlines():
    hand, bid = line.split()
    for i, p2 in enumerate((False, True)):
        parts[i].append((hand_rank(hand, p2=p2), [card_rank(card, p2=p2) for card in hand], bid))

for hands in parts:
    s = 0
    hands.sort()
    print(sum((rank + 1) * int(hand[-1]) for rank, hand in enumerate(hands)))
