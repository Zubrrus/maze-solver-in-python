from graphics import *


def main():
    win = Window(800, 600)

    num_cols = 19
    num_rows = 14
    m1 = Maze(20, 20, num_rows, num_cols, 40, 40, win)
    if m1.solve():
        print("Exit has been found!")
    else:
        print("Exit hasn't been found!")

    win.wait_for_close()

main()