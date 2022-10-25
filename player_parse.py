import json

# returns list of character inputs
def parse_inputs(filename):
    f = open(filename)
    player_data = json.load(f)
    f.close()
    input_list = []
    for input in player_data["input"]:
        input_list.append(input)
    
    return input_list

# returns a tuple
# first value is a list of states
# second value is a default state
def parse_states(filename):
    f = open(filename)
    player_states = json.load(f)
    f.close()
    state_list = []
    for state in player_states["state"]:
        state_list.append(state)
    
    current_state = player_states["default-state"]
    
    return state_list, current_state

# associates state keys with animation list values
# eg: animations[state] = animation_list
# takes in a state list and spritesheet
# uses the state list to properly parse the spritesheet
def parse_animations(state_list, spritesheet):

    animation_dict = {}

    for state in state_list:
        sprite_list = spritesheet.parse_sprite("Player", state)
        if isinstance(sprite_list, list):
            animation_dict[state] = sprite_list
    
    return animation_dict