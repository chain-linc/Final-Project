import pygame

def load_spritesheet(filename, tile_width, tile_height):
    spritesheet = pygame.image.load(filename).convert_alpha()
    sheet_width, sheet_height = spritesheet.get_size()
    tiles = []
    for y in range(0, sheet_height, tile_height):
        for x in range(0, sheet_width, tile_width):
            tile = spritesheet.subsurface((x, y, tile_width, tile_height))
            tiles.append(tile)
    return tiles

tiles = load_spritesheet("spritesheet.png", 16, 16)

levels = [
    [
        [3, 0, 0],
        [
            "###*###",
            "#     #",
            "### ###",
            "#     #",
            "# @@@ #",
            "# @@@ #",
            "# @@@ #",
            "#     #",
            "#######",
        ],
    ]
]

for i, level in enumerate(levels):
    levels[i][1] = [list(row) for row in level[1]]

level = levels[0]

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

TILEID_GRASS = 68
TILEID_MOUNTAIN = 69
TILEID_WATER = 70
TILEID_EXPLOSION = 71
TILEID_GOAL = 76
TILEID_PLACEABLE = 77

TILE_MAP = {
    TILE_FLOOR: TILEID_GRASS,
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
            screen.blit(tiles[tile_id], (levelPos[0] + x * 50, levelPos[1] + y * 50))

def draw_ui():
    global uiPlayButtonRect
    # draw play button if number of needed pipes is met
    if drawed_pipes >= level[0]:
        uiPlayButtonRect = pygame.Rect(screenRect.width - 110, 40, 100, 30)
        pygame.draw.rect(screen, (0, 255, 0), uiPlayButtonRect)
        font_surface = font.render("Play", True, (0, 0, 0))
        screen.blit(font_surface, (uiPlayButtonRect.x + (uiPlayButtonRect.width - font_surface.get_width()) // 2, uiPlayButtonRect.y + (uiPlayButtonRect.height - font_surface.get_height()) // 2))

    font_surface = font.render(f"Needed Pipes: {level[0]} - Drawn Pipes: {drawed_pipes}", True, (255, 255, 255))
    screen.blit(font_surface, (screenRect.width - font_surface.get_width() - 10, 10))

def init():
    global screen, clock, screenRect, FPS, font
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    screenRect = screen.get_rect()
    
    pygame.display.set_caption("Pipe Cleaner Bender")
    clock = pygame.time.Clock()
    FPS = 60
    
    font = pygame.font.SysFont(None, 24)

init()
gameState = "editing"

levelPos = (100, 100)
drawed_pipes = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
                        if level[1][levelY][levelX] == TILE_PLACEABLE and level[0] > drawed_pipes:
                            drawed_pipes += 1
                            level[1][levelY][levelX] = TILE_WATER
                        elif level[1][levelY][levelX] == TILE_WATER:
                            drawed_pipes -= 1
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
                
                if gameState == "editing":
                    
                

    screen.fill((0, 0, 0))
    draw_level(level)
    draw_ui()
    pygame.display.flip()

    # E. Cap the frame rate
    clock.tick(FPS)

# 5. Clean exit
pygame.quit()
