import pygame
import random
from collections import deque
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import time
import numpy as np
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

scoreboard = []

# Constants
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 30
PADDING = 2  # Padding to ensure walls are visible
nrows = HEIGHT // CELL_SIZE
ncols = (WIDTH - 200) // CELL_SIZE  # Reduce columns to accommodate buttons
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
OLIVE = (128, 128, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)
FPS = 30

# Setup the display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver")

# Load images
cat_img = pygame.image.load("G:/AI_project/catto/cat.png")
burger_img = pygame.image.load("G:/AI_project/catto/burger.png")
cat_img = pygame.transform.scale(cat_img, (CELL_SIZE - PADDING*2, CELL_SIZE - PADDING*2))
burger_img = pygame.transform.scale(burger_img, (CELL_SIZE - PADDING*2, CELL_SIZE - PADDING*2))

# Button rectangles
regen_button_rect = pygame.Rect(WIDTH - 180, 50, 160, 40)
show_button_rect = pygame.Rect(WIDTH - 180, 100, 160, 40)
result_button_rect = pygame.Rect(WIDTH - 180, 150, 160, 40)
run_minimax_button_rect = pygame.Rect(WIDTH - 180, 200, 160, 40)

class Cell:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.walls = [True, True, True, True]  # Top Right Bottom Left
        self.visited = False
        self.path_visited = False
        self.part_of_result_path = False

    def draw(self, win):
        x = self.c * CELL_SIZE
        y = self.r * CELL_SIZE

        if self.visited:
            pygame.draw.rect(win, BLACK, (x + PADDING, y + PADDING, CELL_SIZE - PADDING*2, CELL_SIZE - PADDING*2))

        if self.path_visited:
            pygame.draw.rect(win, PURPLE, (x + PADDING, y + PADDING, CELL_SIZE - PADDING*2, CELL_SIZE - PADDING*2))

        if self.part_of_result_path:
            pygame.draw.rect(win, BLUE, (x + PADDING, y + PADDING, CELL_SIZE - PADDING*2, CELL_SIZE - PADDING*2))

        if self.walls[0]: #top wall
            pygame.draw.line(win, WHITE, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls[1]: #right wall
            pygame.draw.line(win, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls[2]: #bottom wall
            pygame.draw.line(win, WHITE, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE), 2)
        if self.walls[3]: #left wall
            pygame.draw.line(win, WHITE, (x, y + CELL_SIZE), (x, y), 2)

    def create_neighbors(self, grid):
        neighbors = []
        if self.r > 0:
            neighbors.append(grid[self.r - 1][self.c])
        if self.c < ncols - 1:
            neighbors.append(grid[self.r][self.c + 1])
        if self.r < nrows - 1:
            neighbors.append(grid[self.r + 1][self.c])
        if self.c > 0:
            neighbors.append(grid[self.r][self.c - 1])
        return neighbors

def remove_walls(current, next):
    dx = current.c - next.c
    dy = current.r - next.r
    if dx == 1:  # Next is left of current
        current.walls[3] = False
        next.walls[1] = False
    elif dx == -1:  # Next is right of current
        current.walls[1] = False
        next.walls[3] = False
    if dy == 1:  # Next is above current
        current.walls[0] = False
        next.walls[2] = False
    elif dy == -1:  # Next is below current
        current.walls[2] = False
        next.walls[0] = False

def generate_maze(grid):
    stack = []
    current = grid[0][0]
    while True:
        current.visited = True
        neighbors = [cell for cell in current.create_neighbors(grid) if not cell.visited]
        if neighbors:
            next_cell = random.choice(neighbors)
            stack.append(current)
            remove_walls(current, next_cell)
            current = next_cell
        elif stack:
            current = stack.pop()
        else:
            break

def step_maze_generation(grid, stack, current):
    current.visited = True
    neighbors = [cell for cell in current.create_neighbors(grid) if not cell.visited]
    if neighbors:
        next_cell = random.choice(neighbors)
        stack.append(current)
        remove_walls(current, next_cell)
        current = next_cell
    elif stack:
        current = stack.pop()
    return current, stack

def draw_grid(win, grid):
    for row in grid:
        for cell in row:
            cell.draw(win)

def draw_buttons(win):
    pygame.draw.rect(win, OLIVE, regen_button_rect)
    pygame.draw.rect(win, OLIVE, show_button_rect)
    pygame.draw.rect(win, OLIVE, result_button_rect)
    pygame.draw.rect(win, OLIVE, run_minimax_button_rect)
    font = pygame.font.Font(None, 36)
    regen_text = font.render('Regenerate', True, WHITE)
    show_text = font.render('Show Gen', True, WHITE)
    result_text = font.render('Result', True, WHITE)
    minimax_text = font.render('Run MinMax', True, WHITE)
    win.blit(regen_text, (regen_button_rect.x + 10, regen_button_rect.y + 5))
    win.blit(show_text, (show_button_rect.x + 10, show_button_rect.y + 5))
    win.blit(result_text, (result_button_rect.x + 10, result_button_rect.y + 5))
    win.blit(minimax_text, (run_minimax_button_rect.x + 10, run_minimax_button_rect.y + 5))

def bfs(grid, start, goal):
    queue = deque([(start, [])])
    visited = set()
    while queue:
        current, path = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]
        if current == goal:
            return path
        neighbors = current.create_neighbors(grid)
        for neighbor in neighbors:
            if not neighbor.visited:
                continue
            if neighbor not in visited:
                if (current.walls[0] == False and neighbor == grid[current.r-1][current.c]) or \
                   (current.walls[1] == False and neighbor == grid[current.r][current.c+1]) or \
                   (current.walls[2] == False and neighbor == grid[current.r+1][current.c]) or \
                   (current.walls[3] == False and neighbor == grid[current.r][current.c-1]):
                    queue.append((neighbor, path))
    return None

