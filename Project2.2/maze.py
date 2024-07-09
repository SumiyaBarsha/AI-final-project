import pygame
import random
from collections import deque
from random import randint
import const
from const import WHITE,BLACK,PURPLE,BLUE,OLIVE,FPS
from ga import *
from minimax import minimax


pygame.init()

# Constants
WIDTH, HEIGHT = const.WIDTH, const.HEIGHT
CELL_SIZE = const.CELL_SIZE
PADDING = const.PADDING  
MAX_moves = const.MAX_moves
nrows = HEIGHT // CELL_SIZE
ncols = WIDTH // CELL_SIZE  
nempty = nrows//2


screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
win = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("AMaze GAme")

cat_img = pygame.image.load("cat.png")
fish_img = pygame.image.load("fish.png")
cat_img = pygame.transform.scale(cat_img, (CELL_SIZE - PADDING, CELL_SIZE - PADDING))
fish_img = pygame.transform.scale(fish_img, (CELL_SIZE - PADDING, CELL_SIZE - PADDING))


def update_dimensions(width, height, max_mov, cell_size):
    global WIDTH, HEIGHT, CELL_SIZE, PADDING, nrows, ncols, nempty, MAX_moves
    WIDTH, HEIGHT = width, height
    CELL_SIZE = cell_size
    PADDING = const.PADDING
    MAX_moves = max_mov
    nrows = HEIGHT // CELL_SIZE
    ncols = WIDTH // CELL_SIZE
    nempty = nrows // 2
    
def center_maze_and_buttons():
    global maze_x, maze_y, button_x, button_y
    maze_x = (screen_width - WIDTH) // 2 - 80
    maze_y = (screen_height - HEIGHT) // 2

    button_x = maze_x + WIDTH + 25  # 25 pixels gap from the maze
    button_y = 150

    global level_button_rect, regen_button_rect, show_button_rect, result_button_rect, toggle_footprints_button_rect, ga_button_rect, minimax_button_rect, quit_button_rect
    level_button_rect = pygame.Rect(button_x, button_y + 50, 160, 40)
    regen_button_rect = pygame.Rect(button_x, button_y + 100, 160, 40)
    show_button_rect = pygame.Rect(button_x, button_y + 150, 160, 40)
    result_button_rect = pygame.Rect(button_x, button_y + 200, 160, 40)
    toggle_footprints_button_rect = pygame.Rect(button_x, button_y + 250, 160, 40)
    ga_button_rect = pygame.Rect(button_x, button_y + 300, 160, 40)
    minimax_button_rect = pygame.Rect(button_x, button_y + 350, 160, 40) 
    quit_button_rect = pygame.Rect(button_x, button_y + 400, 160, 40) 
    
update_dimensions(400, 400, 200, 40)
center_maze_and_buttons()

