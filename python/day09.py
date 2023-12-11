import sys
import numpy as np

lines = [[int(x) for x in line.split()] for line in sys.stdin.read().strip().splitlines()]

for p2 in (False, True):
    s = 0
    for line in lines:
        nums = np.array(line)
        if p2:
            nums = np.flip(nums)
        while np.count_nonzero(nums) != 0:
            s += nums[-1]
            nums = nums[1:] - nums[:-1]
    print(s)
