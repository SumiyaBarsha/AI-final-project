import pygame
import random, datetime, csv, os
from enum import Enum
from collections import deque
from collections import defaultdict

pygame.init()

class COLOR(Enum):
    dark = ((47, 79, 79), (255, 255, 255))  # darkslategray, white
    light = ((255, 255, 255), (0, 0, 0))  # white, black
    black = ((0, 0, 0), (105, 105, 105))  # black, dim gray
    red = ((205, 0, 0), (255, 99, 71))  # red3, tomato
    cyan = ((0, 238, 238), (0, 139, 139))  # cyan2, cyan4
    green = ((0, 139, 0), (152, 251, 152))  # green4, pale green
    blue = ((0, 191, 255), (0, 104, 139))  # DeepSkyBlue2, DeepSkyBlue4
    yellow = ((255, 255, 0), (255, 255, 0))  # yellow2, yellow2

class agent:
    def __init__(self, parentMaze, x=None, y=None, shape='square', goal=None, footprints=False, color: COLOR = COLOR.blue):
        self._parentMaze = parentMaze
        self.color = color
        if isinstance(color, str):
            if color in COLOR.__members__:
                self.color = COLOR[color]
            else:
                raise ValueError(f'{color} is not a valid COLOR!')
        self.shape = shape
        self._orient = 0
        # Set starting position
        if x is None: x = parentMaze.rows
        if y is None: y = parentMaze.cols
        self.x = x
        self.y = y
        self.footprints = footprints
        self._parentMaze._agents.append(self)
        if goal is None:
            self.goal = self._parentMaze._goal
        else:
            self.goal = goal
        self._body = []
        self.position = (self.x, self.y)
        self.path = []  # Add this to keep track of the path
        self.footprint_toggle = False  # Add this to manage alternating footprints
        self._tracePathList = []

    def draw_footprint(self):
        if self.footprints:
            w = self._parentMaze._cell_width
            x = self.x * w - w
            y = self.y * w - w
            footprint_color = self.color.value[1]
            pygame.draw.rect(self._parentMaze.screen, footprint_color, (y + w / 4, x + w / 4, w / 2, w / 2))

    def moveRight(self):
        if self._parentMaze.maze_map[self.x, self.y]['E']:
            self.draw_footprint()
            self.y = self.y + 1

    def moveLeft(self):
        if self._parentMaze.maze_map[self.x, self.y]['W']:
            self.draw_footprint()
            self.y = self.y - 1

    def moveUp(self):
        if self._parentMaze.maze_map[self.x, self.y]['N']:
            self.draw_footprint()
            self.x = self.x - 1

    def moveDown(self):
        if self._parentMaze.maze_map[self.x, self.y]['S']:
            self.draw_footprint()
            self.x = self.x + 1


    def draw(self):
        w = self._parentMaze._cell_width
        x = self.x * w - w
        y = self.y * w - w
        pygame.draw.rect(self._parentMaze.screen, self.color.value[0], (y, x, w, w))
     
        
    def _tracePathSingle(self, a, p, kill, showMarked, delay):
        '''
        An internal method to help tracePath method for tracing a path by agent.
        '''
        def killAgent(a):
            '''
            if the agent should be killed after it reaches the Goal or completes the path
            '''
            self._parentMaze._agents.remove(a)

        w = self._parentMaze._cell_width
        if ((a.x, a.y) in self._parentMaze.markCells and showMarked):
            x = a.x * w - w
            y = a.y * w - w
            pygame.draw.ellipse(self._parentMaze.screen, self._parentMaze._agents[-1].color.value[0], (y + w/2.5 + w/20, x + w/2.5 + w/20, w/8, w/8))

        if (a.x, a.y) == (a.goal):
            del self._parentMaze._tracePathList[0][0][a]
            if self._parentMaze._tracePathList[0][0] == {}:
                del self._parentMaze._tracePathList[0]
                if len(self._parentMaze._tracePathList) > 0:
                    self.tracePath(self._parentMaze._tracePathList[0][0], kill=self._parentMaze._tracePathList[0][1], delay=self._parentMaze._tracePathList[0][2])
            if kill:
                pygame.time.set_timer(26, 300)
                self._win.after(300, killAgent, a)          
            return

        if (type(p) == dict):
            if(len(p) == 0):
                del self._parentMaze._tracePathList[0][0][a]
                return
            a.x, a.y = p[(a.x, a.y)]
        
        if (type(p) == str):
            if(len(p) == 0):
                del self._parentMaze._tracePathList[0][0][a]
                if self._parentMaze._tracePathList[0][0] == {}:
                    del self._parentMaze._tracePathList[0]
                    if len(self._parentMaze._tracePathList) > 0:
                        self.tracePath(self._parentMaze._tracePathList[0][0], kill=self._parentMaze._tracePathList[0][1], delay=self._parentMaze._tracePathList[0][2])
                if kill:
                    self._win.after(300, killAgent, a)          
                return

            if a.shape == 'square':    
                move = p[0]
                if move == 'E':
                    if a.y + 1 <= self._parentMaze.cols:
                        a.y += 1
                elif move == 'W':
                    if a.y - 1 > 0:
                        a.y -= 1
                elif move == 'N':
                    if a.x - 1 > 0:
                        a.x -= 1
                        a.y = a.y
                elif move == 'S':
                    if a.x + 1 <= self._parentMaze.rows:
                        a.x += 1
                        a.y = a.y
                p = p[1:]

        if (type(p) == list):
            if(len(p) == 0):
                del self._parentMaze._tracePathList[0][0][a]
                if self._parentMaze._tracePathList[0][0] == {}:
                    del self._parentMaze._tracePathList[0]
                    if len(self._parentMaze._tracePathList) > 0:
                        self.tracePath(self._parentMaze._tracePathList[0][0], kill=self._parentMaze._tracePathList[0][1], delay=self._parentMaze._tracePathList[0][2])
                if kill:
                    self._win.after(300, killAgent, a)  
                return
            a.x, a.y = p[0]
            del p[0]

        pygame.time.set_timer(26, delay, True)
        pygame.event.post(pygame.event.Event(26, {'agent': a, 'path': p, 'kill': kill, 'showMarked': showMarked, 'delay': delay}))

        self._parentMaze._win.after(delay, self._tracePathSingle, a, p, kill, showMarked, delay)


    def tracePath(self, d, kill=False, delay=300, showMarked=False):
        '''
        A method to trace path by agent.
        You can provide more than one agent/path details.
        '''
        self._parentMaze._tracePathList.append((d, kill, delay))
        if self._parentMaze._tracePathList[0][0] == d: 
            for a, p in d.items():
                if a.goal != (a.x, a.y) and len(p) != 0:
                    self._tracePathSingle(a, p, kill, showMarked, delay)

        


