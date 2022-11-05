import pygame
from sprites import SpriteSheet
import esper
from pytmx.util_pygame import load_pygame
from components import *
from settings import *
import json

# creates entities for map data
def create_map_entities(filename, world):

    layer_dict = load_tiled_data(filename)
    layer_depths = get_layer_depths()
    get_map_images(layer_dict)

    # entity = world.create_entity()
    # world.add_component(entity, RenderComponent(layer_dict['nc_ground'], 1, False))

    # loop through the list of layer_depths
    NUM_LAYERS = len(layer_depths[0])

    for i, map_lists in enumerate(layer_depths):
        for map_layer in map_lists:
            if layer_dict[map_layer]:
                if isinstance(layer_dict[map_layer], list):
                    entity = world.create_entity()
                    world.add_component(entity, RenderComponent(layer_dict[map_layer], i + 1, False))
                else: # images
                    entity = world.create_entity()
                    world.add_component(entity, RenderComponent(still_image=layer_dict[map_layer], depth=i+1))


                # else:
                #     world.add_component(entity, RenderComponent(layer_dict[map_layer], i + 1, True))

    # # create entities from all elements in layer_dict
    # for layer in layer_dict:
    #     if layer_dict[layer]:
    #         entity = world.create_entity()
    #         world.add_component(entity, RenderComponent(layer_dict[layer], layer_depths_dict[layer], False))

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

    # grab x/y coordinates and surface of tiles
    for layer in layer_dict.keys():
        try:
            for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
            # need to create image, rect, and depth values from this info (and layers info)
            # need to add all tiles to a collection (group) of some kind

                # Create MapSpriteComponent for each layer and add it to the layer dict
                map_sprite = GameSprite((x * TILE_SIZE, y * TILE_SIZE), surf)
                layer_dict[layer].append(map_sprite) 
        except AttributeError:
            print(f"{layer} does not have tiles")
        
        # try:
        #     for obj in tmx_data.get_layer_by_name(layer):
        #         pass
        #         # if obj.image:
        #         #     pass
        #         #     # map_sprite = GameSprite((obj.x, obj.y), obj.image)
        #         #     # layer_dict[layer].append(map_sprite)
        #         # else:
        #         #     # obj does not have image
        #         #     print(f"{layer} does not have an image")
        # except AttributeError:
        #     print(f"{layer} is not object or tile layer")

    # print(layer_dict)

    return layer_dict

def get_layer_depths():
    data = None
    try:
        with open(LEVEL_JSON) as f:
            data = json.load(f)
        f.close()
    except FileNotFoundError:
        raise("File does not exist")
    
    # this is a list of lists. Items should be retrieved in order using the index of the list
    # as the layer depth
    json_layers = data["Layer Depths"]["map-01"]

    return json_layers


def get_map_images(layer_dict):
    data = None
    try:
        with open(LEVEL_JSON) as f:
            data = json.load(f)
        f.close()
    except FileNotFoundError:
        raise("File does not exist")
    
    image_sources = data["Image Source"]["map-01"]

    for layer in image_sources:
        layer_dict[layer] = pygame.image.load(image_sources[layer]).convert_alpha()