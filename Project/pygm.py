import pygame
import pygame_menu
from pygame_menu import themes
import const

pygame.init()
w, h = 1000, 600
surface = pygame.display.set_mode((w+200, h))
difficulty_level = 1

def set_difficulty(value, difficulty):
    global difficulty_level
    difficulty_level = difficulty
    print(value)
    print(difficulty)

def start_the_game():
    if difficulty_level == 1:     
        const.set_initial_val(400, 400, 200, cell_size=40)
    elif difficulty_level == 2:     
        const.set_initial_val(700, 500, 600)
    elif difficulty_level == 3:     
        const.set_initial_val(1100, 600, 1100, cell_size=25)

    import maze
    maze.main()

def level_menu():
    mainmenu._open(level)

mainmenu = pygame_menu.Menu('Welcome', w+200, h, theme=themes.THEME_SOLARIZED)
mainmenu.add.button('Play', start_the_game)
mainmenu.add.button('Levels', level_menu)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)

level = pygame_menu.Menu('Select a Difficulty', w+200, h, theme=themes.THEME_BLUE)
level.add.selector('Difficulty:', [('Easy', 1), ('Medium', 2), ('Hard', 3)], onchange=set_difficulty)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if mainmenu.is_enabled():
        mainmenu.update(events)
        mainmenu.draw(surface)

    pygame.display.update()
