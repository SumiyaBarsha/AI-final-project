import random
import time
import numpy as np
from pyamaze2 import maze, agent, COLOR

# Directions
DIRECTIONS = ['U', 'D', 'L', 'R']

# Custom agent class to manage movement and position
class CustomAgent:
    def __init__(self, maze, x=0, y=0):
        self.maze = maze
        self.x = x
        self.y = y

    def moveRight(self):
        if self.x < self.maze.cols:
            self.x += 1

    def moveLeft(self):
        if self.x > 0:
            self.x -= 1

    def moveUp(self):
        if self.y > 0:
            self.y -= 1

    def moveDown(self):
        if self.y < self.maze.rows:
            self.y += 1

    def get_pos(self):
        return self.x, self.y

class Individual:
    def __init__(self, dna=None):
        if dna is None:
            self.dna = self.random_dna()
        else:
            self.dna = dna
        self.fitness = 0

    def random_dna(self):
        return [random.choice(['U', 'D', 'L', 'R']) for _ in range(20)]

    def calc_fitness(self, maze, start, goal):
        agent = CustomAgent(maze, x=start[0], y=start[1])
        for move in self.dna:
            move_agent(agent, move)
        self.fitness = -abs(agent.x - goal[0]) - abs(agent.y - goal[1])

def move_agent(agent, move):
    if move == 'R':
        agent.moveRight()
    elif move == 'L':
        agent.moveLeft()
    elif move == 'U':
        agent.moveUp()
    elif move == 'D':
        agent.moveDown()

class DNA:
    def __init__(self, num):
        self.genes = [random.choice(DIRECTIONS) for _ in range(num)]
        self.fitness = 0

    def get_moves(self):
        return ''.join(self.genes)

    def calc_fitness(self, maze, start, goal):
        agent = CustomAgent(maze, x=start[0], y=start[1])
        for move in self.genes:
            move_agent(agent, move)
        self.fitness = -np.linalg.norm(np.array(agent.get_pos()) - np.array(goal))

    def crossover(self, partner):
        child = DNA(len(self.genes))
        midpoint = random.randint(0, len(self.genes) - 1)
        for i in range(len(self.genes)):
            if i > midpoint:
                child.genes[i] = self.genes[i]
            else:
                child.genes[i] = partner.genes[i]
        return child

    def mutate(self, mutation_rate):
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[i] = random.choice(DIRECTIONS)

class Population:
    def __init__(self, target, mutation_rate, num, maze, start, goal):
        self.population = []
        self.mating_pool = []
        self.generations = 0
        self.finished = False
        self.target = target
        self.mutation_rate = mutation_rate
        self.perfect_score = -1
        self.best = ""
        self.maze = maze
        self.start = start
        self.goal = goal
        
        for _ in range(num):
            self.population.append(DNA(len(self.target)))
        
        self.calc_fitness()

    def calc_fitness(self):
        for individual in self.population:
            individual.calc_fitness(self.maze, self.start, self.goal)

    def natural_selection(self):
        self.mating_pool = []
        max_fitness = max(individual.fitness for individual in self.population)
        
        for individual in self.population:
            fitness = self.map(individual.fitness, -np.linalg.norm(np.array(self.start) - np.array(self.goal)), max_fitness, 0, 1)
            n = int(fitness * 100)
            self.mating_pool.extend([individual] * n)

    def generate(self):
        for i in range(len(self.population)):
            a = random.randint(0, len(self.mating_pool) - 1)
            b = random.randint(0, len(self.mating_pool) - 1)
            partner_a = self.mating_pool[a]
            partner_b = self.mating_pool[b]
            child = partner_a.crossover(partner_b)
            child.mutate(self.mutation_rate)
            self.population[i] = child
        
        self.generations += 1

    def get_best(self):
        return self.best

    def evaluate(self):
        world_record = -np.inf
        index = 0
        for i in range(len(self.population)):
            if self.population[i].fitness > world_record:
                index = i
                world_record = self.population[i].fitness
        
        self.best = self.population[index].get_moves()

    def is_finished(self):
        return self.finished

    def get_generations(self):
        return self.generations

    def get_average_fitness(self):
        total = sum(individual.fitness for individual in self.population)
        return total / len(self.population)

    @staticmethod
    def map(value, left_min, left_max, right_min, right_max):
        left_span = left_max - left_min
        right_span = right_max - right_min
        value_scaled = float(value - left_min) / float(left_span)
        return right_min + (value_scaled * right_span)

def setup():
    global target, popmax, mutation_rate, population, start, goal, maze_obj, agent_obj
    target = " " * 20  # Initial length of the DNA sequence
    popmax = 200
    mutation_rate = 0.01
    maze_obj = maze(20, 20)
    maze_obj.CreateMaze()
    start = (1, 1)
    goal = (20, 20)
    population = Population(target, mutation_rate, popmax, maze_obj, start, goal)
    agent_obj = agent(maze_obj, x=start[0], y=start[1], color=COLOR.cyan, shape='square')

def visualize_moves(best_moves):
    global agent_obj, maze_obj
    agent_pos = list(start)
    moves = {'R': (1, 0), 'L': (-1, 0), 'U': (0, -1), 'D': (0, 1)}

    path = []
    for move in best_moves:
        agent_pos[0] += moves[move][0]
        agent_pos[1] += moves[move][1]
        path.append(tuple(agent_pos))

    maze_obj.tracePath({agent_obj: path}, delay=300)
    time.sleep(1)

def display_info():
    answer = population.get_best()
    statstext = f"Total generations: {population.generations}\n"
    
    print(f"Best moves: {answer}")
    print(statstext)

# Main execution
setup()
population.evaluate()
visualize_moves(population.get_best())
display_info()

# Keep the maze window open
maze_obj.run()
