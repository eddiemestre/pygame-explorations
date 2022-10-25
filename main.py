# Basic Sprite Movement in Pygame
#
# for more about esper, see https://github.com/benmoran56/esper
# Sprites grabbed randomly from Google here: https://forum.unity.com/attachments/linkedit-png.80767/

import pygame
from components import *
from sprites import SpriteSheet
from player_parse import *
import esper

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60
    

# Main core of the program 
def run():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
    input_list = parse_inputs("player-data.json")
    # parse possible player states and the default state from player-data json
    state_list, current_state = parse_states("player-data.json")

    # debugging for parsing player data
    # print("input_list", input_list)
    # print("state_list", state_list)
    # print("current_state", current_state)

    # parse player animations from sprite sheet and add them to a dict
    animation_dict = parse_animations(state_list, my_spritesheet)

    # create player entity
    player = world.create_entity()

    # initialize and connect player entity components
    world.add_component(player, VelocityComponent()) # determines speed to move sprites
    world.add_component(player, AnimationComponent(animation_dict, current_state)) # determines sprites based on state - > should contain a list of all sprite animations as well as current sprite animation
    world.add_component(player, StateComponent(state_list, current_state)) # determines state based on input
    world.add_component(player, InputComponent(input_list)) # determines correct input based on key presses
    world.add_component(player, RenderComponent(animation_dict[current_state], 200, 200)) # should eventually be replaced by start position for a level

    # TO DO: diagnal player movement


    # Create Processor instances and assign them
    render_processor = RenderProcessor(window=screen)
    movement_processor = MovementProcessor(minx=0, maxx=SCREEN_WIDTH, miny=0, maxy=SCREEN_HEIGHT)

    # add processors to world, order matters
    world.add_processor(InputProcessor())
    world.add_processor(StateProcessor())
    world.add_processor(AnimationProcessor())
    world.add_processor(VelocityProcessor())
    world.add_processor(movement_processor)
    world.add_processor(render_processor)


    # Game loop
    while True:
        # A single call to world.process() will update all Processors
        world.process()
        clock.tick(FPS)


if __name__ == "__main__":
    run()