# Define fuzzy variables with extended ranges for larger grids
distance_traveled = ctrl.Antecedent(np.arange(0, 5001, 1), 'distance_traveled')
turns_taken = ctrl.Antecedent(np.arange(0, 201, 1), 'turns_taken')
time_spent = ctrl.Antecedent(np.arange(0, 3601, 1), 'time_spent')
score = ctrl.Consequent(np.arange(0, 101, 1), 'score')
distance = ctrl.Antecedent(np.arange(0, 100, 1), 'distance')
open_paths = ctrl.Antecedent(np.arange(0, 4, 1), 'open_paths')
direction = ctrl.Consequent(np.arange(0, 4, 1), 'direction')

# Define extended membership functions for distance traveled
distance_traveled['short'] = fuzz.trapmf(distance_traveled.universe, [0, 0, 1000, 2000])
distance_traveled['medium'] = fuzz.trapmf(distance_traveled.universe, [1000, 2000, 3000, 4000])
distance_traveled['long'] = fuzz.trapmf(distance_traveled.universe, [3000, 4000, 5000, 5000])

# Define extended membership functions for turns taken
turns_taken['few'] = fuzz.trapmf(turns_taken.universe, [0, 0, 50, 100])
turns_taken['average'] = fuzz.trapmf(turns_taken.universe, [50, 100, 150, 200])
turns_taken['many'] = fuzz.trapmf(turns_taken.universe, [150, 200, 200, 200])

# Define extended membership functions for time spent
time_spent['short'] = fuzz.trapmf(time_spent.universe, [0, 0, 600, 1200])
time_spent['average'] = fuzz.trapmf(time_spent.universe, [600, 1200, 1800, 2400])
time_spent['long'] = fuzz.trapmf(time_spent.universe, [1800, 2400, 3600, 3600])

# Define membership functions for score
score['low'] = fuzz.trapmf(score.universe, [0, 0, 25, 50])
score['medium'] = fuzz.trapmf(score.universe, [25, 50, 75, 100])
score['high'] = fuzz.trapmf(score.universe, [50, 75, 100, 100])

# Define membership functions for distance to goal
distance['close'] = fuzz.trimf(distance.universe, [0, 0, 50])
distance['far'] = fuzz.trimf(distance.universe, [0, 50, 100])

# Define membership functions for open paths
open_paths['few'] = fuzz.trimf(open_paths.universe, [0, 0, 2])
open_paths['many'] = fuzz.trimf(open_paths.universe, [1, 3, 3])

# Define membership functions for direction
direction[pygame.K_UP] = fuzz.trimf(direction.universe, [0, 0, 1])
direction[pygame.K_RIGHT] = fuzz.trimf(direction.universe, [1, 1, 2])
direction[pygame.K_DOWN] = fuzz.trimf(direction.universe, [2, 2, 3])
direction[pygame.K_LEFT] = fuzz.trimf(direction.universe, [3, 3, 3])

