from random import seed, randint
import time
import numpy as np
from tkinter.constants import W
import turtle as t

N = 4
BOX_SIZE = 120
PADDING  = 5
SIZE = BOX_SIZE * N
EDGE = PADDING * 2

t.setup(SIZE, SIZE)
t.setworldcoordinates(0, 0, SIZE, SIZE)
t.up()
t.speed(0)
t.hideturtle()
t.colormode(255)
screen = t.getscreen()
canvas = screen.getcanvas()
seed(time.time())

mines = np.zeros((N, N), np.int8)
nums  = np.zeros((N, N), np.int8)
flags = np.zeros((N, N), np.int8)

v  = lambda i, j: (i >= 0 and i < N and j >= 0 and j < N)

def init_data():
    for k in range(int(N * N // 5) + randint(0, 2)):
        i = randint(0, N-1)
        j = randint(0, N-1)
        mines[i][j] = 1
    f = lambda i, j: mines[i][j] if v(i, j) else 0
    for i in range(N):
        for j in range(N):
            nums[i][j] = f(i-1,j-1) + f(i-1, j) + f(i-1, j+1) \
                + f(i,j-1) + f(i, j) + f(i, j+1) \
                + f(i+1,j-1) + f(i+1, j) + f(i+1, j+1)


def pos_to_index(x, y, noedge=True):
    x2 = x % BOX_SIZE
    y2 = y % BOX_SIZE
    if noedge and (x2 < EDGE or y2 < EDGE or (BOX_SIZE - x2) < EDGE or (BOX_SIZE - y2) < EDGE):
        return None
    return (int(x // BOX_SIZE), int(y // BOX_SIZE))

def index_to_pos(i, j, center = True):
    x = i * BOX_SIZE
    y = j * BOX_SIZE
    if center:
        x += BOX_SIZE // 2
        y += BOX_SIZE // 2
    
    return (x, y)

def box_goto(i, j, center = True):
    t.up()
    x, y = index_to_pos(i, j, center)
    t.goto(x, y)

def box_color(i, j, clr):
    x, y = index_to_pos(i, j, False)
    box_goto(i, j, False)

    t.down()
    t.width(1)
    t.color(clr, clr)
    t.begin_fill()
    t.begin_poly()
    t.goto(x + BOX_SIZE - EDGE, y)
    t.goto(x + BOX_SIZE - EDGE, y + BOX_SIZE - EDGE)
    t.goto(x , y + BOX_SIZE - EDGE)
    t.goto(x , y + EDGE)
    t.end_poly()
    t.end_fill()
    t.up()

def box_close(i, j):
    return box_color(i, j, (120, 120, 120))

def box_open(i, j):
    return box_color(i, j, (120, 120, 200))

def box_text(i, j, s):
    box_open(i, j)
    x, y = index_to_pos(i, j)

    t.up()
    t.goto(x, y - BOX_SIZE // 3)
    t.down()
    t.color(0, 0, 0)
    t.write(str(s), False, align='center', font=("Arial", 64, "normal"))
    t.up()

def box_flag(i, j):
    box_open(i, j)
    box_goto(i, j)
    t.down()
    t.color(200, 200, 120)
    t.dot(60)
    t.up()

def box_blowup(i, j):
    box_open(i, j)
    box_goto(i, j)
    t.down()
    t.color(250, 120, 120)
    t.dot(60)
    t.up()

def open_boxes(i, j):
    if not v(i, j):
        return

    if flags[i][j]:
        return
    flags[i][j] = 1

    if nums[i][j] == 0:
        box_open(i, j)
        open_boxes(i - 1, j)
        open_boxes(i + 1, j)
        open_boxes(i, j - 1)
        open_boxes(i, j + 1)
    else:
        box_text(i, j, nums[i][j])

def check_it():
    for i in range(N):
        for j in range(N):
            if mines[i][j] == 0 and flags[i][j] == 2:
                return False
            elif mines[i][j] == 1 and flags[i][j] != 2:
                return False
    return True

def game_str(s, clr = 'red'):
    screen.onclick(None)
    screen.onclick(None, 2)
    t.up()
    t.goto(SIZE // 2, SIZE // 2)
    t.color(clr)
    t.down()
    print('$$$', SIZE)
    t.write(str(s), False, align='center', font=("Arial", 60, "normal"))

def game_over():
    game_str('Game Over')

def game_ok():
    game_str('Congratulation!', 'blue')

def lclick(x, y):
    idx = pos_to_index(x, y)
    if not idx:
        return

    i, j = idx

    if flags[i][j]:
        return

    if mines[i][j]:
        box_blowup(i, j)
        game_over()
        return
    
    open_boxes(i, j)


def rclick(x, y):
    idx = pos_to_index(x, y)
    if not idx:
        return
    
    i, j = idx
    if flags[i][j]:
        flags[i][j] = 0
        box_close(i, j)
        return
    
    flags[i][j] = 2
    box_flag(i, j)
    if check_it():
        game_ok()

def init_canvas():
    t.width(EDGE)
    t.color(90, 90, 160)
    for i in range(N+1):
        t.up()
        t.goto(i * BOX_SIZE - PADDING, 0 - PADDING)
        t.down()
        t.goto(i * BOX_SIZE - PADDING, SIZE - PADDING)
        t.up()
        t.goto(0 - PADDING, i * BOX_SIZE - PADDING)
        t.down()
        t.goto(SIZE - PADDING, i * BOX_SIZE - PADDING)
        t.up()

    for i in range(N):
        for j in range(N):
            box_close(i, j)

init_data()
init_canvas()


#screen.register_shape('green.gif')
#t2 = t.Turtle()
#t2.hideturtle()

print(mines, nums, flags)

screen.onclick(lclick)
screen.onclick(rclick, 2)
t.mainloop()
