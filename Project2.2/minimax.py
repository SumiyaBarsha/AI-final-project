# import pygame
# import random
# from collections import deque

# # Initialize Pygame
# pygame.init()

# # Constants
# WIDTH, HEIGHT = 1200, 600
# CELL_SIZE = 30
# PADDING = 2  # Padding to ensure walls are visible
# nrows = HEIGHT // CELL_SIZE
# ncols = (WIDTH - 200) // CELL_SIZE  # Reduce columns to accommodate buttons
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# GREEN = (0, 255, 0)
# OLIVE = (128, 128, 0)
# RED = (255, 0, 0)
# PURPLE = (128, 0, 128)
# BLUE = (0, 0, 255)
# FPS = 30

# # Setup the display
# win = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Maze Solver")

# # Load images
# cat_img = pygame.image.load("G:/AI_project/catto/cat.png")
# burger_img = pygame.image.load("G:/AI_project/catto/burger.png")
# cat_img = pygame.transform.scale(cat_img, (CELL_SIZE - PADDING*2, CELL_SIZE - PADDING*2))
# burger_img = pygame.transform.scale(burger_img, (CELL_SIZE - PADDING*2, CELL_SIZE - PADDING*2))

# # Button rectangles
# regen_button_rect = pygame.Rect(WIDTH - 180, 50, 160, 40)
# show_button_rect = pygame.Rect(WIDTH - 180, 100, 160, 40)
# result_button_rect = pygame.Rect(WIDTH - 180, 150, 160, 40)

# class Cell:
#     def __init__(self, r, c):
#         self.r = r
#         self.c = c
#         self.walls = [True, True, True, True]  # Top Right Bottom Left
#         self.visited = False
#         self.path_visited = False
#         self.part_of_result_path = False

#     def draw(self, win):
#         x = self.c * CELL_SIZE
#         y = self.r * CELL_SIZE

#         if self.visited:
#             pygame.draw.rect(win, BLACK, (x + PADDING, y + PADDING, CELL_SIZE - PADDING*2, CELL_SIZE - PADDING*2))

#         if self.path_visited:
#             pygame.draw.rect(win, PURPLE, (x + PADDING, y + PADDING, CELL_SIZE - PADDING*2, CELL_SIZE - PADDING*2))

#         if self.part_of_result_path:
#             pygame.draw.rect(win, BLUE, (x + PADDING, y + PADDING, CELL_SIZE - PADDING*2, CELL_SIZE - PADDING*2))

#         if self.walls[0]:  # top wall
#             pygame.draw.line(win, WHITE, (x, y), (x + CELL_SIZE, y), 2)
#         if self.walls[1]:  # right wall
#             pygame.draw.line(win, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
#         if self.walls[2]:  # bottom wall
#             pygame.draw.line(win, WHITE, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE), 2)
#         if self.walls[3]:  # left wall
#             pygame.draw.line(win, WHITE, (x, y + CELL_SIZE), (x, y), 2)

#     def create_neighbors(self, grid):
#         neighbors = []
#         if self.r > 0:
#             neighbors.append(grid[self.r - 1][self.c])
#         if self.c < ncols - 1:
#             neighbors.append(grid[self.r][self.c + 1])
#         if self.r < nrows - 1:
#             neighbors.append(grid[self.r + 1][self.c])
#         if self.c > 0:
#             neighbors.append(grid[self.r][self.c - 1])
#         return neighbors

# def remove_walls(current, next):
#     dx = current.c - next.c
#     dy = current.r - next.r
#     if dx == 1:  # Next is left of current
#         current.walls[3] = False
#         next.walls[1] = False
#     elif dx == -1:  # Next is right of current
#         current.walls[1] = False
#         next.walls[3] = False
#     if dy == 1:  # Next is above current
#         current.walls[0] = False
#         next.walls[2] = False
#     elif dy == -1:  # Next is below current
#         current.walls[2] = False
#         next.walls[0] = False

# def generate_maze(grid):
#     stack = []
#     current = grid[0][0]
#     while True:
#         current.visited = True
#         neighbors = [cell for cell in current.create_neighbors(grid) if not cell.visited]
#         if neighbors:
#             next_cell = random.choice(neighbors)
#             stack.append(current)
#             remove_walls(current, next_cell)
#             current = next_cell
#         elif stack:
#             current = stack.pop()
#         else:
#             break

# def step_maze_generation(grid, stack, current):
#     current.visited = True
#     neighbors = [cell for cell in current.create_neighbors(grid) if not cell.visited]
#     if neighbors:
#         next_cell = random.choice(neighbors)
#         stack.append(current)
#         remove_walls(current, next_cell)
#         current = next_cell
#     elif stack:
#         current = stack.pop()
#     return current, stack

# def draw_grid(win, grid, show_footprints):
#     for row in grid:
#         for cell in row:
#             cell.draw(win, show_footprints)

# def draw_buttons(win):
#     pygame.draw.rect(win, OLIVE, regen_button_rect)
#     pygame.draw.rect(win, OLIVE, show_button_rect)
#     pygame.draw.rect(win, OLIVE, result_button_rect)
#     font = pygame.font.Font(None, 36)
#     regen_text = font.render('Regenerate', True, WHITE)
#     show_text = font.render('Show Gen', True, WHITE)
#     result_text = font.render('Result', True, WHITE)
#     win.blit(regen_text, (regen_button_rect.x + 10, regen_button_rect.y + 5))
#     win.blit(show_text, (show_button_rect.x + 10, show_button_rect.y + 5))
#     win.blit(result_text, (result_button_rect.x + 10, result_button_rect.y + 5))