# Define fuzzy rules
rule1 = ctrl.Rule(distance_traveled['short'] & turns_taken['few'] & time_spent['short'], score['high'])
rule2 = ctrl.Rule(distance_traveled['medium'] & turns_taken['average'] & time_spent['average'], score['medium'])
rule3 = ctrl.Rule(distance_traveled['long'] & turns_taken['many'] & time_spent['long'], score['low'])

# Define fuzzy rules for direction
direction_rule1 = ctrl.Rule(distance['close'] & open_paths['many'], direction[pygame.K_UP])
direction_rule2 = ctrl.Rule(distance['far'] & open_paths['few'], direction[pygame.K_RIGHT])
direction_rule3 = ctrl.Rule(distance['close'] & open_paths['few'], direction[pygame.K_DOWN])
direction_rule4 = ctrl.Rule(distance['far'] & open_paths['many'], direction[pygame.K_LEFT])

# Create control system
score_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
score_sim = ctrl.ControlSystemSimulation(score_ctrl)
direction_ctrl = ctrl.ControlSystem([direction_rule1, direction_rule2, direction_rule3, direction_rule4])
direction_sim = ctrl.ControlSystemSimulation(direction_ctrl)

def calculate_score(distance, turns, time):
    print(f"Inputs - Distance: {distance}, Turns: {turns}, Time: {time}")  # Debug prints for inputs
    score_sim.input['distance_traveled'] = distance
    score_sim.input['turns_taken'] = turns
    score_sim.input['time_spent'] = time

    # Compute score
    try:
        score_sim.compute()
        print(f"Score: {score_sim.output['score']}")
        return score_sim.output['score']
    except ValueError as e:
        print(f"Error: {e}")
        return None


def add_to_scoreboard(name, score):
    scoreboard.append((name, score))
    scoreboard.sort(key=lambda x: x[1], reverse=True)  # Sort by score in descending order

def display_scoreboard():
    print("Scoreboard:")
    for idx, (name, score) in enumerate(scoreboard):
        print(f"{idx + 1}. {name} - Score: {score}")

def fuzzy_next_move(current, goal, direction_sim):
    open_paths = 0
    if current.r > 0 and not current.walls[0]:  # Top
        open_paths += 1
    if current.c < ncols - 1 and not current.walls[1]:  # Right
        open_paths += 1
    if current.r < nrows - 1 and not current.walls[2]:  # Bottom
        open_paths += 1
    if current.c > 0 and not current.walls[3]:  # Left
        open_paths += 1

    distance_to_goal = abs(current.r - goal.r) + abs(current.c - goal.c)
    
    direction_sim.input['distance'] = distance_to_goal
    direction_sim.input['open_paths'] = open_paths
    direction_sim.compute()

    direction_output = direction_sim.output['direction']
    
    if direction_output < 1:
        return 'up'
    elif direction_output < 2:
        return 'right'
    elif direction_output < 3:
        return 'down'
    else:
        return 'left'

def minimax(cell, goal, grid, depth, minimizingPlayer, visited):
    print(f"Visiting cell: ({cell.r}, {cell.c}), depth: {depth}")
    if cell == goal:
        print(f"Goal found at ({cell.r}, {cell.c})")
        return heuristic(cell, goal), [cell]
    if depth == 0:
        return heuristic(cell, goal), [cell]

    visited.add(cell)
    
    if minimizingPlayer:
        minEval = float('inf')
        bestPath = []
        for neighbor in cell.create_neighbors(grid):
            if neighbor not in visited:
                # Check walls between current cell and neighbor
                if (cell.walls[0] == False and neighbor == grid[cell.r-1][cell.c]) or \
                   (cell.walls[1] == False and neighbor == grid[cell.r][cell.c+1]) or \
                   (cell.walls[2] == False and neighbor == grid[cell.r+1][cell.c]) or \
                   (cell.walls[3] == False and neighbor == grid[cell.r][cell.c-1]):
                    eval, path = minimax(neighbor, goal, grid, depth - 1, True, visited)
                    if eval < minEval:
                        minEval = eval
                        bestPath = [cell] + path
        visited.remove(cell)
        return minEval, bestPath
    else:
        maxEval = float('-inf')
        bestPath = []
        for neighbor in cell.create_neighbors(grid):
            if neighbor not in visited:
                if (cell.walls[0] == False and neighbor == grid[cell.r-1][cell.c]) or \
                   (cell.walls[1] == False and neighbor == grid[cell.r][cell.c+1]) or \
                   (cell.walls[2] == False and neighbor == grid[cell.r+1][cell.c]) or \
                   (cell.walls[3] == False and neighbor == grid[cell.r][cell.c-1]):
                    eval, path = minimax(neighbor, goal, grid, depth - 1, False, visited)
                    if eval > maxEval:
                        maxEval = eval
                        bestPath = [cell] + path
        visited.remove(cell)
        return maxEval, bestPath

