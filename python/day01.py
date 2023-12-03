words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

p1 = 0
p2 = 0

for line in open("../inputs/01.txt").readlines():
    first = min(
        (index, i + 1) for i in range(9) if (index := line.find(str(i + 1))) != -1
    )
    last = max(
        (index, i + 1) for i in range(9) if (index := line.rfind(str(i + 1))) != -1
    )
    p1 += 10 * first[1] + last[1]

    first_2 = min(
        [(index, i + 1) for i, w in enumerate(words) if (index := line.find(w)) != -1]
        + [first]
    )
    last_2 = max(
        [(index, i + 1) for i, w in enumerate(words) if (index := line.rfind(w)) != -1]
        + [last]
    )
    p2 += 10 * first_2[1] + last_2[1]

print(p1)
print(p2)
