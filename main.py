import ctypes

import copy
import time
import random
import pygame
from pygame._sdl2 import Window
pygame.mixer.init()

# Tells Windows to treat the app as DPI aware (Fixes blurriness)
try:
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError:
    pass # Non-Windows platforms

def load_spritesheet(filename, tile_width, tile_height):
    spritesheet = pygame.image.load(filename).convert_alpha()
    sheet_width, sheet_height = spritesheet.get_size()
    tiles = []
    for y in range(0, sheet_height, tile_height):
        for x in range(0, sheet_width, tile_width):
            tile = spritesheet.subsurface((x, y, tile_width, tile_height))
            tiles.append(tile)
    return tiles


levels = [
    [
        [3, 0, 0],
        [
            "##*##",
            "#   #",
            "## ##",
            "# @ #",
            "#@@@#",
            "#@@@#",
            "#####",
        ],
    ],
    [
        [3, 0, 0],
        [
            " ####",
            "##  *",
            "#   #",
            "#  ##",
            "# @ #",
            "#@@@#",
            "##@##",
            " ### ",
        ],
    ],
    [
        [4, 0, 0],
        [
            " #####",
            "#*   #",
            "#    #",
            "###  #",
            " #@@ #",
            " #@@@#",
            " ##@##",
            "  ### ",
        ],
    ],
    [
        [4, 0, 0],
        [
            "###### ",
            "#    * ",
            "#   ###",
            "#  @@@#",
            "#  @@@#",
            "## @###",
            " ####  ",
        ],
    ],
    [
        [5, 0, 0],
        [
            "##########  ",
            "#@@@ #   ## ",
            "#@@@      ##",
            "#@@@       #",
            "####   #   #",
            "   ######*##",
        ],
    ],
    [
        [5, 0, 0],
        [
            "   #####   ",
            "####   ### ",
            "#@@@     ##",
            "#@@@      *",
            "#@@@ #   ##",
            "########## ",
        ],
    ],
    [
        [4, 0, 0],
        [
            "     ####",
            "     *  ##",
            "######   #",
            "#@@@@#   #",
            "#@@@     #",
            "####     #",
            "   #######",
        ],
    ],
    [
        [3, 0, 0],
        [
            "####### ",
            "#     *#",
            "# #    #",
            "# # ####",
            "#@@@#   ",
            "#@@@#   ",
            "#####   ",
        ],
    ],
    [
        [1, 2, 0],
        [
            "##*##",
            "#MMM#",
            "## ##",
            "# @ #",
            "#@@@#",
            "#@@@#",
            "#####",
        ],
    ],
    [
        [1, 4, 0],
        [
            " ##*###",
            " #M MM#",
            " #M   #",
            " #MMM #",
            "##    #",
            "#M MMM#",
            "#M MMM#",
            "#@@@###",
            "#@@@#  ",
            "#@@@#  ",
            "#####  ",
        ],
    ],
    [
        [1, 0, 2],
        [
            "##*##",
            "#WWW#",
            "## ##",
            "# @ #",
            "#@@@#",
            "#@@@#",
            "#####",
        ],
    ],
    [
        [1, 0, 2],
        [
            " ##*#   ",
            " # W#   ",
            "## W#   ",
            "#  W#   ",
            "# W#####",
            "# W@ @@#",
            "#  @@@##",
            "####@## ",
            "   ###  ",
        ],
    ],
    [
        [1, 1, 1],
        [
            "##*##",
            "#WWW#",
            "#W M#",
            "# @M#",
            "#@@@#",
            "#@@@#",
            "#####",
        ],
    ],
    [
        [1, 1, 1],
        [
            "######",
            "#    *",
            "# WM###",
            "#     #",
            "###@@ #",
            "  #@@@#",
            "  ##@@#",
            "   ####",
        ],
    ],
    [
        [1, 3, 2],
        [
            "###*###  ",
            "#M# #W#  ",
            "# #MM ###",
            "#     WW#",
            "#WW M   #",
            "### #@# #",
            "  #@@@@@#",
            "  #@###@#",
            "  ### ###",
        ],
    ],
]

TILEID_WALL_RIGHT = 32
TILEID_WALL_LEFT_RIGHT = 33
TILEID_WALL_LEFT = 34
TILEID_WALL_ = 35

