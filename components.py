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

import pygame
import esper

PLAYER_WALK_SPEED = 0.25

# Components
class VelocityComponent:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y



class RenderComponent:
    def __init__(self, default_sequence, posx, posy, depth=0):
        self.image_sequence = default_sequence
        self.depth = depth
        self.x = posx
        self.y = posy
        # self.w = image.get_width()
        # self.h = image.get_height()

class AnimationComponent:
    def __init__(self, anim_dict, default_animation):
        self.animation_dict = anim_dict # stores lists of animation frames
        self.curr_animation = default_animation
        self.animation_frame = 0

class StateComponent:
    def __init__(self, state_options, default_state):
        assert(isinstance(state_options, list))
        self.entity_states = {}
        self.curr_state = None
        for option in state_options:
            self.entity_states[option] = False
        self.entity_states[default_state] = True
        self.curr_state = default_state


class InputComponent: # do we want two inputs possible at same time? aka walking?
    def __init__(self, input_options):
        assert(isinstance(input_options, list))
        self.inputs = {} # list of possible inputs
        self.curr_input = None
        self.input_queue = []
        # self.curr_input = None
        for option in input_options:
            self.inputs[option] = False


class StateProcessor(esper.Processor):
    def __init__(self):
        self.same = False

    def process(self):
        # loops through entities with state components and updates
        # their states according to either input updates or 
        # AI updates

        # handle updates from InputComponent
        for ent, (input, state) in self.world.get_components(InputComponent, StateComponent):
            if state.curr_state != input.curr_input and input.curr_input != None:
                state.curr_state = input.curr_input
                self.same = False
                # print("curr_state in StateProcessor", state.curr_state)
            elif state.curr_state != input.curr_input and input.curr_input == None and self.same == False:
                # print("curr_state in StateProcessor", state.curr_state)
                self.same = True


        # handle updates from Computer info (AI movement, attacking, etc)
        for ent, state in self.world.get_components(StateComponent):
            pass

# should only belong to moveable entities (probably especially the player)
class InputProcessor(esper.Processor):
    def __init__(self):
        pass


    def process(self):
        prev_input = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # pass event to input system         
            # grab each entity that has an Input Component
            #
            # TO DO:
            # 1. maybe eliminate the inputs dict, not necessary
            # 2. clean this up
            for ent, input in self.world.get_component(InputComponent):
                # update that entity's input component with new state
                # eventually this should be defined in a json file
                if event.type == pygame.KEYDOWN:
                    input.inputs['idle-left'] = False
                    input.inputs['idle-right'] = False
                    input.inputs['idle-up'] = False
                    input.inputs['idle-down'] = False
                    if event.key == pygame.K_LEFT:
                        input.inputs['walk-left'] = True
                        input.input_queue.append('walk-left')
                        input.curr_input = 'walk-left'
                    elif event.key == pygame.K_RIGHT:
                        input.inputs['walk-right'] = True
                        input.input_queue.append('walk-right')
                        input.curr_input = 'walk-right'
                    elif event.key == pygame.K_UP:
                        input.inputs['walk-up'] = True
                        input.input_queue.append('walk-up')
                        input.curr_input = 'walk-up'
                    elif event.key == pygame.K_DOWN:
                        input.inputs['walk-down'] = True
                        input.input_queue.append('walk-down')
                        input.curr_input = 'walk-down'
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    # print("inputs", input.inputs)
                    # print("inputs curr inputs", input.curr_input)
                    # print("inputs queue", input.input_queue)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        input.inputs['walk-left'] = False
                        prev_input = "walk-left"
                        input.input_queue.remove('walk-left')
                    if event.key == pygame.K_RIGHT:
                        input.inputs['walk-right'] = False
                        input.input_queue.remove('walk-right')
                        prev_input = "walk-right"
                    if event.key == pygame.K_UP:
                        input.inputs['walk-up'] = False
                        input.input_queue.remove('walk-up')
                        prev_input = "walk-up"
                    if event.key == pygame.K_DOWN:
                        input.inputs['walk-down'] = False
                        input.input_queue.remove('walk-down')
                        prev_input = "walk-down"
                
                    if not input.input_queue: # queue is empty, set idle
                        if prev_input == "walk-left":
                            input.inputs['idle-left'] = True
                            input.curr_input = 'idle-left'
                        elif prev_input == 'walk-right':
                            input.inputs['idle-right'] = True
                            input.curr_input = 'idle-right'
                        elif prev_input == 'walk-up':
                            input.inputs['idle-up'] = True
                            input.curr_input = 'idle-up'
                        elif prev_input == 'walk-down':
                            input.inputs['idle-down'] = True
                            input.curr_input = 'idle-down'
                        else:
                            raise ValueError("input queue should be empty")
                    else: # queue is not empty, set input to last element in queue
                        input.curr_input = input.input_queue[-1]

                    # input.curr_input = 'idle-down'
                    # print("inputs", input.inputs)
                    # print("inputs curr inputs", input.curr_input)
                    # print("inputs queue", input.input_queue)


class AnimationProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        # determines which animation frames should be used given the current
        # state
        for ent, (state, animate, render) in self.world.get_components(StateComponent, AnimationComponent, RenderComponent):
            if animate.curr_animation != animate.animation_dict[state.curr_state]:
                animate.curr_animation = animate.animation_dict[state.curr_state]
                render.image_sequence = animate.curr_animation
                animate.animation_frame = 0
                # print("curr animation", animate.curr_animation)

        

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
        for ent, (vel, rend, state) in self.world.get_components(VelocityComponent, RenderComponent, StateComponent):
            # update renderable component's position by its velocity
            rend.x += vel.x
            rend.y += vel.y

            # keeps sprite in bounds
            rend.x = max(self.minx, rend.x)
            rend.y = max(self.miny, rend.y)
            rend.x = min(self.maxx - rend.image_sequence[int(index % len(rend.image_sequence))].get_width(), rend.x)
            rend.y = min(self.maxy - rend.image_sequence[int(index % len(rend.image_sequence))].get_height(), rend.y)

class RenderProcessor(esper.Processor):
    def __init__(self, window, clear_color=(0,0,0)):
        super().__init__()
        self.window = window
        self.clear_color = clear_color
        self.index = 0

    def process(self):
        # Clear the window
        self.window.fill(self.clear_color)

        # iterate over every Entity that has this component and blit it
        for ent, (rend, anim) in self.world.get_components(RenderComponent, AnimationComponent):
            # print("len rend image", len(rend.image))
            if anim.animation_frame >= len(rend.image_sequence):
                anim.animation_frame = 0
            self.window.blit(rend.image_sequence[int(anim.animation_frame)], (rend.x, rend.y))

            # speed of animation
            anim.animation_frame += PLAYER_WALK_SPEED
            # print("index", anim.animation_frame)

        # flip framebuffers
        pygame.display.flip()

class VelocityProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        # update player velocity based on state
        # TO DO:
        # 1. enable diagnal walking. Potentially just add the velocity value if that state is not 
        # already accounted for in the state list (the input queue)
        for ent, (input, vel, state) in self.world.get_components(InputComponent, VelocityComponent, StateComponent):
            if state.curr_state == 'walk-left':
                vel.x = -4
                vel.y = 0
            elif state.curr_state == 'walk-right':
                vel.x = 4
                vel.y = 0
            elif state.curr_state == 'walk-up':
                vel.y = -4
                vel.x = 0
            elif state.curr_state == 'walk-down':
                vel.y = 4
                vel.x = 0
            else:
                vel.x = 0
                vel.y = 0