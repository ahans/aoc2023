import sys
from collections import defaultdict


grid = defaultdict(int)
bricks = defaultdict(list)
for id, line in enumerate(sys.stdin.read().strip().splitlines()):
    a, b = line.split("~")
    a = [int(x) for x in a.split(",")]
    b = [int(x) for x in b.split(",")]
    for x in range(a[0], b[0] + 1):
        for y in range(a[1], b[1] + 1):
            for z in range(a[2], b[2] + 1):
                grid[(x, y, z)] = id + 1
                bricks[id + 1].append((x, y, z))


def can_move_down(id):
    for x, y, z in bricks[id]:
        if z == 0 or (grid[(x,y,z - 1)] != 0 and grid[(x, y, z - 1)] != id):
            return False
    return True

def move_down(id):
    coords = bricks[id]
    new_coords = [(x, y, z - 1) for x, y, z in coords]
    for old_pos, new_pos in zip(coords, new_coords):
        grid[old_pos] = 0
        grid[new_pos] = id
    bricks[id] = new_coords 


moved = True
while moved:
    moved = False
    for id in bricks.keys():
        if can_move_down(id):
            move_down(id)
            moved = True

is_supported_by = defaultdict(set)
supports = defaultdict(set)
for id, coords in bricks.items():
    for x, y, z in coords:
        cube_below = grid[(x, y, z - 1)]
        if cube_below != 0 and cube_below != id:
            is_supported_by[id].add(cube_below)
            supports[cube_below].add(id)

non_essential = set()
for id in bricks.keys():
    if id not in supports or all(len(is_supported_by[k]) > 1 for k in supports[id]):
        non_essential.add(id) 
print(len(non_essential))

p2 = 0
for brick_id in bricks.keys():
    if brick_id in non_essential:
        continue
    q = [brick_id]
    disintegrated = set()
    while q:
        cur = q.pop()
        disintegrated.add(cur)
        for supported_brick in supports[cur]:
            if len(is_supported_by[supported_brick] - disintegrated) == 0:
                q.append(supported_brick)

    p2 += len(disintegrated) - 1
print(p2)