TILEID_WALL_RIGHT_DOWN = 40
TILEID_WALL_LEFT_RIGHT_DOWN = 41
TILEID_WALL_LEFT_DOWN = 42
TILEID_WALL_DOWN = 43

TILEID_WALL_UP_RIGHT_DOWN = 48
TILEID_WALL_UP_LEFT_RIGHT_DOWN = 49
TILEID_WALL_UP_LEFT_DOWN = 50
TILEID_WALL_UP_DOWN = 51

TILEID_WALL_UP_RIGHT = 56
TILEID_WALL_UP_LEFT_RIGHT = 57
TILEID_WALL_UP_LEFT = 58
TILEID_WALL_UP = 59

TILEID_SHEEP = 0
TILEID_RAM = 2
TILEID_SHEEP_BUOY = 4

TILEID_OFFSET_LEFT = 0
TILEID_OFFSET_RIGHT = 8
TILEID_OFFSET_UP = 16
TILEID_OFFSET_DOWN = 24
TILEID_OFFSET_ANIMATION = 1
TILEID_OFFSET_WATER = 2

TILEID_GRASS = 36
TILEID_MOUNTAIN = 37
TILEID_WATER = 38
TILEID_EXPLOSION = 39

TILEID_GOAL = 44
TILEID_PLACEABLE = 45
TILEID_LOCK = 46
TILEID_COMPLETED = 47

TILEID_DARKGRASS = 52

TILEID_ARROW_LEFT = 60
TILEID_ARROW_RIGHT = 61
TILEID_ARROW_UP = 62
TILEID_ARROW_DOWN = 63

COLLECTION_ARROW = {TILEID_ARROW_LEFT: "left", TILEID_ARROW_DOWN: "down", TILEID_ARROW_RIGHT: "right", TILEID_ARROW_UP: "up"}
COLLECTION_KEY = {pygame.K_LEFT: "left", pygame.K_DOWN: "down", pygame.K_RIGHT: "right", pygame.K_UP: "up"}
COLLECTION_DIRECTION = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
COLLECTION_DIRECTIONS = {
    (-1, 0): TILEID_OFFSET_LEFT,
    (1, 0): TILEID_OFFSET_RIGHT,
    (0, -1): TILEID_OFFSET_UP,
    (0, 1): TILEID_OFFSET_DOWN
}

TILECOLLECTION_SHEEP = [TILEID_SHEEP, TILEID_RAM, TILEID_SHEEP_BUOY]

TILEMASK_MOUNTAIN = 64
TILEMASK_WATER = 128

# UP_LEFT_RIGHT_DOWN
TILECOLLECTION_WALL = {
    "[0, 0, 0, 0]": TILEID_WALL_,
    "[0, 0, 0, 1]": TILEID_WALL_DOWN,
    "[0, 0, 1, 0]": TILEID_WALL_RIGHT,
    "[0, 0, 1, 1]": TILEID_WALL_RIGHT_DOWN,
    "[0, 1, 0, 0]": TILEID_WALL_LEFT,
    "[0, 1, 0, 1]": TILEID_WALL_LEFT_DOWN,
    "[0, 1, 1, 0]": TILEID_WALL_LEFT_RIGHT,
    "[0, 1, 1, 1]": TILEID_WALL_LEFT_RIGHT_DOWN,
    "[1, 0, 0, 0]": TILEID_WALL_UP,
    "[1, 0, 0, 1]": TILEID_WALL_UP_DOWN,
    "[1, 0, 1, 0]": TILEID_WALL_UP_RIGHT,
    "[1, 0, 1, 1]": TILEID_WALL_UP_RIGHT_DOWN,
    "[1, 1, 0, 0]": TILEID_WALL_UP_LEFT,
    "[1, 1, 0, 1]": TILEID_WALL_UP_LEFT_DOWN,
    "[1, 1, 1, 0]": TILEID_WALL_UP_LEFT_RIGHT,
    "[1, 1, 1, 1]": TILEID_WALL_UP_LEFT_RIGHT_DOWN,
} 
TILE_MAP = {
    " ": TILEID_GRASS,
    "#": TILEID_WALL_LEFT_RIGHT,
    "*": TILEID_GOAL,
    "@": TILEID_PLACEABLE,
    "M": TILEID_MOUNTAIN,
    "W": TILEID_WATER,
}

