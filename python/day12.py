import sys

from functools import cache


@cache
def count(springs, nums):
    k = (springs, nums)
    if len(nums) == 0:
        return 1 if "#" not in springs else 0

    if nums[0] == 0:
        if len(springs) == 0:
            if len(nums) == 1:
                return 1
            return 0
        else:
            if springs[0] == "#":
                return 0
            else:
                return count(springs[1:], nums[1:])

    # skip leading .
    while len(springs) > 0 and springs[0] == ".":
        springs = springs[1:]

    if len(springs) == 0:
        return 0

    if springs[0] == "?":
        r = count("#" + springs[1:], nums) + count("." + springs[1:], nums)
        return r

    cur_count = nums[0]
    if len(springs) < cur_count:
        r = 0
        return r

    for i, c in enumerate(springs):
        if cur_count == 0:
            if c != "#":
                return count(springs[i + 1 :], nums[1:])
            return 0
        else:
            if c == "#" or c == "?":
                cur_count -= 1
            else:
                return 0

    if cur_count == 0 and len(nums) == 1:
        return 1
    return 0


lines = sys.stdin.read().strip().splitlines()
p1 = 0
p2 = 0
for l in lines:
    springs, nums = l.split()
    nums = [int(x) for x in nums.split(",")]
    p1 += count(springs, tuple(nums))
    p2 += count("?".join([springs] * 5), tuple(5 * nums))


print(p1)
print(p2)
