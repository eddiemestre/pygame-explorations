import pygame
import json 

class SpriteSheet:
    def __init__(self, filename, jsonfile):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = jsonfile
        try:
            with open(self.meta_data) as f:
                self.data = json.load(f)
            f.close()
        except FileNotFoundError:
            raise("File does not exist")
    
    def get_sprite(self, x, y, w, h):
        # initialize empty sprite surface
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0,0,0))
        # take empty surface and paste image onto it
        sprite.blit(self.sprite_sheet, (0,0), (x, y, w, h))

        # Temporary scaling while playing around with Link sprite
        return pygame.transform.scale(sprite, (40,40))
        
    def parse_sprite(self, name, frame_type):
        # grab sub_dict
        animation_sequence = []
        try:
            sprite = self.data['frames'][name][frame_type]
            # print("sprite", type(sprite))
            # iterate over sprite frame types and add to animation list
            for image in sprite:
                x = sprite[image]['frame']['x']
                # print("x", x)
                y = sprite[image]['frame']['y']
                w = sprite[image]['frame']['w']
                h = sprite[image]['frame']['h']
                animation_sequence.append(self.get_sprite(x, y, w, h).convert_alpha())
        except KeyError:
            print("invalid arguments for parsing sprites")
            pass

        assert(isinstance(animation_sequence, list))
        # print("is list")
        return animation_sequence


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



# may need to make sprite component and have img and rec as attributes
# then we have a dict of states with individual sprite components in them instead of surfaces themselves
# we get the surfaces by calling .image and the rects by calling .rect