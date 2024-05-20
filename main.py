import math
import casioplot
# from msvcrt import getch

print("LOADING...")

WIDTH = 128
RAYS = 32
HEIGHT = 63

# WIDTH = 21
# HEIGHT = 7

TILE_SIZE = 1.4
FOV = math.pi / 6
RENDER_DISTANCE = 18
RAYCAST_PERCISION = 0.135

SHADES = "█▓▒░"

# SHADES = "#$=."
SHADES_LEN = len(SHADES)

level = ["11111",
         "11.11",
         "1...1",
         "11..1",
         "11111"]

player_pos = (2.5 * TILE_SIZE, 2.5 * TILE_SIZE)
player_rot = 0
bar_heights = [0 for i in range(WIDTH)]

def addPos(t1, t2):
    return tuple(map(lambda i, j: i + j, t1, t2))
def multPos(t1, v):
    return (t1[0] * v, t1[1] * v)

def collision(pos):
    grid_pos = (math.floor(pos[0] / TILE_SIZE),
                math.floor(pos[1] / TILE_SIZE))

    return level[grid_pos[1]][grid_pos[0]] != "."

def getShade(distance, max_distance):
    if distance > max_distance: return " "
    return SHADES[math.floor(distance / max_distance * SHADES_LEN)]

def raycast(_from, direction, distance = 12):
    hit_distance = 0
    pos = _from
    real_direction = multPos(direction, RAYCAST_PERCISION)
    
    for i in range(math.floor(distance / RAYCAST_PERCISION)):
        if collision(pos):
            return hit_distance
        hit_distance += RAYCAST_PERCISION
        pos = addPos(pos, real_direction)
    return -1

def update():
    global player_pos
    global player_rot
    forward = (math.cos(player_rot), math.sin(player_rot))
    back = multPos(forward, -1)
    right = (math.cos(player_rot + math.pi / 2), math.sin(player_rot + math.pi / 2))
    left = multPos(right, -1)
    
    for i in range(RAYS):
        theta = player_rot - FOV + (FOV / RAYS) * i
        raycast_distance = raycast(player_pos, (math.cos(theta), math.sin(theta)), RENDER_DISTANCE)
        bar_heights[i] = 0

        if raycast_distance == 0:
            bar_heights[i] = HEIGHT
        elif raycast_distance != -1:
            bar_heights[i] = HEIGHT / raycast_distance

    # =============================================================
    # for h in range(HEIGHT):
    #     distance_from_center = abs(HEIGHT / 2 - h)
    #     for w in range(WIDTH):
    #         cur = bar_heights[w]
    #         if distance_from_center <= cur and cur != 0: print(getShade(HEIGHT / cur, RENDER_DISTANCE), end = "")
    #         else: # render empty
    #             print(" ", end = "")
    #     print()

    # # wait for input
    # key = getch()

    # if key == b'w': player_pos = addPos(player_pos, forward)
    # elif key == b's': player_pos = addPos(player_pos, back)
    # elif key == b'a': player_rot -= math.pi / 8
    # elif key == b'd': player_rot += math.pi / 8

    # =============================================================

    middle = int(HEIGHT / 2)
    bar_width = int(WIDTH / RAYS)

    casioplot.clear_screen()
    for i in range(RAYS):
        cur = math.floor(bar_heights[i])
        
        # if cur > 0:
        #     casioplot.set_pixel(i, middle + int(cur / 2) + 1)
        #     casioplot.set_pixel(i, middle - int(cur / 2) - 1)
        # else: casioplot.set_pixel(i, middle)


        for hehe in range(bar_width):
            casioplot.set_pixel(i * bar_width + hehe, middle)
            for j in range(int(cur / 2)):
                casioplot.set_pixel(i * bar_width + hehe, middle + j + 1)
                casioplot.set_pixel(i * bar_width + hehe, middle - j - 1)
    casioplot.draw_string(2, 2, "Raycasting Engine DEMO")
    casioplot.show_screen()
    
    player_rot += 0.1

    # key = input()

    # if key == "8": player_pos = addPos(player_pos, forward)
    # elif key == "2": player_pos = addPos(player_pos, back)
    # elif key == "4": player_rot -= math.pi / 6
    # elif key == "6": player_rot += math.pi / 6

while True:
    update()
    

