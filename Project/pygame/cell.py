import pygame as pg
from random import shuffle

class Cell:

    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.is_start = False
        self.is_end = False
        self.visited = False
        self.rect = None
        self.walls = [True] * 4
        self.choices = [0, 1, 2, 3]
        shuffle(self.choices)
        self.changed = True

    def get_neighbors(self, grid):
        width = len(grid)
        height = len(grid[0])

        # top right left bottom
        self.neighbors = []

        if self.y == 0:
            self.neighbors.append(None)
        else:
            self.neighbors.append(grid[self.x][self.y - 1])
        
        if self.x == width - 1:
            self.neighbors.append(None)
        else:
            self.neighbors.append(grid[self.x + 1][self.y])
        
        if self.x == 0:
            self.neighbors.append(None)
        else:
            self.neighbors.append(grid[self.x - 1][self.y])

        if self.y == height - 1:
            self.neighbors.append(None)
        else:
            self.neighbors.append(grid[self.x][self.y + 1])


    def update(self, stack):
        self.visited = True

        if len(self.choices):
            stack.append(self)
            choice = self.choices.pop()
            n = self.neighbors[choice]
            if n and not n.visited:
                self.changed = True
                n.changed = True
                self.walls[choice] = False
                n.walls[3 - choice] = False
                n.visited = True
                stack.append(n)


    def show(self, surface: pg.surface, size, current, changed_cells):
        x0 = self.x * size[0]
        y0 = self.y * size[1]
        if self.rect == None:
            self.rect = pg.Rect(x0, y0, size[0], size[1])

        if self.changed:
            if self == current:
                color = pg.Color('purple')
            elif self.is_start:
                color = pg.Color('green')
            elif self.is_end:
                color = pg.Color('red')
            elif self.visited:
                color = pg.Color('white')
            else:
                color = pg.Color('gray')

            pg.draw.rect(surface, color, self.rect)
            
            if self.walls[0]:
                pg.draw.line(surface, pg.Color('black'), (x0, y0), (x0 + size[0], y0))
            if self.walls[1]:
                pg.draw.line(surface, pg.Color('black'), (x0 + size[0], y0), (x0 + size[0], y0 + size[1]))
            if self.walls[2]:
                pg.draw.line(surface, pg.Color('black'), (x0, y0), (x0, y0 + size[1]))
            if self.walls[3]:
                pg.draw.line(surface, pg.Color('black'), (x0, y0 + size[1]), (x0 + size[0], y0 + size[1]))

            self.changed = False
            changed_cells.append(self.rect)