CLICKABLE_COLOR = (20, 180, 20)
UNCLICKABLE_COLOR = (180, 20, 20)
PRESSED_COLOR = (160, 160, 160)
UNPRESSED_COLOR = (200, 200, 200)
HOVER_COLOR_OFFSET = (-10, -10, -10)
DOWNPRESS_COLOR_OFFSET = (-25, -25, -25)

HELP_TEXT = {
    "intro": [
        "Just click on the screen to start!"
    ],
#                                                |||||
    "levels": [
        "Press a level to begin!",
        "After you complete a level, a green",
        "checkmark will appear on it,",
        "and the next level will be unlocked.",
        "A lock symbol will appear on locked",
        "levels."
    ],
#                                                |||||
    "editing": [
        "Press a sheep button to enable that",
        "type of sheep. The button will become",
        "darker after you enable it.",
        "Press on a 'ghost' sheep to place your",
        "selected sheep. Press on it again to",
        "remove it. The number on the sheep",
        "button represents how many more you",
        "can place of that type of sheep.",
        "Press Clear to clear all the sheep.",
        "The Play button will become green and",
        "pressable when: You place all the sheep",
        "or there are no more 'ghost' sheep left."
    ],
#                                                |||||
    "playing": [
        "Use arrow keys or arrow buttons to",
        "mave all of the sheep in that direction.",
        "Regular sheep can only move on grass.",
        "Mountain sheep (the ones with the horns)",
        "can only move on grass+mountains.",
        "Lifevest sheep (the ones with the life",
        "preservers) can only move on",
        "grass+water.",
        "Guide at least one sheep to the staff to",
        "win!",
        "Press the Stop button to edit the",
        "formation again.",
    ],
#                                                |||||
    "win": [
        "You win! Congratulations!",
        "You may have unlocked a new level!",
        "Also the game will save your progress",
        "automatically when you close the",
        "application."
    ]
}

for i, j in enumerate(levels):
    levels[i][1] = [list(row) for row in j[1]]

for i, j in enumerate(levels):
    for y, row in enumerate(j[1]):
        for x, tile in enumerate(row):
            levels[i][1][y][x] = TILE_MAP[tile]

for i, j in enumerate(levels):
    for y, row in enumerate(j[1]):
        for x, tile in enumerate(row):
            if levels[i][1][y][x] in TILECOLLECTION_WALL.values():
                possible_walls = [0, 0, 0, 0]
                for j in range(4):
                    # UP_LEFT_RIGHT_DOWN
                    x_offset, y_offset = [(0, -1), (-1, 0), (1, 0), (0, 1)][j]
                    index = (x + x_offset, y + y_offset)
                    if index[0] == -1 or index[1] == -1:
                        continue
                    
                    try:
                        wall = levels[i][1][index[1]][index[0]]
                    except IndexError: pass
                    else:
                        if wall in TILECOLLECTION_WALL.values():
                            possible_walls[j] = 1

                levels[i][1][y][x] = TILECOLLECTION_WALL[str(possible_walls)]

level_num = 0

SHEEP_SOUNDS = [
    pygame.mixer.Sound("assets/sheep1.mp3"),
    pygame.mixer.Sound("assets/sheep2.mp3"),
    pygame.mixer.Sound("assets/sheep3.mp3")
]

WIN_SOUND = pygame.mixer.Sound("assets/win.mp3")
CLICK_SOUND = pygame.mixer.Sound("assets/click.mp3")
IMPACT_SOUND = pygame.mixer.Sound("assets/impact.mp3")
IMPACT_SOUND.set_volume(2)
music_queue = []

level_interface_buttons = []
for i in range(15):
    w = 40
    h = 40
    x = i % 5
    y = i // 5
    x = (x * (w+20)) + w // 2
    y = (y * (h+20)) + 60
    level_interface_buttons.append((pygame.Rect(x, y, w, h), i + 1))

unlocked_levels = 1

def save_savestate():
    with open("savestate.txt", "w") as f:
        f.write(str(unlocked_levels))

