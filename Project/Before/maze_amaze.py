from maze_pygame import maze, agent, COLOR


# Initialize the maze and create it
m = maze(10, 20)
m.CreateMaze()

# Initialize the agent with footprints, color cyan, and shape arrow
a = agent(m,  footprints=True, color=COLOR.cyan, shape='square')
a.tracePath()
a.draw()

# Run the Pygame loop
m.run()