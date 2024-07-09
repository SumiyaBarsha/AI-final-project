from pyamaze2 import maze,agent
m=maze(20,20)
m.CreateMaze()
a=agent(m,footprints=True,color='cyan', shape='square' , )
m.enableArrowKey(a)
m.enableWASD(a)
# m.tracePath({a:m.path})
m.run()