def load_savestate():
    global unlocked_levels
    try:
        with open("savestate.txt", "r") as f:
            unlocked_levels = int(f.read())
    except (FileNotFoundError, ValueError):
        save_savestate()

def play_sheep_sound(sheep_number):
    for i in range(sheep_number):
        sound = random.choice(SHEEP_SOUNDS)
        sound.set_volume(0.25 / sheep_number)
        music_queue.append((sound, time.time() + (random.randint(0, 200)) / 1000))

def play_click_sound():
    CLICK_SOUND.play()

def play_impact_sound():
    IMPACT_SOUND.play()

def play_win_sound():
    WIN_SOUND.play()

def get_sheep_type(tile_id):
    sheep_type = (tile_id % 8) // 2
    if sheep_type == 3:
        sheep_type = 2
    return sheep_type

def button_color(rect, base_color):
    color = base_color
    if rect.collidepoint(mouse_pos):
        color = (color[0] + HOVER_COLOR_OFFSET[0], color[1] + HOVER_COLOR_OFFSET[1], color[2] + HOVER_COLOR_OFFSET[2])
        if mouse_down:
            color = (color[0] + DOWNPRESS_COLOR_OFFSET[0], color[1] + DOWNPRESS_COLOR_OFFSET[1], color[2] + DOWNPRESS_COLOR_OFFSET[2])
    return color

def check_playable(level):
    placeable_count = 0
    for row in level[1]:
        for tile in row:
            if tile == TILEID_PLACEABLE:
                placeable_count += 1
    if placeable_count == 0 or sum(drawed_sheeps) == sum(level[0]):
        return True
    return False