class maze:
    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.maze_map = {}
        self.grid = []
        self.path = {}
        self._cell_width = 30  # Adjust this value based on your screen size
        self._agents = []
        self.markCells = []
        self._tracePathList = defaultdict(list)

        # Calculate the appropriate window size
        self.width = self.cols * self._cell_width
        self.height = self.rows * self._cell_width

        # Pygame window initialization
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('AMaze Game')
        self.screen.fill(COLOR.dark.value[0])

    @property
    def grid(self):
        return self._grid
    
    def add_path(self, agent, path):
        self._tracePathList[agent] = path

    def get_path(self, agent):
        return self._tracePathList.get(agent, [])

    @grid.setter
    def grid(self, n):
        self._grid = []
        y = 0
        for n in range(self.cols):
            x = 1
            y = 1 + y
            for m in range(self.rows):
                self.grid.append((x, y))
                self.maze_map[x, y] = {'E': 0, 'W': 0, 'N': 0, 'S': 0}
                x = x + 1

    def _Open_East(self, x, y):
        self.maze_map[x, y]['E'] = 1
        if y + 1 <= self.cols:
            self.maze_map[x, y + 1]['W'] = 1

    def _Open_West(self, x, y):
        self.maze_map[x, y]['W'] = 1
        if y - 1 > 0:
            self.maze_map[x, y - 1]['E'] = 1

    def _Open_North(self, x, y):
        self.maze_map[x, y]['N'] = 1
        if x - 1 > 0:
            self.maze_map[x - 1, y]['S'] = 1

    def _Open_South(self, x, y):
        self.maze_map[x, y]['S'] = 1
        if x + 1 <= self.rows:
            self.maze_map[x + 1, y]['N'] = 1

    def CreateMaze(self, x=1, y=1, pattern=None, loopPercent=0, saveMaze=False, loadMaze=None, theme: COLOR = COLOR.dark):
        _stack = []
        _closed = []
        self.theme = theme
        self._goal = (x, y)
        if isinstance(theme, str):
            if theme in COLOR.__members__:
                self.theme = COLOR[theme]
            else:
                raise ValueError(f'{theme} is not a valid theme COLOR!')

        def blockedNeighbours(cell):
            n = []
            for d in self.maze_map[cell].keys():
                if self.maze_map[cell][d] == 0:
                    if d == 'E' and (cell[0], cell[1] + 1) in self.grid:
                        n.append((cell[0], cell[1] + 1))
                    elif d == 'W' and (cell[0], cell[1] - 1) in self.grid:
                        n.append((cell[0], cell[1] - 1))
                    elif d == 'N' and (cell[0] - 1, cell[1]) in self.grid:
                        n.append((cell[0] - 1, cell[1]))
                    elif d == 'S' and (cell[0] + 1, cell[1]) in self.grid:
                        n.append((cell[0] + 1, cell[1]))
            return n

        def removeWallinBetween(cell1, cell2):
            if cell1[0] == cell2[0]:
                if cell1[1] == cell2[1] + 1:
                    self.maze_map[cell1]['W'] = 1
                    self.maze_map[cell2]['E'] = 1
                else:
                    self.maze_map[cell1]['E'] = 1
                    self.maze_map[cell2]['W'] = 1
            else:
                if cell1[0] == cell2[0] + 1:
                    self.maze_map[cell1]['N'] = 1
                    self.maze_map[cell2]['S'] = 1
                else:
                    self.maze_map[cell1]['S'] = 1
                    self.maze_map[cell2]['N'] = 1

        def isCyclic(cell1, cell2):
            ans = False
            if cell1[0] == cell2[0]:
                if cell1[1] > cell2[1]: cell1, cell2 = cell2, cell1
                if self.maze_map[cell1]['S'] == 1 and self.maze_map[cell2]['S'] == 1:
                    if (cell1[0] + 1, cell1[1]) in self.grid and self.maze_map[(cell1[0] + 1, cell1[1])]['E'] == 1:
                        ans = True
                if self.maze_map[cell1]['N'] == 1 and self.maze_map[cell2]['N'] == 1:
                    if (cell1[0] - 1, cell1[1]) in self.grid and self.maze_map[(cell1[0] - 1, cell1[1])]['E'] == 1:
                        ans = True
            else:
                if cell1[0] > cell2[0]: cell1, cell2 = cell2, cell1
                if self.maze_map[cell1]['E'] == 1 and self.maze_map[cell2]['E'] == 1:
                    if (cell1[0], cell1[1] + 1) in self.grid and self.maze_map[(cell1[0], cell1[1] + 1)]['S'] == 1:
                        ans = True
                if self.maze_map[cell1]['W'] == 1 and self.maze_map[cell2]['W'] == 1:
                    if (cell1[0], cell1[1] - 1) in self.grid and self.maze_map[(cell1[0], cell1[1] - 1)]['S'] == 1:
                        ans = True
            return ans

        def BFS(cell):
            frontier = deque()
            frontier.append(cell)
            path = {}
            visited = {(self.rows, self.cols)}
            while len(frontier) > 0:
                cell = frontier.popleft()
                if self.maze_map[cell]['W'] and (cell[0], cell[1] - 1) not in visited:
                    nextCell = (cell[0], cell[1] - 1)
                    path[nextCell] = cell
                    frontier.append(nextCell)
                    visited.add(nextCell)
                if self.maze_map[cell]['S'] and (cell[0] + 1, cell[1]) not in visited:
                    nextCell = (cell[0] + 1, cell[1])
                    path[nextCell] = cell
                    frontier.append(nextCell)
                    visited.add(nextCell)
                if self.maze_map[cell]['E'] and (cell[0], cell[1] + 1) not in visited:
                    nextCell = (cell[0], cell[1] + 1)
                    path[nextCell] = cell
                    frontier.append(nextCell)
                    visited.add(nextCell)
                if self.maze_map[cell]['N'] and (cell[0] - 1, cell[1]) not in visited:
                    nextCell = (cell[0] - 1, cell[1])
                    path[nextCell] = cell
                    frontier.append(nextCell)
                    visited.add(nextCell)
            fwdPath = {}
            cell = self._goal
            while cell != (self.rows, self.cols):
                try:
                    fwdPath[path[cell]] = cell
                    cell = path[cell]
                except:
                    print('Path to goal not found!')
                    return
            return fwdPath

        _stack.append((x, y))
        _closed.append((x, y))
        biasLength = 2
        if pattern is not None and pattern.lower() == 'h':
            biasLength = max(self.cols // 10, 2)
        if pattern is not None and pattern.lower() == 'v':
            biasLength = max(self.rows // 10, 2)
        bias = 0

        while len(_stack) > 0:
            cell = []
            bias += 1
            if (x, y + 1) not in _closed and (x, y + 1) in self.grid:
                cell.append("E")
            if (x, y - 1) not in _closed and (x, y - 1) in self.grid:
                cell.append("W")
            if (x + 1, y) not in _closed and (x + 1, y) in self.grid:
                cell.append("S")
            if (x - 1, y) not in _closed and (x - 1, y) in self.grid:
                cell.append("N")
            if len(cell) > 0:
                if pattern is not None and pattern.lower() == 'h' and bias <= biasLength:
                    if 'E' in cell or 'W' in cell:
                        if 'S' in cell: cell.remove('S')
                        if 'N' in cell: cell.remove('N')
                elif pattern is not None and pattern.lower() == 'v' and bias <= biasLength:
                    if 'N' in cell or 'S' in cell:
                        if 'E' in cell: cell.remove('E')
                        if 'W' in cell: cell.remove('W')
                else:
                    bias = 0
                current_cell = (random.choice(cell))
                if current_cell == "E":
                    self._Open_East(x, y)
                    self.path[x, y + 1] = x, y
                    y = y + 1
                    _closed.append((x, y))
                    _stack.append((x, y))

                elif current_cell == "W":
                    self._Open_West(x, y)
                    self.path[x, y - 1] = x, y
                    y = y - 1
                    _closed.append((x, y))
                    _stack.append((x, y))

                elif current_cell == "N":
                    self._Open_North(x, y)
                    self.path[(x - 1, y)] = x, y
                    x = x - 1
                    _closed.append((x, y))
                    _stack.append((x, y))

                elif current_cell == "S":
                    self._Open_South(x, y)
                    self.path[(x + 1, y)] = x, y
                    x = x + 1
                    _closed.append((x, y))
                    _stack.append((x, y))

            else:
                x, y = _stack.pop()

        if loopPercent != 0:
            x, y = self.rows, self.cols
            pathCells = [(x, y)]
            while x != self.rows or y != self.cols:
                x, y = self.path[(x, y)]
                pathCells.append((x, y))
            notPathCells = [i for i in self.grid if i not in pathCells]
            random.shuffle(pathCells)
            random.shuffle(notPathCells)
            pathLength = len(pathCells)
            notPathLength = len(notPathCells)
            count1, count2 = pathLength / 3 * loopPercent / 100, notPathLength / 3 * loopPercent / 100

            count = 0
            i = 0
            while count < count1:
                if len(blockedNeighbours(pathCells[i])) > 0:
                    cell = random.choice(blockedNeighbours(pathCells[i]))
                    if not isCyclic(cell, pathCells[i]):
                        removeWallinBetween(cell, pathCells[i])
                        count += 1
                    i += 1
                else:
                    i += 1
                if i == len(pathCells):
                    break

            if len(notPathCells) > 0:
                count = 0
                i = 0
                while count < count2:
                    if len(blockedNeighbours(notPathCells[i])) > 0:
                        cell = random.choice(blockedNeighbours(notPathCells[i]))
                        if not isCyclic(cell, notPathCells[i]):
                            removeWallinBetween(cell, notPathCells[i])
                            count += 1
                        i += 1
                    else:
                        i += 1
                    if i == len(notPathCells):
                        break
            self.path = BFS((self.rows, self.cols))
        


    def _drawMaze(self, theme):
        self.screen.fill(theme.value[0])
        w = self._cell_width
        for cell in self.grid:
            x, y = cell
            x = x * w - w
            y = y * w - w
            if self.maze_map[cell]['E'] == False:
                pygame.draw.line(self.screen, theme.value[1], (y + w, x), (y + w, x + w), 2)
            if self.maze_map[cell]['W'] == False:
                pygame.draw.line(self.screen, theme.value[1], (y, x), (y, x + w), 2)
            if self.maze_map[cell]['N'] == False:
                pygame.draw.line(self.screen, theme.value[1], (y, x), (y + w, x), 2)
            if self.maze_map[cell]['S'] == False:
                pygame.draw.line(self.screen, theme.value[1], (y, x + w), (y + w, x + w), 2)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        for a in self._agents:
                            a.moveLeft()
                    elif event.key == pygame.K_RIGHT:
                        for a in self._agents:
                            a.moveRight()
                    elif event.key == pygame.K_UP:
                        for a in self._agents:
                            a.moveUp()
                    elif event.key == pygame.K_DOWN:
                        for a in self._agents:
                            a.moveDown()
            self._drawMaze(self.theme)
            for a in self._agents:
                a.draw()
            pygame.display.flip()
        pygame.quit()
