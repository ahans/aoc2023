import sys
import heapq
from collections import namedtuple, defaultdict

grid = [[int(x) for x in line] for line in sys.stdin.read().strip().splitlines()]

H = len(grid)
W = len(grid[0])

State = namedtuple("State", "y x dir num_straight")


def find_path(min_num_straight, max_num_straight):
    q = [(0, State(0, 0, None, 0))]
    seen = set()
    costmap = defaultdict(lambda: sys.maxsize)
    costmap[State(0, 0, None, 0)] = 0

    while q:
        cost, state = heapq.heappop(q)

        if state in seen:
            continue
        seen.add(state)

        if (
            state.y + 1 == H
            and state.x + 1 == W
            and (min_num_straight is None or state.num_straight >= min_num_straight)
        ):
            return costmap[state]

        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (-dy, -dx) == state.dir:
                # going backwards is not allowed
                continue

            ny, nx = state.y + dy, state.x + dx

            if ny < 0 or ny >= H or nx < 0 or nx >= W:
                continue

            if (dy, dx) == state.dir:
                num_straight = state.num_straight + 1
            else:
                num_straight = 1
                if state.dir is not None and min_num_straight is not None and state.num_straight < min_num_straight:
                    continue

            if num_straight > max_num_straight:
                continue
            
            new_cost = cost + grid[ny][nx]
            new_state = State(ny, nx, (dy, dx), num_straight)
            if new_cost < costmap[new_state]:
                costmap[new_state] = new_cost
                heapq.heappush(q, (new_cost, new_state))


print(find_path(None, 3))
print(find_path(4, 10))
