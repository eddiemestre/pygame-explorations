# sprite component
# velocity
# location component
# name component
# health component
# physical damage component
# render component


# Movement system
#   gravity

# Weather System - integrated with the movement system
#   wind
#   rain
#   snow, etc

# Input System

# Audio System

from inspect import walktree
import pygame
import esper
from settings import *

# Components
class VelocityComponent:
    def __init__(self, speed=4):
        self.speed = speed

# direction component
class DirectionComponent:
    def __init__(self, x=0, y=0):
        self.direction = pygame.math.Vector2(x, y)

class PositionComponent:
    def __init__(self, pos):
        self.position = pygame.math.Vector2(pos[0], pos[1])

class RenderComponent:
    def __init__(self, still_image=None, depth=4, single_image=True):
        self.image = still_image # sprite(s) to render. Initialized to none
        self.depth = depth
        self.rect = None
        self.single_image = single_image
        if still_image: # if true, this is a still image, so self.rect should be (0,0)
            self.rect = self.image.get_rect()

# For entities that need to render multiple tiles at once
# this will typically be used with Map tile groups/layers
class MultiSpriteRenderComponent:
    def __init__(self, sprite_list, depth):
        self.sprite_list = sprite_list
        self.depth = depth

class MapSprite:
    def __init__(self, pos, surf):
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class AnimationComponent:
    def __init__(self, anim_dict, default_animation, animation_name):
        self.animation_dict = anim_dict # stores lists of sprite frames
        assert(isinstance(default_animation, list))
        self.curr_animation = default_animation # a list
        assert(isinstance(animation_name, str))
        self.animation_name = animation_name # a string
        self.animation_frame = 0 # current animation (sprite) frame


class StateComponent:
    def __init__(self, state_options, default_state):
        assert(isinstance(state_options, list))
        # self.entity_states = {} # dictionary of currently active states
        # self.curr_state = None
        # self.state_queue = []
        self.prev_state = None
        # set all states to False except the default state
        # for option in state_options:
        #     self.entity_states[option] = False
        # self.entity_states[default_state] = True
        self.curr_state = default_state


class InputComponent: # do we want two inputs possible at same time? aka walking?
    def __init__(self, input_options):
        assert(isinstance(input_options, list))
        # self.inputs = {} # list of possible inputs this is unnecessary
        self.curr_input = None
        self.input_queue = [] # gives us the order of all current keys being pressed
        self.prev_input = None
        # for option in input_options:
        #     self.inputs[option] = False


class StateProcessor(esper.Processor):
    def __init__(self):
        self.same = False

    def process(self):
        # loops through entities with state components and updates
        # their states according to either input updates or 
        # AI updates

        # in direction processor we first check that state is move, if it is
        # then we update direction vector based on the movement. If current
        # state isn't move, we don't do anything. (or later, we check if 
        # the current state interferes with movement by looping through a list
        # in json data of states that interrupt movement (like attacking or 
        # sometimes taking damage))

        # current state will always reflect the most current input or action of a character.
        # it is possible for a character to have multiple states (walk-left and walk-right means we are walking
        # diagnally), but only the latest input will be reflected. High level checks are done to see if character
        # state includes "walk" or "idle"


        # handle updates from InputComponent
        for ent, (input, state) in self.world.get_components(InputComponent, StateComponent):
            # if last state added to state queue is not the same as the current input and we do have input
            # then update the current and previous state variables
            if state.curr_state != input.curr_input and input.curr_input:
                state.prev_state = state.curr_state
                state.curr_state = input.curr_input

            # if there is no current input but there is a prev_input check conditions
            elif not input.curr_input and input.prev_input:
                # state.entity_states[input.prev_input] = False

                # set idle states here
                if "walk" in input.prev_input:
                    state.prev_state = state.curr_state
                    if input.prev_input == "walk-left":
                        state.curr_state = 'idle-left'
                    elif input.prev_input == 'walk-right':
                        state.curr_state = 'idle-right'
                    elif input.prev_input == 'walk-up':
                        state.curr_state = 'idle-up'
                    elif input.prev_input == 'walk-down':
                        state.curr_state = 'idle-down'

            # print("cur state", state.curr_state)

        # handle updates from Computer info (AI movement, attacking, etc)
        for ent, state in self.world.get_components(StateComponent):
            pass

