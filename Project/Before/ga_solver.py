import numpy as np
from maze_pygame import maze, agent, COLOR

def genetic_algorithm(maze, population_size=100, generations=500, mutation_rate=0.01):
    start = (maze.rows, maze.cols)
    goal = maze._goal

    def generate_individual():
        return np.random.choice(['U', 'D', 'L', 'R'], size=(maze.rows + maze.cols))

    def fitness(individual):
        x, y = start
        for move in individual:
            if move == 'U' and maze.maze_map[(x, y)]['N']:
                x -= 1
            elif move == 'D' and maze.maze_map[(x, y)]['S']:
                x += 1
            elif move == 'L' and maze.maze_map[(x, y)]['W']:
                y -= 1
            elif move == 'R' and maze.maze_map[(x, y)]['E']:
                y += 1
            if (x, y) == goal:
                break
        return -((x - goal[0]) ** 2 + (y - goal[1]) ** 2)  # Negative distance to goal

    def mutate(individual):
        for i in range(len(individual)):
            if np.random.rand() < mutation_rate:
                individual[i] = np.random.choice(['U', 'D', 'L', 'R'])
        return individual

    def crossover(parent1, parent2):
        idx = np.random.randint(0, len(parent1))
        child1 = np.concatenate([parent1[:idx], parent2[idx:]])
        child2 = np.concatenate([parent2[:idx], parent1[idx:]])
        return child1, child2

    population = [generate_individual() for _ in range(population_size)]

    for generation in range(generations):
        population = sorted(population, key=fitness, reverse=True)
        if fitness(population[0]) == 0:
            break
        next_population = population[:population_size // 2]
        for i in range(len(next_population) // 2):
            parent1, parent2 = next_population[i], next_population[-i - 1]
            child1, child2 = crossover(parent1, parent2)
            next_population += [mutate(child1), mutate(child2)]
        population = next_population

    best_individual = population[0]
    path = []
    x, y = start
    for move in best_individual:
        if move == 'U' and maze.maze_map[(x, y)]['N']:
            x -= 1
        elif move == 'D' and maze.maze_map[(x, y)]['S']:
            x += 1
        elif move == 'L' and maze.maze_map[(x, y)]['W']:
            y -= 1
        elif move == 'R' and maze.maze_map[(x, y)]['E']:
            y += 1
        path.append((x, y))
        if (x, y) == goal:
            break
    return path

# Example of usage
maze_instance = maze(10, 10)
maze_instance.CreateMaze(loopPercent=0)
path = genetic_algorithm(maze_instance)
print("Path found by GA:", path)