class Cell:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.walls = [True, True, True, True]  # Top Right Bottom Left
        self.visited = False
        self.path_visited = False
        self.part_of_result_path = False

    def draw(self, win, show_footprints):
        x = maze_x + self.c * CELL_SIZE
        y = maze_y + self.r * CELL_SIZE

        if self.visited:
            pygame.draw.rect(win, BLACK, (x + PADDING, y + PADDING, CELL_SIZE - PADDING*2, CELL_SIZE - PADDING*2))

        if show_footprints and self.path_visited:
            pygame.draw.rect(win, PURPLE, (x + PADDING, y + PADDING, CELL_SIZE - PADDING*2, CELL_SIZE - PADDING*2))

        if self.part_of_result_path:
            pygame.draw.rect(win, BLUE, (x + PADDING, y + PADDING, CELL_SIZE - PADDING*2, CELL_SIZE - PADDING*2))

        if self.walls[0]:
            pygame.draw.line(win, WHITE, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls[1]:
            pygame.draw.line(win, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls[2]:
            pygame.draw.line(win, WHITE, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE), 2)
        if self.walls[3]:
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

def random_remove_walls(grid, start, goal, num_walls):
    path = bfs(grid, start, goal)
    if not path:
        return  # No path found

    # Set to keep track of cells already modified to avoid redundant work
    modified_cells = set()

    for _ in range(num_walls):
        # Randomly decide whether to remove walls from the path or the entire grid
        if random.random() < 0.5 and len(path) > 1:
            # Choose a random cell along the path (except the last one)
            idx = random.randint(0, len(path) - 2)
            current = path[idx]
        else:
            # Choose a random cell from the grid
            r = random.randint(0, nrows - 1)
            c = random.randint(0, ncols - 1)
            current = grid[r][c]

        # Ensure we are not modifying the same cell multiple times
        if current in modified_cells:
            continue

        # Mark the cell as modified
        modified_cells.add(current)

        # Remove all walls from the current cell
        for neighbor in current.create_neighbors(grid):
            remove_walls(current, neighbor)

        # Recalculate the path after removing walls to ensure it still leads to the goal
        path = bfs(grid, start, goal)
        if not path:
            break



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

def draw_grid(win, grid, show_footprints):
    for row in grid:
        for cell in row:
            cell.draw(win, show_footprints)

def draw_buttons(win, difficulty_level):
    pygame.draw.rect(win, OLIVE, level_button_rect)
    pygame.draw.rect(win, OLIVE, regen_button_rect)
    pygame.draw.rect(win, OLIVE, show_button_rect)
    pygame.draw.rect(win, OLIVE, result_button_rect)
    pygame.draw.rect(win, OLIVE, toggle_footprints_button_rect)
    pygame.draw.rect(win, OLIVE, ga_button_rect)
    pygame.draw.rect(win, OLIVE, minimax_button_rect)
    pygame.draw.rect(win, OLIVE, quit_button_rect)
    font = pygame.font.Font(None, 36)
    level_text = font.render(f'Level: {difficulty_level}', True, WHITE)
    regen_text = font.render('Regenerate', True, WHITE)
    show_text = font.render('Show Gen', True, WHITE)
    result_text = font.render('Result', True, WHITE)
    toggle_footprints_text = font.render('Footprints', True, WHITE)
    ga_text = font.render('Run GA', True, WHITE)
    minimax_text = font.render('Run MinMax', True, WHITE)
    quit_text = font.render('Quit', True, WHITE)
    win.blit(level_text, (level_button_rect.x + 10, level_button_rect.y + 5))
    win.blit(regen_text, (regen_button_rect.x + 10, regen_button_rect.y + 5))
    win.blit(show_text, (show_button_rect.x + 10, show_button_rect.y + 5))
    win.blit(result_text, (result_button_rect.x + 10, result_button_rect.y + 5))
    win.blit(toggle_footprints_text, (toggle_footprints_button_rect.x + 10, toggle_footprints_button_rect.y + 5))
    win.blit(ga_text, (ga_button_rect.x + 10, ga_button_rect.y + 5))
    win.blit(minimax_text, (minimax_button_rect.x + 10, minimax_button_rect.y + 5))
    win.blit(quit_text, (quit_button_rect.x + 10, quit_button_rect.y + 5))

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


def main():
    clock = pygame.time.Clock()
    difficulty_level = 1
    grid = [[Cell(r, c) for c in range(ncols)] for r in range(nrows)]
    generate_maze(grid)
    nempty = nrows//2
    random_remove_walls(grid, grid[0][0], grid[nrows - 1][ncols - 1], nempty)
    print(nempty)
    current = grid[0][0]
    goal = grid[nrows - 1][ncols - 1]
    stack = []
    generating = False
    show_footprints = True

    ga_running = False
    ga_start_time = 0
    ga_best_fitness = 0
    ga_generations = 0
    ga_best_path = []

    running = True
    while running:
        clock.tick(FPS)
        win.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if level_button_rect.collidepoint(event.pos):
                    difficulty_level = (difficulty_level%3) + 1  # Cycle between 1, 2, 3
                    print("diff", difficulty_level)
                    if difficulty_level == 1:
                        update_dimensions(400, 400, 200, 40)
                    elif difficulty_level == 2:
                        update_dimensions(700, 500, 600, 30)
                    elif difficulty_level == 3:
                        update_dimensions(1100, 600, 1100, 25)

                    
                    grid = [[Cell(r, c) for c in range(ncols)] for r in range(nrows)]
                    generate_maze(grid)
                    center_maze_and_buttons()
                    clock = pygame.time.Clock()   
                    nempty = nrows//2
                    random_remove_walls(grid, grid[0][0], grid[nrows - 1][ncols - 1], nempty)
                    print(nempty)
                    current = grid[0][0]
                    goal = grid[nrows - 1][ncols - 1]
                    stack = []
                    generating = False
                    show_footprints = True
                    ga_running = False
                    ga_start_time = 0
                    ga_best_fitness = 0
                    ga_generations = 0
                    ga_best_path = []

                    running = True
                if regen_button_rect.collidepoint(event.pos):
                    grid = [[Cell(r, c) for c in range(ncols)] for r in range(nrows)]
                    generate_maze(grid) 
                    random_remove_walls(grid, grid[0][0], grid[nrows - 1][ncols - 1], nempty)
                    current = grid[0][0]
                    goal = grid[nrows - 1][ncols - 1]
                    stack = []
                    generating = False
                    ga_running = False
                elif show_button_rect.collidepoint(event.pos):
                    grid = [[Cell(r, c) for c in range(ncols)] for r in range(nrows)]
                    current = grid[0][0]
                    goal = grid[nrows - 1][ncols - 1]
                    stack = []
                    generating = True
                    ga_running = False
                elif result_button_rect.collidepoint(event.pos):
                    path = bfs(grid, grid[0][0], goal)
                    if path:
                        for cell in path:
                            cell.part_of_result_path = True
                    ga_running = False
                elif toggle_footprints_button_rect.collidepoint(event.pos):
                    show_footprints = not show_footprints
                elif ga_button_rect.collidepoint(event.pos):
                    ga_running = True
                    ga_start_time = pygame.time.get_ticks()
                    ga_best_fitness = 0
                    ga_generations = 0
                    ga_best_path = []
                elif minimax_button_rect.collidepoint(event.pos):
                    ga_running = False
                    _, path = minimax(current, goal, grid, 500, True, set())
                    if path:
                        for cell in path:
                            cell.part_of_result_path = True
                        draw_grid(win, grid, show_footprints)
                        pygame.display.flip()
                elif quit_button_rect.collidepoint(event.pos):  
                    running = False

            elif event.type == pygame.KEYDOWN:
                if not generating:
                    if event.key == pygame.K_UP and not current.walls[0]:
                        current.path_visited = True
                        current = grid[current.r - 1][current.c]
                    elif event.key == pygame.K_DOWN and not current.walls[2]:
                        current.path_visited = True
                        current = grid[current.r + 1][current.c]
                    elif event.key == pygame.K_LEFT and not current.walls[3]:
                        current.path_visited = True
                        current = grid[current.r][current.c - 1]
                    elif event.key == pygame.K_RIGHT and not current.walls[1]:
                        current.path_visited = True
                        current = grid[current.r][current.c + 1]

        if generating:
            current, stack = step_maze_generation(grid, stack, current)
            if not stack and all(cell.visited for row in grid for cell in row):
                generating = False

        if ga_running:
            current_time = pygame.time.get_ticks()
            if current_time - ga_start_time >= 1200:
                ga_start_time = current_time
                ga_generations += 1
                best_path = run_genetic_algorithm(grid, grid[0][0], goal, nrows, ncols, pop_size=1000, max_moves=MAX_moves, num_generations=1, mutation_rate=0.01)
                current = grid[0][0]
                for move in best_path:
                    current.path_visited = True
                    if move == 'U' and not current.walls[0] and current.r > 0:
                        current = grid[current.r - 1][current.c]
                    elif move == 'D' and not current.walls[2] and current.r < nrows - 1:
                        current = grid[current.r + 1][current.c]
                    elif move == 'L' and not current.walls[3] and current.c > 0:
                        current = grid[current.r][current.c - 1]
                    elif move == 'R' and not current.walls[1] and current.c < ncols - 1:
                        current = grid[current.r][current.c + 1]
                    if current == goal:
                        break
                fitness = evaluate_individual(grid, best_path, grid[0][0], goal, nrows, ncols)
                if fitness > ga_best_fitness:
                    ga_best_fitness = fitness
                    ga_best_path = best_path
                    if(fitness==1.0):
                        ga_running = False
                print(f"Generation: {ga_generations}, Fitness: {ga_best_fitness}")

        draw_grid(win, grid, show_footprints)
        draw_buttons(win, difficulty_level)
        win.blit(cat_img, (maze_x + current.c * CELL_SIZE + PADDING, maze_y + current.r * CELL_SIZE + PADDING))  # Fixed position
        win.blit(fish_img, (maze_x + goal.c * CELL_SIZE + PADDING, maze_y + goal.r * CELL_SIZE + PADDING))

        pygame.display.flip()

        if current == goal and not generating:
            print("You won!")
            winning_message(win)
            # running = False
            

    
def winning_message(win):
    font = pygame.font.Font(None, 72)
    text = font.render("You Won!!!", True, (0, 255, 0))
    win.blit(text, (maze_x + WIDTH // 2 - text.get_width() // 2, maze_y + HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(2000)  

if __name__ == "__main__":
    main()