# should only belong to moveable entities (probably especially the player)
class InputProcessor(esper.Processor):
    def __init__(self):
        pass


    def process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            for ent, input in self.world.get_component(InputComponent):
                # if key is pressed, append that value to the input queue
                # and set the curr_input to that input
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        input.input_queue.append("walk-left")
                        input.curr_input = "walk-left"
                    elif event.key == pygame.K_RIGHT:
                        input.input_queue.append('walk-right')
                        input.curr_input = 'walk-right'
                    elif event.key == pygame.K_UP:
                        input.input_queue.append('walk-up')
                        input.curr_input = 'walk-up'
                    elif event.key == pygame.K_DOWN:
                        input.input_queue.append('walk-down')
                        input.curr_input = 'walk-down'
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

                # if key is released remove the input from the input queue
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        input.input_queue.remove('walk-left')
                    if event.key == pygame.K_RIGHT:
                        input.input_queue.remove('walk-right')
                    if event.key == pygame.K_UP:
                        input.input_queue.remove('walk-up')
                    if event.key == pygame.K_DOWN:
                        input.input_queue.remove('walk-down')

                    # prev_input is whatever the curr_input was
                    input.prev_input = input.curr_input

                    if not input.input_queue: # queue is empty
                        input.curr_input = None # curr_input is None
                    else: # queue is not empty, set input to last element in queue
                        input.curr_input = input.input_queue[-1]

            # print("inputs curr inputs", input.curr_input)
            # print("inputs queue", input.input_queue)

# determines which frame should be drawn to screen
class AnimationProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        # determines which animation frames should be used given the current
        # state
        for ent, (state, animate, render, pos) in self.world.get_components(StateComponent, AnimationComponent, RenderComponent, PositionComponent):
            # set curr animation list
            if animate.animation_name != state.curr_state:
                animate.curr_animation = animate.animation_dict[state.curr_state]
                animate.animation_name = state.curr_state
                animate.animation_frame = 0
        
            if animate.animation_frame >= len(animate.curr_animation):
                animate.animation_frame = 0

            render.image = animate.curr_animation[int(animate.animation_frame)]
            # create a rect from the image and set the center based off position component
            render.rect = render.image.get_rect(center=pos.position)

               
            animate.animation_frame += PLAYER_ANIMATION_SPEED
            # print("curr animation", animate.curr_animation)

        
# Updates Position and Direction Components
# Position component is updated based on the direction and size of the currently rendering sprite
# Direction component is normalized to maintain consistent movement speed
class MovementProcessor(esper.Processor):
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
    
    def process(self):
        # iterate over every Entity with both of these components
        index = 0
        for ent, (pos, dir, rend, vel) in self.world.get_components(PositionComponent, DirectionComponent, RenderComponent, VelocityComponent):
            
            # normalizes direction
            if dir.direction.magnitude() > 0:
                dir.direction = dir.direction.normalize()

            # sets position x
            pos.position.x += dir.direction.x * vel.speed

            # sets position y
            pos.position.y += dir.direction.y * vel.speed

            # keeps sprite in bounds [TEMPORARY]
            # pos.position.x = max(self.minx, pos.position.x)
            # pos.position.y = max(self.miny, pos.position.y)
            # pos.position.x = min(self.maxx - rend.image.get_width(), pos.position.x)
            # pos.position.y = min(self.maxy - rend.image.get_height(), pos.position.y)


# Renders the sprite to the screen
# Updates Animation Component based on the current Image Sequence and Position
class RenderProcessor(esper.Processor):
    def __init__(self, clear_color=(0,0,0)):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.clear_color = clear_color
        self.offset = pygame.math.Vector2()

    def process(self):
        # Clear the window
        # self.window.fill(self.clear_color)
        self.display_surface.fill('black')

        # get player to calculate offset
        for ent, (input, rend_comp) in self.world.get_components(InputComponent, RenderComponent):

            # use player rect to set offset
            self.offset.x = rend_comp.rect.centerx - SCREEN_WIDTH / 2
            self.offset.y = rend_comp.rect.centery - SCREEN_HEIGHT / 2

        # iterate over all layers with render components
        for z, elem in enumerate(LAYERS):
        # iterate over every Entity that needs to be drawn at this layer and blit it
            for ent, (rend) in self.world.get_component(RenderComponent):
                if rend.depth == z:
                    offset_rect = rend.rect.copy()
                    offset_rect.center -= self.offset

                    self.display_surface.blit(rend.image, offset_rect)

            
            # speed of animation
            # anim.animation_frame += PLAYER_ANIMATION_SPEED
            # print("index", anim.animation_frame)

        # flip framebuffers
        # pygame.display.flip()
        pygame.display.update()

class DirectionProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        # update player direction based on state and current inputs
        for ent, (dir, state, input) in self.world.get_components(DirectionComponent, StateComponent, InputComponent):
            
            if "walk" in state.curr_state:
                # process input

                # TO DO: take another look at these two top conditions
                # if no left, right movement, set direction.x to 0
                if not any("right" in s for s in input.input_queue) and not any("left" in s for s in input.input_queue):
                    dir.direction.x = 0

                # if no up, down movement, set direction.y to 0
                if not any("up" in s for s in input.input_queue) and not any("down" in s for s in input.input_queue):
                    dir.direction.y = 0

                for i in input.input_queue:
                    # update direction based on which input keys are active
                    if i == 'walk-left':
                        dir.direction.x = -1
                    elif i == 'walk-right':
                        dir.direction.x = 1

                    if i == 'walk-up':
                        dir.direction.y = -1
                    elif i == 'walk-down':
                        dir.direction.y = 1
            else:
                dir.direction.x = 0
                dir.direction.y = 0

            # print("direction", dir.direction)
