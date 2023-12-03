lines = open("../inputs/04.txt").readlines()

p1 = 0
counts = {card_id: 1 for card_id in range(len(lines))}
for card_id, card in enumerate(lines):
    winning, own = (
        set((int(x) for x in nums.split())) for nums in card.split(":")[1].split("|")
    )
    matches = len(own & winning)
    if matches:
        p1 += 2 ** (matches - 1)
        for i in range(matches):
            if card_id + i + 1 < len(lines):
                counts[card_id + i + 1] += counts[card_id]

print(p1)
print(sum(counts.values()))
