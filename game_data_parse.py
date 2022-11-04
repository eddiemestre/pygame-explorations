import json

# returns list of character inputs
def parse_inputs(filename):
    f = open(filename)
    game_data = json.load(f)
    f.close()
    input_list = []
    for input in game_data["Player"]["input"]:
        input_list.append(input)
    
    return input_list

# returns a tuple
# first value is a list of states
# second value is a default state
def parse_states(filename):
    f = open(filename)
    game_data = json.load(f)
    f.close()
    state_list = []
    for state in game_data["Player"]["state"]:
        state_list.append(state)
    
    current_state = game_data["Player"]["default-state"]
    
    return state_list, current_state


def parse_render_depth(entity, filename):
    f = open(filename)
    game_data = json.load(f)
    f.close()

    return game_data[entity]["depth"]

# get layers for entities
def extract_layers(filename):
    f = open(filename)
    game_data = json.load(f)
    f.close()

    layers = []
    for layer in game_data["Layers"]:
        layers.append(layer)

    assert(isinstance(layers, list))
    return layers