def draw_checkerboard_grass():
    offset = ((levelPos[0] % 16) - 16,
              (levelPos[1] % 16) - 16)
    for y in range(0, 256, 16):
        for x in range(0, 376, 16):
            lightgrass = (((y // 16) % 2) == ((x // 16) % 2))
            if not lightgrass:
                screen.blit(tiles[TILEID_DARKGRASS], (x + offset[0], y + offset[1]))

def draw_level(level):
    for y, row in enumerate(level[1]):
        for x, tile in enumerate(row):
            pos = (levelPos[0] + x * 16, levelPos[1] + y * 16)
            water_offset = 0
            
            tile_mask = tile // 64
            if tile_mask == 1:
                screen.blit(tiles[TILEID_MOUNTAIN], pos)
            if tile_mask == 2:
                screen.blit(tiles[TILEID_WATER], pos)
                water_offset = TILEID_OFFSET_WATER
            
            tile %= 64
            
            if tile == TILEID_GRASS:
                continue
            
            hop_offset = 0
            if 0 <= tile <= 31:
                if sheep_hop_animation > time.time():
                    hop_offset = TILEID_OFFSET_ANIMATION
            
                hop_offset = round(time.time() * 3) % 2
            else:
                water_offset = 0
            
            screen.blit(tiles[tile + hop_offset + water_offset], pos)

def draw_help_button():
    color = button_color(help_button, (255, 255, 255))
    font_surface = font.render("?", False, (0, 0, 0))
    pygame.draw.rect(screen, color, help_button, border_radius=5)
    screen.blit(font_surface, (help_button.centerx - font_surface.get_width() // 2, help_button.centery - font_surface.get_height() // 2))

def draw_ui():
    font_surface = font.render(f"Level: {level_num + 1}", False, (255, 255, 255))
    screen.blit(font_surface, (screenRect.width // 2 - font_surface.get_width() // 2, 5))
    
    # draw sheep buttons to drag and drop
    if gameState == "editing":
        for i, tile_id in enumerate(TILECOLLECTION_SHEEP):
            color = UNPRESSED_COLOR
            if sheep_button_pressed == i:
                color = PRESSED_COLOR
            color = button_color(sheep_buttons[i], color)
            
            pygame.draw.rect(screen, color, sheep_buttons[i], border_radius=5)
            screen.blit(tiles[tile_id], (sheep_buttons[i].x + ((sheep_buttons[i].width-20) - tiles[tile_id].get_width()) // 2, sheep_buttons[i].y + (sheep_buttons[i].height - tiles[tile_id].get_height()) // 2))

            color = CLICKABLE_COLOR
            if level[0][i] - drawed_sheeps[i] <= 0:
                color = UNCLICKABLE_COLOR
            
            if sheep_button_pressed == i:
                color = (max(color[0] + DOWNPRESS_COLOR_OFFSET[0], 0), 
                         max(color[1] + DOWNPRESS_COLOR_OFFSET[1], 0), 
                         max(color[2] + DOWNPRESS_COLOR_OFFSET[2], 0))

            font_surface = font.render(f"x{level[0][i] - drawed_sheeps[i]}", False, color)
            screen.blit(font_surface, (sheep_buttons[i].x + sheep_buttons[i].width - 20, sheep_buttons[i].centery - font_surface.get_height() // 2))

        # clear button
        color = button_color(clear_button, UNPRESSED_COLOR)
        pygame.draw.rect(screen, color, clear_button, border_radius=5)
        font_surface = font.render("Clear", False, CLICKABLE_COLOR)
        screen.blit(font_surface, (clear_button.x + (clear_button.width - font_surface.get_width()) // 2, clear_button.y + (clear_button.height - font_surface.get_height()) // 2))

    elif gameState == "playing":
        # arrow buttons
        for i, button in enumerate(arrow_buttons):
            color = button_color(button, UNPRESSED_COLOR)
            pygame.draw.rect(screen, color, button, border_radius=5)
            surface = tiles[list(COLLECTION_ARROW.keys())[i]]
            screen.blit(surface, (button.x + (button.width - surface.get_width()) // 2, button.y + (button.height - surface.get_height()) // 2))

    # exit button
    color = button_color(exit_button, UNPRESSED_COLOR)
    pygame.draw.rect(screen, color, exit_button, border_radius=5)
    font_surface = font.render("Exit", False, CLICKABLE_COLOR)
    screen.blit(font_surface, (exit_button.x + (exit_button.width - font_surface.get_width()) // 2, exit_button.y + (exit_button.height - font_surface.get_height()) // 2))

    # play button
    color = button_color(play_button, UNPRESSED_COLOR)
    pygame.draw.rect(screen, color, play_button, border_radius=5)
    color = UNCLICKABLE_COLOR
    if check_playable(level):
        color = CLICKABLE_COLOR
    text = "Play"
    if gameState == "playing":
        text = "Stop"
    font_surface = font.render(text, False, color)
    screen.blit(font_surface, (play_button.x + (play_button.width - font_surface.get_width()) // 2, play_button.y + (play_button.height - font_surface.get_height()) // 2))

def init():
    global screen, actual_screen, actual_screenRect, clock, screenRect, FPS, font, help_font, tiles, window
    global sheep_buttons, sheep_button_pressed, clear_button, play_button, exit_button, help_button, arrow_buttons
    pygame.init()
    screen = pygame.Surface((320, 240))
    actual_screen = pygame.display.set_mode((320, 240), pygame.RESIZABLE)
    screenRect = screen.get_rect()
    actual_screenRect = actual_screen.get_rect()
    
    # Maximise Window
    window = Window.from_display_module()
    window.maximize()
    
    pygame.display.set_caption("The Good Shepherd: Guiding His Sheep")
    clock = pygame.time.Clock()
    FPS = 30
    
    load_savestate()
    tiles = load_spritesheet("assets/spritesheet.png", 16, 16)
    font = pygame.font.SysFont(None, 24)
    
    sheep_buttons = []
    for button in range(3):
        sheep_buttons.append(pygame.Rect(5 + button * 45, 215, 40, 20))
    sheep_button_pressed = -1
    
    help_button = pygame.Rect(screenRect.right - 25, 5, 20, 20)
    
    exit_button = pygame.Rect(screenRect.right - 55, 215, 50, 20)
    play_button = pygame.Rect(exit_button.left - 55, 215, 50, 20)
    clear_button = pygame.Rect(play_button.left - 55, 215, 50, 20)
    
    arrow_buttons = []
    for button in range(3):
        arrow_buttons.append(pygame.Rect(5 + button * 25, 215, 20, 20))
    arrow_buttons.append(pygame.Rect(30, 190, 20, 20))

init()
gameState = "intro"

GRASS_COLOR = tiles[TILEID_GRASS].get_at((0, 0))

explosion_animations = []

intro_sheep = []
for i in range(20):
    intro_sheep.append([random.randint(0, screenRect.width), random.randint(0, screenRect.height), random.choice(TILECOLLECTION_SHEEP)])

sheep_hop_animation = 0

levelPos = [0, 0]

mouse_down = False
mouse_pos = (0, 0)
ratio = 1
new_size = (1, 1)
new_pos = (0, 0)

running = True
while running:
    move_direction = None
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_savestate()
            running = False
        if event.type == pygame.VIDEORESIZE:
            actual_screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            actual_screenRect = actual_screen.get_rect()
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            pos = (pos[0] - new_pos[0], pos[1] - new_pos[1])
            pos = (pos[0] / ratio, pos[1] / ratio)
            mouse_pos = pos
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            pos = (pos[0] - new_pos[0], pos[1] - new_pos[1])
            pos = (pos[0] / ratio, pos[1] / ratio)
            if event.button == 1:
                mouse_down = True
                
                if help_button.collidepoint(pos):
                    play_click_sound()
                    if gameState == "help":
                        gameState = helpGameState
                    else:
                        helpGameState = gameState
                        gameState = "help"
                elif gameState in ("intro", "win"):
                    if 0 < pos[0] < screenRect.width and 0 < pos[1] < screenRect.height:
                        play_click_sound()
                        gameState = "levels"
                elif gameState == "levels":
                    for rect, level_index in level_interface_buttons:
                        if rect.collidepoint(pos) and (level_index <= unlocked_levels and level_index <= len(levels)):
                            play_click_sound()
                            level_num = level_index - 1
                            level = copy.deepcopy(levels[level_num])
                            levelPos = screenRect.midtop[0] - (len(levels[level_num][1][0]) * 16) // 2, 25
                            drawed_sheeps = [0, 0, 0]
                            sheep_button_pressed = -1
                            gameState = "editing"
                elif gameState in ("playing", "editing"):
                    if play_button.collidepoint(pos):
                        play_click_sound()
                        if gameState == "editing" and check_playable(level):
                            edit_level = copy.deepcopy(level)
                            for y, row in enumerate(level[1]):
                                for x, tile in enumerate(row):
                                    if tile == TILEID_PLACEABLE:
                                        level[1][y][x] = TILEID_GRASS
                            gameState = "playing"
                            play_sheep_sound(sum(drawed_sheeps))
                        elif gameState == "playing":
                            level = copy.deepcopy(edit_level)
                            gameState = "editing"
                    if exit_button.collidepoint(pos):
                        play_click_sound()
                        levelPos = [0, 0]
                        gameState = "levels"
                
                if gameState == "editing":
                    if clear_button.collidepoint(pos):
                        play_click_sound()
                        if gameState == "editing":
                            level = copy.deepcopy(levels[level_num])
                            drawed_sheeps = [0, 0, 0]
                            sheep_button_pressed = -1
                    
                    # click on different sheep types into placeable spots
                    levelY = int((pos[1] - levelPos[1]) // 16)
                    levelX = int((pos[0] - levelPos[0]) // 16)
                    try:
                        try_remove = True
                        if sheep_button_pressed != -1:
                            if level[1][levelY][levelX] == TILEID_PLACEABLE and level[0][sheep_button_pressed] > drawed_sheeps[sheep_button_pressed]:
                                play_click_sound()
                                try_remove = False
                                drawed_sheeps[sheep_button_pressed] += 1
                                level[1][levelY][levelX] = TILECOLLECTION_SHEEP[sheep_button_pressed]
                        if try_remove and level[1][levelY][levelX] in TILECOLLECTION_SHEEP:
                            play_click_sound()
                            drawed_sheeps[get_sheep_type(level[1][levelY][levelX])] -= 1
                            level[1][levelY][levelX] = TILEID_PLACEABLE
                    except IndexError:
                        pass
                    
                    for sheep_button in sheep_buttons:
                        if sheep_button.collidepoint(pos):
                            play_click_sound()
                            index = sheep_buttons.index(sheep_button)
                            if sheep_button_pressed == index:
                                sheep_button_pressed = -1
                            else:
                                sheep_button_pressed = index
                elif gameState == "playing":
                    for i, rect in enumerate(arrow_buttons):
                        if rect.collidepoint(pos):
                            move_direction = list(COLLECTION_ARROW.values())[i]

        if event.type == pygame.KEYDOWN:
            if gameState == "playing":
                if event.key in COLLECTION_KEY:
                    move_direction = COLLECTION_KEY[event.key]

    if move_direction:
        offset = COLLECTION_DIRECTION[move_direction]
        
        play_sheep_sound(sum(drawed_sheeps))
        sheep_hop_animation = time.time() + 0.4
        
        hit_goal = False
        explosions = []
        sheep_to_move = []

        for y, row in enumerate(level[1]):
            for x, tile in enumerate(row):
                tile_unmasked = tile % 64
                tile_mask = (tile // 64) 
                if 0 <= tile_unmasked <= 31:
                    target_x, target_y = x + offset[0], y + offset[1]
                    sheep_type = get_sheep_type(tile_unmasked)
                    target_mask = 0
                    
                    if 0 <= target_y < len(level[1]) and 0 <= target_x < len(level[1][0]):
                        target_tile = level[1][target_y][target_x]
                        target_tile_mask = target_tile // 64
                        
                        if target_tile == TILEID_GOAL:
                            hit_goal = True
                        elif sheep_type == 1 and (target_tile == TILEID_MOUNTAIN or target_tile_mask == 1):
                            target_mask = 1
                        elif sheep_type == 2 and (target_tile == TILEID_WATER or target_tile_mask == 2):
                            target_mask = 2
                        elif (target_tile != TILEID_GRASS and 32 <= target_tile):
                            explosions.append((time.time(), (target_x, target_y)))
                    else:
                        print("out of range", target_x, target_y)
                    sheep_to_move.append((x, y, sheep_type, tile_mask, target_mask))

        if explosions:
            play_impact_sound()
            for x, y, sheep_type, mask, target_mask in sheep_to_move:
                level[1][y][x] = TILECOLLECTION_SHEEP[sheep_type] + COLLECTION_DIRECTIONS[offset] + (mask * 64)
            explosion_animations.extend(explosions)
        else:
            if hit_goal:
                explosion_animations = []
                music_queue = []
                pygame.mixer.stop()
                play_win_sound()
                unlocked_levels = max(unlocked_levels, level_num + 2)
                levelPos = [0, 0]
                gameState = "win"
            
            copy_level_layer = [row[:] for row in level[1]]
            
            for x, y, sheep_type, mask, target_mask in sheep_to_move:
                if mask == 0:
                    copy_level_layer[y][x] = TILEID_GRASS
                elif mask == 1:
                    copy_level_layer[y][x] = TILEID_MOUNTAIN
                elif mask == 2:
                    copy_level_layer[y][x] = TILEID_WATER
            
            for x, y, sheep_type, mask, target_mask in sheep_to_move:
                new_x, new_y = x + offset[0], y + offset[1]
                
                copy_level_layer[new_y][new_x] = TILECOLLECTION_SHEEP[sheep_type] + COLLECTION_DIRECTIONS[offset] + (target_mask * 64)
            
            level[1] = copy_level_layer
    
    for music in music_queue:
        if time.time() >= music[1]:
            music[0].play()
            music_queue.remove(music)
    

    screen.fill(GRASS_COLOR)
    draw_checkerboard_grass()
    
    if gameState in ("playing", "editing"):
        draw_level(level)
        draw_ui()
    elif gameState == "levels":
        font_surface = font.render("The Good Shepherd: Guiding His Sheep", False, (255, 255, 255))
        pos = (screenRect.width // 2 - font_surface.get_width() // 2, 2)
        screen.blit(font_surface, pos)
        
        font_surface = font.render(f"More Levels Probably Not Coming...", False, (255, 255, 255))
        pos = (screenRect.width // 2 - font_surface.get_width() // 2, pos[1] + font_surface.get_height() + 3)
        screen.blit(font_surface, pos)
        
        font_surface = font.render(f"There are currently {len(levels)} levels availible", False, (255, 255, 255))
        pos = (screenRect.width // 2 - font_surface.get_width() // 2, pos[1] + font_surface.get_height() + 3)
        screen.blit(font_surface, pos)
        
        for rect, level_index in level_interface_buttons:
            color = button_color(rect, (255, 255, 255))
            pygame.draw.rect(screen, color, rect, border_radius=5)
            font_surface = font.render(str(level_index), False, CLICKABLE_COLOR)
            screen.blit(font_surface, (rect.x + (rect.width - font_surface.get_width()) // 2, rect.y + (rect.height - font_surface.get_height()) // 2))
            if unlocked_levels < level_index or len(levels) < level_index:
                scaled_lock = pygame.transform.scale(tiles[TILEID_LOCK], (rect.width - 10, rect.height - 10))
                screen.blit(scaled_lock, (rect.centerx - scaled_lock.get_width() // 2, rect.centery - scaled_lock.get_height() // 2))
            elif level_index < unlocked_levels:
                scaled_check = pygame.transform.scale(tiles[TILEID_COMPLETED], (rect.width - 10, rect.height - 10))
                screen.blit(scaled_check, (rect.centerx - scaled_check.get_width() // 2, rect.centery - scaled_check.get_height() // 2))
            
    elif gameState == "win":
        font_surface = font.render(f"You Win Level {level_num + 1}", False, (255, 255, 255))
        screen.blit(font_surface, (screenRect.width // 2 - font_surface.get_width() // 2, screenRect.height // 2 - font_surface.get_height() // 2))
        font_surface = font.render("Click to Continue", False, (255, 255, 255))
        screen.blit(font_surface, (screenRect.width // 2 - font_surface.get_width() // 2, screenRect.height // 2 - font_surface.get_height() // 2 + 20))
    elif gameState == "intro":
        for sheep in intro_sheep:
            sheep[0] -= 1
            if sheep[0] < -16:
                sheep[0] = screenRect.width
                sheep[1] = random.randint(0, screenRect.height)
                sheep[2] = random.choice(TILECOLLECTION_SHEEP)
            screen.blit(tiles[sheep[2]], (sheep[0], sheep[1]))
        
        title_font_surface = font.render("The Good Shepherd: Guiding His Sheep", False, (255, 255, 255))
        pos = (screenRect.width // 2 - title_font_surface.get_width() // 2, 50)
        screen.blit(title_font_surface, pos)
        
        font_surface = font.render("Click to Start", False, (255, 255, 255))
        pos = (screenRect.width // 2 - font_surface.get_width() // 2, pos[1] + title_font_surface.get_height() + 5)
        screen.blit(font_surface, pos)
        
        
        font_surface = font.render("for help in any menu or screen", False, (255, 255, 255))
        pos = (screenRect.width // 2 - font_surface.get_width() // 2, screenRect.height - font_surface.get_height() - 5)
        screen.blit(font_surface, pos)
        
        help_font_surface = font.render("Press the ? in the top right", False, (255, 255, 255))
        pos = (screenRect.width // 2 - help_font_surface.get_width() // 2, pos[1] - font_surface.get_height() - 5)
        screen.blit(help_font_surface, pos)
        
    
    elif gameState == "help":
        text = HELP_TEXT[helpGameState]
        y = 5
        for line in text:
            font_surface = font.render(line, False, (255, 255, 255))
            pos = (5, y)
            screen.blit(font_surface, pos)
            
            y += font_surface.get_height() + 3
    
    draw_help_button()
    
    if gameState == "playing":
        for explosion in explosion_animations:
            if time.time() - explosion[0] < 0.5:
                screen.blit(tiles[TILEID_EXPLOSION], (levelPos[0] + explosion[1][0] * 16, levelPos[1] + explosion[1][1] * 16))
            else:
                explosion_animations.remove(explosion)

    ratio = min(actual_screenRect.width / screenRect.width, actual_screenRect.height / screenRect.height)
    new_size = (int(screenRect.width * ratio), int(screenRect.height * ratio))
    new_pos = ((actual_screenRect.width - new_size[0]) // 2, (actual_screenRect.height - new_size[1]) // 2)
    actual_screen.blit(pygame.transform.scale(screen, new_size), new_pos)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
