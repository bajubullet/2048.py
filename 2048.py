import random
import os
import sys, tty, termios

def initialize():
    grid = [0]*16
    # set 2 random cells to value 2
    for i in random.sample(range(16), 2):
        grid[i] += 2
    return [
        grid[i:i+4]
        for i in range(0, 16, 4)
    ]

def render(grid):
    for row in grid:
        print '\t'.join(str(cell) for cell in row)


def get_zero_cells(grid):
    return [
        (i, j)
        for i in range(4)
        for j in range(4)
        if grid[i][j] == 0
    ]

def get_col(grid, col_index):
    return [grid[row][col_index] for row in range(4)]

def set_col(grid, col_index, col_values):
    for row in range(4):
        grid[row][col_index] = col_values[row]
    return grid

def merge(data):
    for i in range(1, 4):
        if data[i] == 0:
            continue
        for j in range(i-1, -1, -1):
            if data[j] != 0:
                if data[j] != data[i]:
                    temp = data[i]
                    data[i] = 0
                    data[j+1] = temp
                else:
                    data[j] = data[j] * 2
                    data[i] = 0
                break
            if j == 0:
                data[j] = data[i]
                data[i] = 0
    return data

def left(grid):
    return [
        merge(row)
        for row in grid
    ]

def right(grid):
    return [
        list(reversed(merge(list(reversed(row)))))
        for row in grid
    ]

def up(grid):
    for col in range(4):
        set_col(grid, col, merge(get_col(grid, col)))
    return grid

def down(grid):
    for col in range(4):
        set_col(grid, col, list(reversed(merge(get_col(list(reversed(grid)), col)))))
    return grid

def add_random(grid):
    zero_cells = get_zero_cells(grid)
    if zero_cells == 0:
        print 'Done'
        exit()
    selcted_cell = random.sample(zero_cells, 1)[0]
    if random.randint(0,9) == 7:
        grid[selcted_cell[0]][selcted_cell[1]] = 4
    else:
        grid[selcted_cell[0]][selcted_cell[1]] = 2
    return grid

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch



def play():
    cmd = ''
    grid = initialize()
    while cmd != 'exit':
        os.system('clear')
        render(grid)
        cmd = getch()
        if cmd == 'a':
            grid = left(grid)
        elif cmd == 'd':
            grid = right(grid)
        elif cmd == 'w':
            grid = up(grid)
        elif cmd == 's':
            grid = down(grid)
        else:
            continue
        grid = add_random(grid)


play()
