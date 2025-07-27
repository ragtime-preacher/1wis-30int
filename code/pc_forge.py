# The purpose of the code here is to provide means by which a functional
#   playable character can be spat out in json form for access by the
#   other half of the program.

import json
import easygui


# steal my py libraries from the json_libraries folder
import sys, os
current_dir = os.path.dirname(__file__)
lib_path = os.path.abspath(os.path.join(current_dir, '..', 'json_libraries'))
sys.path.append(lib_path)

# janky I know but it seems to work
from alt_species_library import SPECIES_DICTIONARY

from empty_pc_data import generate_empty_pc_data

# NOTE
#   The PC class IS NOT the same class that will represent a character during
#       the terminal-based character sheet. That's the Character class.
#   Maybe they should be the same thing, but for now they aren't. However, the
#       JSON resulting from running the PC constructor should plug right in to
#       the Character class's constructor interface.
# LEGACY (hopefully)
class PC:
    def __init__(self, split_token: str = ';'):
        self.data = {} # this is the big, overarching dictionary
        self.st = split_token
        species_lib = open("/home/feijao/programming/1wis-30int/json_libraries/species_library.json")
        all_species = json.load(species_lib)
        species_lib.close()
        species_dict = all_species["dwarf"]
        for i_key in species_dict.keys():
            current_feature_raw = species_dict[i_key]
            current_feature_split = current_feature_raw.split(self.st)

            self.data[i_key] = current_feature_split[0] # flavor text
            self._parse_metadata(current_feature_split[1], i_key, current_feature_split[0])
    
    # read everything after the ';' and make sure that our character's data
    #   gets updated to suit.
    def _parse_metadata (self, metadata: str, feature_key, flavor=""):
        # Choice token parsing
        choice_token = metadata.find("CHOICE")
        # this returns -1 on a fail.
        if choice_token == -1:
            # we've hit a null, so it doesn't matter. we have nothing to choose.
            pass
        # otherwise, we'll have to manage a choice token.
        else:
            choice_list_index = choice_token+len("CHOICE")
            # this is the start of our choices. It should go until the end.
            # choice_list_index should be a [.
            # there's also supposed to be a ] floating around at the end somewhere.
            choice_substring = metadata[choice_list_index:]
            no_brackets = choice_substring.removeprefix('[').removesuffix(']')
            choices = no_brackets.split(',')
            selection = None
            while selection == None:
                selection = easygui.choicebox(msg=flavor, title="character selection", choices=choices)
            print (f"selected: {selection}")
            # next, we have to actually modify our data to reflect this.
            self.data[feature_key] = f"{self.data[feature_key]} Selected: {selection}"
            # TODO: write this to larger JSON file for Character.Character


        
    def __str__(self):
        return f"{self.data}"
    
class ALT_PC:
    def __init__(self):
        self.data = generate_empty_pc_data()
        self._choose_species()
        self._choose_class()
        self._determine_ability_scores()
        self._describe_character()
        self._choose_equipment()
        self._write_json()

    def _choose_species (self):
        chosen_species = easygui.choicebox("Select a race (please refer to an actual book for details because I'm too lazy to type all that out)", title="species selection", choices=SPECIES_DICTIONARY.keys())
        SPECIES_DICTIONARY[chosen_species](self.data)
    def _choose_class (self):
        pass
    def _determine_ability_scores (self):
        pass
    def _describe_character (self):
        # pretty much background and that's it
        pass 
    def _choose_equipment (self):
        pass
    def _write_json (self):
        pass

    def __str__(self):
        return f"{self.data}"

# one day, I'd like the selection to be terminal-based too. However, just for
#   here and now, I think EasyGui is a better solution.
# Terminal-based selection will require something with the same interface as
#   easy gui, it just will run in the terminal.

print (ALT_PC())