def heuristic(cell, goal):
    # Manhattan distance heuristic
    return abs(cell.r - goal.r) + abs(cell.c - goal.c)

def minimax(cell, goal, grid, depth, minimizingPlayer, visited):
    # print(f"Visiting cell: ({cell.r}, {cell.c}), depth: {depth}")
    if cell == goal:
        return 0,[cell]
    if depth == 0:
        return heuristic(cell, goal), [cell]

    visited.add(cell)
    
    if minimizingPlayer:
        
        minEval = float('inf')
        bestPath = []
        for neighbor in cell.create_neighbors(grid):
            if not neighbor.visited:
                continue
            if neighbor not in visited:
                if (cell.walls[0] == False and neighbor == grid[cell.r-1][cell.c]) or \
                (cell.walls[1] == False and neighbor == grid[cell.r][cell.c+1]) or \
                (cell.walls[2] == False and neighbor == grid[cell.r+1][cell.c]) or \
                (cell.walls[3] == False and neighbor == grid[cell.r][cell.c-1]):
                    eval, path = minimax(neighbor, goal, grid, depth - 1, True, visited)
                    if eval < minEval:
                        minEval = eval
                        bestPath = [cell] + path
        visited.remove(cell)
        # if bestPath:
        #     print(f"Best path so far: {[(c.r, c.c) for c in bestPath]}")
        return minEval, bestPath
    # else:
    #     maxEval = float('-inf')
    #     bestPath = []
    #     for neighbor in cell.create_neighbors(grid):
    #         if not neighbor.visited:
    #             continue
    #         if neighbor not in visited :
    #             if (cell.walls[0] == False and neighbor == grid[cell.r-1][cell.c]) or \
    #                (cell.walls[1] == False and neighbor == grid[cell.r][cell.c+1]) or \
    #                (cell.walls[2] == False and neighbor == grid[cell.r+1][cell.c]) or \
    #                (cell.walls[3] == False and neighbor == grid[cell.r][cell.c-1]):
    #                 eval, path = minimax(neighbor, goal, grid, depth - 1, False, visited)
    #                 if eval > maxEval:
    #                     maxEval = eval
    #                     bestPath = [cell] + path
    #     visited.remove(cell)
    #     return maxEval, bestPath


# def main():
#     clock = pygame.time.Clock()
#     grid = [[Cell(r, c) for c in range(ncols)] for r in range(nrows)]
#     generate_maze(grid)

#     current = grid[0][0]
#     goal = grid[nrows - 1][ncols - 1]
#     stack = []
#     generating = False
#     show_footprints = True

#     running = True
#     while running:
#         clock.tick(FPS)
#         win.fill(BLACK)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if regen_button_rect.collidepoint(event.pos):
#                     grid = [[Cell(r, c) for c in range(ncols)] for r in range(nrows)]
#                     generate_maze(grid)
#                     current = grid[0][0]
#                     goal = grid[nrows - 1][ncols - 1]
#                     stack = []
#                     generating = False
#                 elif show_button_rect.collidepoint(event.pos):
#                     grid = [[Cell(r, c) for c in range(ncols)] for r in range(nrows)]
#                     current = grid[0][0]
#                     goal = grid[nrows - 1][ncols - 1]
#                     stack = []
#                     generating = True
#                 elif result_button_rect.collidepoint(event.pos):
#                     #print("Result button clicked")
#                     _, path = minimax(current, goal, grid, 500, True, set())  # Increase depth limit
#                     if path:
#                         # print("Path found")
#                         # # Print the path to the console
#                         # print("Path:")
#                         # for cell in path:
#                         #     print(f"({cell.r}, {cell.c})")
#                         for cell in path:
#                             cell.part_of_result_path = True
#                         draw_grid(win, grid)
#                         pygame.display.flip()
#                     else:
#                         print("No path found")
#             elif event.type == pygame.KEYDOWN:
#                 if not generating:
#                     if event.key == pygame.K_UP and not current.walls[0]:
#                         current.path_visited = True
#                         current = grid[current.r - 1][current.c]
#                     elif event.key == pygame.K_DOWN and not current.walls[2]:
#                         current.path_visited = True
#                         current = grid[current.r + 1][current.c]
#                     elif event.key == pygame.K_LEFT and not current.walls[3]:
#                         current.path_visited = True
#                         current = grid[current.r][current.c - 1]
#                     elif event.key == pygame.K_RIGHT and not current.walls[1]:
#                         current.path_visited = True
#                         current = grid[current.r][current.c + 1]

#         if generating:
#             current, stack = step_maze_generation(grid, stack, current)
#             if not stack and all(cell.visited for row in grid for cell in row):
#                 generating = False

#         draw_grid(win, grid, show_footprints)
#         draw_buttons(win)
#         win.blit(cat_img, (current.c * CELL_SIZE + PADDING, current.r * CELL_SIZE + PADDING))
#         win.blit(burger_img, (goal.c * CELL_SIZE + PADDING, goal.r * CELL_SIZE + PADDING))

#         pygame.display.flip()

#         if current == goal and not generating:
#             print("You won!")
#             running = False

#     pygame.quit()

# if __name__ == "__main__":
#     main()
