import pygame as pg
from cell import Cell

class Maze:
    def __init__(self, size):
        self.width = size[0]
        self.height = size[1]
        self.make_grid()
        self.stack = [self.grid[0][0]]
        self.current = self.stack[0]
        self.finished = False


    def make_grid(self):
        self.grid = []
        for i in range(self.width):
            col = []
            for j in range(self.height):
                cell = Cell((i, j))
                col.append(cell)
            
            self.grid.append(col)
        
        for col in self.grid:
            for cell in col:
                cell.get_neighbors(self.grid)
                
        self.start = self.grid[0][0]
        self.end = self.grid[self.width - 1][self.height - 1]
        self.start.is_start = True
        self.end.is_end = True


    def update(self):
        if len(self.stack):
            self.current.changed = True
            self.current = self.stack.pop()
            self.current.update(self.stack)
        else:
            self.current = None
            self.finished = True


    def show(self, surface):
        width, height = surface.get_size()
        cell_size = (width / self.width, height / self.height)

        changed_cells = [None]
        for col in self.grid:
            for cell in col:
                cell.show(surface, cell_size, self.current, changed_cells)
        
        return changed_cells

    def reset(self):
        self.__init__((self.width, self.height))