# Example heuristic function
def heuristic(cell, goal):
    # Manhattan distance heuristic
    return abs(cell.r - goal.r) + abs(cell.c - goal.c)

def main():
    clock = pygame.time.Clock()
    grid = [[Cell(r, c) for c in range(ncols)] for r in range(nrows)]
    generate_maze(grid)

    current = grid[0][0]
    goal = grid[nrows - 1][ncols - 1]
    stack = []
    generating = False
    start_time = time.time()
    turns_taken = 0
    distance_traveled = 0

    running = True
    while running:
        clock.tick(FPS)
        win.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if regen_button_rect.collidepoint(event.pos):
                    grid = [[Cell(r, c) for c in range(ncols)] for r in range(nrows)]
                    generate_maze(grid)
                    current = grid[0][0]
                    goal = grid[nrows - 1][ncols - 1]
                    stack = []
                    generating = False
                    start_time = time.time()
                    turns_taken = 0
                    distance_traveled = 0
                elif show_button_rect.collidepoint(event.pos):
                    grid = [[Cell(r, c) for c in range(ncols)] for r in range(nrows)]
                    current = grid[0][0]
                    goal = grid[nrows - 1][ncols - 1]
                    stack = []
                    generating = True
                    start_time = time.time()
                    turns_taken = 0
                    distance_traveled = 0
                elif result_button_rect.collidepoint(event.pos):
                    path = bfs(grid, grid[0][0], goal)
                    if path:
                        for cell in path:
                            cell.part_of_result_path = True
                        end_time = time.time()
                        total_time = end_time - start_time
                        score = calculate_score(distance_traveled, turns_taken, total_time)
                        print(f"Score: {score}")
                elif run_minimax_button_rect.collidepoint(event.pos):
                    # Run the minimax algorithm
                    eval, path = minimax(current, goal, grid, 10, True, set())
                    if path:
                        for cell in path:
                            cell.part_of_result_path = True
                        print(f"Path found with evaluation: {eval}")
                        print("Path:")
                        for p in path:
                            print(f"({p.r}, {p.c})")
            elif event.type == pygame.KEYDOWN:
                if not generating:
                    prev_r, prev_c = current.r, current.c
                    move = fuzzy_next_move(current, goal, direction_sim)
                    if event.key == pygame.K_UP and not current.walls[0]:
                        current.path_visited = True
                        current = grid[current.r - 1][current.c]
                    elif event.key == pygame.K_RIGHT and not current.walls[1]:
                        current.path_visited = True
                        current = grid[current.r][current.c + 1]
                    elif event.key == pygame.K_DOWN and not current.walls[2]:
                        current.path_visited = True
                        current = grid[current.r + 1][current.c]
                    elif event.key == pygame.K_LEFT and not current.walls[3]:
                        current.path_visited = True
                        current = grid[current.r][current.c - 1]
                    
                    if (prev_r, prev_c) != (current.r, current.c):
                        turns_taken += 1
                        distance_traveled += 1

        if generating:
            current, stack = step_maze_generation(grid, stack, current)
            if not stack and all(cell.visited for row in grid for cell in row):
                generating = False

        draw_grid(win, grid)
        draw_buttons(win)
        win.blit(cat_img, (current.c * CELL_SIZE + PADDING, current.r * CELL_SIZE + PADDING))
        win.blit(burger_img, (goal.c * CELL_SIZE + PADDING, goal.r * CELL_SIZE + PADDING))

        pygame.display.flip()

        if current == goal and not generating:
            end_time = time.time()
            total_time = end_time - start_time
            score = calculate_score(distance_traveled, turns_taken, total_time)
            print(f"Score: {score}")
            add_to_scoreboard("Player 1", score)
            display_scoreboard()
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
