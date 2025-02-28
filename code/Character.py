# Character class

# In theory, contains everything that a character needs to have in order
#   to be played in Dnd.

# The actual character data will be stored in a dictionary that we can
#   save to and load from a .json file.

import json

import re

def get_mod (ability_score: int) -> int:
    if ability_score >= 10:
        return int(ability_score / 2 - 5)
    else:
        return int((ability_score-1) / 2 - 5)

class Character:
    def __init__(self, filename: str):
        self.data_file = open (filename)
        self.data = json.load(self.data_file)
        self.data_file.close ()
        self.update_everything ()
        # in practice, we'll need to call this update_everything function
        #   whenever we render a screen.
        return
    
    def write_file (self, filename: str):
        outfile = open (filename, 'w')
        json.dump (self.data, outfile)
        outfile.close()

    def update_everything (self):
        self.update_attacks()
        self.update_spells ()
        # other update methods

    # Character.update_attacks ()
    #   go through our equipment and add attack strings to the data["attacks"]
    #       list.
    def update_attacks (self):
        weapon_library = open ("/home/lurch5-64/progamming/1wis-30int/weapon_library.json")
        weapon_dict = json.load(weapon_library)
        weapon_library.close ()
        try:
            # First, we'll take away attacks for weapons that we don't have.
            for i_attack in self.data["attacks"]:
                attack_name = i_attack.split(":")[0]
                # this should give us the string until the first colon.
                #   Because of the way that these strings are constructed
                #       in the first place, this will be the "name" attribute
                #       of the weapon in the weapon library.
                if not attack_name in [
                    weapon_dict[w]["name"] for w in self.data["eq_weapons"]
                    # ^ this is a complicated list comprehension that basically means:
                    #       "a list of the true names (capitalized and everything)
                    #       of every weapon that the charcter has"
                ]:
                    self.data["attacks"].remove(i_attack)
            # now, we'll add the attacks for weapons that we have
            for i_weapon in self.data["eq_weapons"]:
                # type(i_weapon) = 'str'
                w_data = weapon_dict[i_weapon]
                # make sure we don't add any duplicate attacks
                #   we'll do this by comparing the weapon names.
                copy_found = False
                for i_attack in self.data["attacks"]:
                    if i_attack.startswith(w_data["name"]):
                        copy_found = True
                if copy_found: continue
                attack_mod = 0
                if not "finesse" in w_data["tags"]:
                    # this is a normal weapon with only one attack stat option.
                    if w_data["attack_stat"] == "STR":
                        attack_mod += get_mod(self.data["stat_str"])
                    elif w_data["attack_stat"] == "DEX":
                        attack_mod += get_mod(self.data["stat_dex"])
                else:
                    # we are dealing with a finesse weapon.
                    #   We'll make the attack_modifier whatever's highest
                    #       between strength and dexterity.
                    #   Heaven help hexblade warlocks and artificers.
                    if self.data["stat_str"] >= self.data["stat_dex"]:
                        attack_mod += get_mod(self.data["stat_str"])
                    else:
                        attack_mod += get_mod(self.data["stat_dex"])

                range_portion = w_data["range"]
                for i_tag in w_data["tags"]:
                    if i_tag.startswith("thrown"):
                        range_portion += f" ({re.sub(r'[()]', '', i_tag)} ft)"
                weapon_string = f"{w_data["name"]}: {self.data["prof_bonus"] + attack_mod:+} to hit, {range_portion}; {w_data["dice"]}{attack_mod:+} {w_data["damage_type"]}"
                self.data["attacks"].append(weapon_string)

        except KeyError as e:
            # something went wrong with our keys
            self.data["attacks"].append(e)
    
    def update_spells (self):
        pass

# DEBUGGING ONLY
    def _populate_spells (self) :
        spell_library = open("/home/lurch5-64/progamming/1wis-30int/json_libraries/efficient_spell_library.json")
        # probably the most gargantuan dictionary I've ever used
        spell_dict = json.load(spell_library)
        spell_library.close()

        self.data["sc_slots_total"] = {
		"1st": 2,
		"2nd": 1,
		"3rd": 0,
		"4th": 0,
		"5th": 0,
		"6th": 0,
		"7th": 0,
		"8th": 0,
		"9th": 0
	}
        self.data["sc_slots_available"] = {
		"1st": 2,
		"2nd": 1,
		"3rd": 0,
		"4th": 0,
		"5th": 0,
		"6th": 0,
		"7th": 0,
		"8th": 0,
		"9th": 0
	}
        self.data["sc_spells_prep"] = [
            spell_dict["shield"],
            spell_dict["scorching ray"]
        ]

        self.data["sc_cantrips_known"] = [
            spell_dict["eldritch blast"]
        ]

        self.write_file("test_character_data_with_spells.json")