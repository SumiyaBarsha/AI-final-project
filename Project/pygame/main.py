# PyGame template.
 
# Import standard modules.
import argparse
import sys
 
# Import non-standard modules.
import pygame as pg
from pygame.locals import *

# Import local modules
from maze import Maze

def update(dt, maze):
  """
  Update game. Called once per frame.
  dt is the amount of time passed since last frame.
  If you want to have constant apparent movement no matter your framerate,
  what you can do is something like
  
  x += v * dt
  
  and this will scale your velocity based on time. Extend as necessary."""
  
  # Go through events that are passed to the script by the window.
  for event in pg.event.get():
    # We need to handle these events. Initially the only one you'll want to care
    # about is the QUIT event, because if you don't handle it, your game will crash
    # whenever someone tries to exit.
    if event.type == QUIT:
      pg.quit() # Opposite of pg.init
      sys.exit(0) # Not including this line crashes the script on Windows. Possibly
      # on other operating systems too, but I don't know for sure.
    # Handle other events as you wish.
    if event.type == KEYDOWN:
      if event.key == ord(' ') or event.key == ord('r'):
        maze.reset()
      elif event.key == ord('q'):
        pg.quit()
        sys.exit(0)

  maze.update()
 
def draw(screen, maze: Maze):
  """
  Draw things to the window. Called once per frame.
  """
  # screen.fill(pg.Color('black')) # Fill the screen with black.
  
  # Redraw screen here
  changed_cells = maze.show(screen)
  
  # Flip the display so that the things we drew actually show up.
  pg.display.update(changed_cells)
 
def runpg(args):
  # Initialise pg.
  pg.init()
  
  # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
  fps = 60.0
  fpsClock = pg.time.Clock()
  
  # Set up the window.
  window_width, window_height = [int(x) for x in args.window.split("x")]
  flags = DOUBLEBUF

  screen = pg.display.set_mode((window_width, window_height), flags)
  screen.set_alpha(None)
  pg.display.set_caption("Mazing")
  
  # screen is the surface representing the window.
  # pg surfaces can be thought of as screen sections that you can draw onto.
  # You can also draw surfaces onto other surfaces, rotate surfaces, and transform surfaces.
  
  # Set up the maze
  grid_width, grid_height = [int(x) for x in args.geometry.split("x")]
  #maze = Maze((grid_width, grid_height))
  maze = Maze((20, 20))

  # Main game loop.
  dt = 1/fps # dt is the time since last frame.
  # for i in range(7):
  while True: # Loop forever!
    update(dt, maze) # You can update/draw here, I've just moved the code for neatness.
    if args.animate:
      draw(screen, maze)
      dt = fpsClock.tick(fps)
    elif maze.finished:
      if args.file:
        # TODO: add file export
        pass
      else:
        draw(screen, maze)
      
      if args.profile:
        pg.quit()
        sys.exit(0)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Create a maze.')
  parser.add_argument('-g', '--geometry', metavar='WxH', type=str, default="50x50",
                      help='geometry of grid')
  parser.add_argument('-w', '--window', metavar='WxH', type=str, default="600x600",
                      help='windows size')
  parser.add_argument('-A', '--no-animate', dest='animate', action='store_false', default=True,
                      help='hide maze progress')
  parser.add_argument('-f', '--file', type=str, nargs=1, default=None,
                      help='write result to file') 
  parser.add_argument('-p', '--profile', action='store_true', default=False,
                      help='quit after generation (debugging)')
  args = parser.parse_args()

  runpg(args)
