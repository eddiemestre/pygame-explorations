import pygame
from sprites import SpriteSheet
import esper
from pytmx.util_pygame import load_pygame
from components import *
from settings import *


def create_map_entities():
    pass

# takes a tmx file and parses the layers into a layers dict with a collection of 
# MapSprites
def load_tiled_data(filename): # map_01.tmx
    tmx_data = load_pygame(filename)

    # types of objects/tiles
    layer_dict = {}

    # loop over all layer names
    layer_names = tmx_data.layernames
    for layer in layer_names:
        layer_dict[layer] = []
    
    # print(layer_dict)

    # floor
    # grab x/y coordinates and surface of tiles
    for x,y,surf in tmx_data.get_layer_by_name("nc_ground").tiles():
        # need to create image, rect, and depth values from this info (and layers info)
        # need to add all tiles to a collection (group) of some kind

        # Create MapSpriteComponent for each layer and add it to the layer dict
        map_sprite = MapSprite((x * TILE_SIZE, y * TILE_SIZE), surf)
        layer_dict['nc_ground'].append(map_sprite) 
        
    # print(layer_dict)

    return layer_dict
