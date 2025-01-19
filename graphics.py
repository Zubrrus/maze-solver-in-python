from tkinter import Tk, BOTH, Canvas
import time
import random


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.__running = False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p_1, p_2):
        self.p_1 = p_1
        self.p_2 = p_2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.p_1.x, self.p_1.y, 
            self.p_2.x, self.p_2.y, 
            fill=fill_color, width=2
        )


class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        fill_color = {True: "black", False: "white"}
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win.draw_line(
            Line(
                Point(self._x1, self._y1),
                Point(self._x1, self._y2),
            ), 
            fill_color[self.has_left_wall]
        )
        self._win.draw_line(
            Line(
                Point(self._x2, self._y1),
                Point(self._x2, self._y2),
            ), 
            fill_color[self.has_right_wall]
        )
        self._win.draw_line(
            Line(
                Point(self._x1, self._y1),
                Point(self._x2, self._y1),
            ), 
            fill_color[self.has_top_wall]
        )
        self._win.draw_line(
            Line(
                Point(self._x1, self._y2),
                Point(self._x2, self._y2),
            ), 
            fill_color[self.has_bottom_wall]
        )

    def draw_move(self, to_cell, undo=False):
        if not undo:
            fill_color = "red"
        else:
            fill_color = "gray"
        
        self._win.draw_line(
                Line(
                    Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2),
                    Point((to_cell._x1 + to_cell._x2) / 2, (to_cell._y1 + to_cell._y2) / 2),
                ),
                fill_color
        )

    
class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None, 
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)
            
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r()
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        if self._win:
            self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        if self._win:
            self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i=0, j=0):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))
            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
            self._break_walls_r(next_index[0], next_index[1])
        
    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                    self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if (i == self._num_cols - 1) and (j == self._num_rows - 1):
            return True
        next_index_list = []
        if (i > 0) and (not self._cells[i][j].has_left_wall) and (not self._cells[i - 1][j].visited):
            next_index_list.append((i - 1, j))
        if (i < self._num_cols - 1) and (not self._cells[i][j].has_right_wall) and (not self._cells[i + 1][j].visited):
            next_index_list.append((i + 1, j))
        if (j > 0) and (not self._cells[i][j].has_top_wall) and (not self._cells[i][j - 1].visited):
            next_index_list.append((i, j - 1))
        if (j < self._num_rows - 1) and (not self._cells[i][j].has_bottom_wall) and (not self._cells[i][j + 1].visited):
            next_index_list.append((i, j + 1))
        for next_index in next_index_list:
            self._cells[i][j].draw_move(self._cells[next_index[0]][next_index[1]])
            if self._solve_r(next_index[0], next_index[1]):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[next_index[0]][next_index[1]], True)
        return False
        
