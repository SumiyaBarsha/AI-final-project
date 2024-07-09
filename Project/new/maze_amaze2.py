from maze_pygame2 import maze, agent, COLOR


# Initialize the maze and create it
m = maze(10, 20)
m.CreateMaze()

# Initialize the agent with footprints, color cyan, and shape arrow
a = agent(m,  footprints=True, color=COLOR.cyan, shape='square')
a.draw()
def run_with_trace_path():
    path = {
        a: [(1, 2), (1, 3), (2, 3), (3, 3), (4, 3), (4, 4)]
    }
    a.tracePath(path, kill=True, delay=300, showMarked=True)
    
run_with_trace_path()
# Run the Pygame loop
m.run()