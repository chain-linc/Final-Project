import pygame
from pygame._sdl2 import Window


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
            "###*###",
            "#     #",
            "### ###",
            "#     #",
            "#  @  #",
            "# @@@ #",
            "# @@@ #",
            "#     #",
            "#######",
        ],
    ]
]

for i, level in enumerate(levels):
    levels[i][1] = [list(row) for row in level[1]]

level_num = 0
level = levels[level_num]

TILE_WALL = "#"
TILE_FLOOR = " "
TILE_GOAL = "*"
TILE_PLACEABLE = "@"
TILE_WATER = "W"

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

TILE_MAP = {
    TILE_FLOOR: TILEID_GRASS,
    TILE_WALL: TILEID_WALL_LEFT_RIGHT,
    TILE_GOAL: TILEID_GOAL,
    TILE_PLACEABLE: TILEID_PLACEABLE,
    TILE_WATER: TILEID_WATER,
}

def draw_level(level):
    for y, row in enumerate(level[1]):
        for x, tile in enumerate(row):
            tile_id = TILE_MAP.get(tile)
            if tile_id is None:
                continue
            screen.blit(tiles[tile_id], (levelPos[0] + x * 16, levelPos[1] + y * 16))

def draw_ui():
    global uiPlayButtonRect
    
    font_surface = font.render(f"Level: {level_num + 1}", False, (255, 255, 255))
    screen.blit(font_surface, (screenRect.width // 2 - font_surface.get_width() // 2, 5))
    
    # draw sheep buttons to drag and drop
    if gameState == "editing":
        for i, tile_id in enumerate([TILEID_SHEEP, TILEID_RAM, TILEID_SHEEP_BUOY]):
            button_rect = pygame.Rect(5 + i * 45, 215, 40, 20)
            pygame.draw.rect(screen, (200, 200, 200), button_rect, border_radius=5)
            screen.blit(tiles[tile_id], (button_rect.x + ((button_rect.width-20) - tiles[tile_id].get_width()) // 2, button_rect.y + (button_rect.height - tiles[tile_id].get_height()) // 2))

            color = (20, 20, 20)
            if level[0][i] - drawed_sheeps <= 0:
                color = (150, 50, 50)

            font_surface = font.render(f"x{level[0][i] - drawed_sheeps}", False, color)
            screen.blit(font_surface, (button_rect.x + button_rect.width - 20, button_rect.centery - font_surface.get_height() // 2))

    # play button
    uiPlayButtonRect = pygame.Rect(screenRect.width - 55, 215, 50, 20)
    pygame.draw.rect(screen, (200, 200, 200), uiPlayButtonRect, border_radius=5)
    font_surface = font.render("Play", False, (20, 100, 20))
    screen.blit(font_surface, (uiPlayButtonRect.x + (uiPlayButtonRect.width - font_surface.get_width()) // 2, uiPlayButtonRect.y + (uiPlayButtonRect.height - font_surface.get_height()) // 2))

    # clear button
    uiClearButtonRect = pygame.Rect(uiPlayButtonRect.left - 55, 215, 50, 20)
    pygame.draw.rect(screen, (200, 200, 200), uiClearButtonRect, border_radius=5)
    font_surface = font.render("Clear", False, (100, 20, 20))
    screen.blit(font_surface, (uiClearButtonRect.x + (uiClearButtonRect.width - font_surface.get_width()) // 2, uiClearButtonRect.y + (uiClearButtonRect.height - font_surface.get_height()) // 2))

def init():
    global screen, actual_screen, actual_screenRect, clock, screenRect, FPS, font, tiles, window
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
    FPS = 60
    
    tiles = load_spritesheet("spritesheet.png", 16, 16)
    font = pygame.font.SysFont(None, 24)

init()
gameState = "editing"

GRASS_COLOR = tiles[TILEID_GRASS].get_at((0, 0))

levelPos = screenRect.midtop[0] - (len(level[1][0]) * 16) // 2, 25
drawed_sheeps = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            actual_screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            actual_screenRect = actual_screen.get_rect()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if uiPlayButtonRect.collidepoint(event.pos):
                    if gameState == "editing":
                        gameState = "playing"
                
                # drag and drop diffent sheep types into placebale spots
                if gameState == "editing":
                    levelY = (event.pos[1] - levelPos[1]) // 50
                    levelX = (event.pos[0] - levelPos[0]) // 50
                    try:
                        if level[1][levelY][levelX] == TILE_PLACEABLE and level[0][0] > drawed_sheeps:
                            drawed_sheeps += 1
                            level[1][levelY][levelX] = TILE_WATER
                        elif level[1][levelY][levelX] == TILE_WATER:
                            drawed_sheeps -= 1
                            level[1][levelY][levelX] = TILE_PLACEABLE
                    except IndexError:
                        pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                
                if gameState == "playing":
                    hitWall = False
                    for y, row in enumerate(level[1]):
                        for x, tile in enumerate(row):
                            if tile == TILE_WATER:
                                if level[1][y-1][x] != TILE_FLOOR:
                                    hitWall = True
                
                # drag and drop sheep mode
                if gameState == "editing":
                    pass
                

    screen.fill(GRASS_COLOR)
    draw_level(level)
    draw_ui()
    
    ratio = min(actual_screenRect.width / screenRect.width, actual_screenRect.height / screenRect.height)
    new_size = (int(screenRect.width * ratio), int(screenRect.height * ratio))
    new_pos = ((actual_screenRect.width - new_size[0]) // 2, (actual_screenRect.height - new_size[1]) // 2)
    actual_screen.blit(pygame.transform.scale(screen, new_size), new_pos)
    
    pygame.display.flip()

    # E. Cap the frame rate
    clock.tick(FPS)

# 5. Clean exit
pygame.quit()
