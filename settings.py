from game_data_parse import extract_layers


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60
LAYERS = extract_layers("game-data.json")
TILE_SIZE = 32
PLAYER_ANIMATION_SPEED = 0.25
PLAYER_START_POSITION = (400, 200)
LEVEL_JSON = "game-data.json"
NUM_LAYERS = 0
MAP_WIDTH = 40 * 32
MAP_HEIGHT = 35 * 32