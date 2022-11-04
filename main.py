# Basic Sprite Movement in Pygame
#
# for more about esper, see https://github.com/benmoran56/esper
# Sprites grabbed randomly from Google here: https://forum.unity.com/attachments/linkedit-png.80767/

import pygame
from components import *
from sprites import SpriteSheet
from game_data_parse import *
from sprites import *
from map_parse import *
import esper
from pytmx.util_pygame import load_pygame
from settings import *


    

# Main core of the program 
def run():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Level One')
    clock = pygame.time.Clock()

    # music
    # background_music = pygame.mixer.Sound('...')
    # background_music.set_volume(0.4)
    # background_music.play(loops = -1)

    # Initialize Esper world
    world = esper.World()
  
    #####################
    ###### SPRITES ######
    #####################

    # create player spritesheet (should eventually be automated within json data to grab ALL needed sprites for a level)
    my_spritesheet = SpriteSheet('graphics\Player\link-sprites.png', 'sprite-data.json')
    




    ################
    #### Player ####
    ################
    # parse possible inputs from player-data json
    input_list = parse_inputs("game-data.json")
    # parse possible player states and the default state from player-data json
    state_list, current_state = parse_states("game-data.json")
    # parse depth
    player_depth = parse_render_depth("Player", "game-data.json")

    # debugging for parsing player data
    # print("input_list", input_list)
    # print("state_list", state_list)
    # print("current_state", current_state)

    # parse player animations from sprite sheet and add them to a dict
    animation_dict = parse_animations(state_list, my_spritesheet)

    # create player entity
    player = world.create_entity()

    # initialize and connect player entity components
    world.add_component(player, PositionComponent((400,200))) # determines position, should eventually be determined  by json data
    world.add_component(player, VelocityComponent(2.5)) # determines speed to move sprites
    world.add_component(player, AnimationComponent(animation_dict, animation_dict[current_state], current_state)) # determines sprites based on state - > should contain a list of all sprite animations as well as current sprite animation
    world.add_component(player, StateComponent(state_list, current_state)) # determines state based on input
    world.add_component(player, InputComponent(input_list)) # determines correct input based on key presses
    world.add_component(player, RenderComponent(depth=player_depth)) # sets the sprite list to render currently (potentially redundant with current animation?)
    world.add_component(player, DirectionComponent()) # determines player direction
    # TO DO: diagnal player movement

    # redoing player shell test
    # player_alt = world.create_entity()
    # world.add_component(player_alt, PositionComponent((200,200)))
    # alt_player_surface = [pygame.Surface((64,32))]
    # alt_player_surface[0].fill("green")
    # world.add_component(player_alt, RenderComponent(alt_player_surface))
    # world.add_component(player, )

    
    ###################
    ### Map Loading ###
    ###################
    
    ground = world.create_entity()
    ground_depth = parse_render_depth("Ground", "game-data.json")

    world.add_component(ground, PositionComponent((0,0)))
    world.add_component(ground, RenderComponent(still_image=pygame.image.load('tiled\map_01.png').convert_alpha(), depth=ground_depth))


    # Actual map loading
    parse_map('tiled/map_01.tmx')

    # TO DO: 
    # 1. add rect component or add it as part of the render component? 
    # 2. use these to properly render character to center of screen
    # 3. understand why rects are important

    # map data broken into components:
    # collision component (on some elements)
    # static render component - aka this does not change so after the initial load
    # we do not need to run this process again until a higher order state change (death, location change, etc)
    # animated render component - aka these sprites are animating and need to be 
    # updated every frame (this is the type of component we currently have)
    # some objects may also have an interact component (i.e signs or other objects that display text)
    # at some point need to create a bridge component between static and animated
    # render components so things that are static that then need to animate can



    # Create Processor instances and assign them
    render_processor = RenderProcessor()
    movement_processor = MovementProcessor(minx=0, maxx=SCREEN_WIDTH, miny=0, maxy=SCREEN_HEIGHT)

    # add processors to world, order matters
    world.add_processor(InputProcessor())
    world.add_processor(StateProcessor())
    world.add_processor(DirectionProcessor())
    world.add_processor(AnimationProcessor())
    world.add_processor(movement_processor)
    world.add_processor(render_processor)


    # Game loop
    while True:
        # A single call to world.process() will update all Processors
        world.process()
        clock.tick(FPS)


if __name__ == "__main__":
    run()