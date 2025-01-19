# Screen
#   contains functionality to display information about a given class.

from curses import window
from Character import Character, get_mod
from surface import Surface

# thanks, ChatGPT
from abc import ABC, abstractmethod

class Screen (ABC) :
    
    def __init__(self):
        # Screen.surface
        #   a two-dimensional array to store lines and columns - coordinates, 
        #       in other words. conveniently, the (y, x) ordering used by
        #       curses interfaces perfectly with the two-dimensional array
        #       system. Maybe that's why they started using it in the first
        #       place?? sei la mano
        self.surface = Surface([[]])
        pass


        # render ()
        #   stores the needed character data in the surface attribute.
        #       this needs to be implimented individually by the 
        #       child classes.
    @abstractmethod
    def render (self, source: Character) -> None:
        pass

        # draw ()
        #   This is the real point of the parent class - to inherit 
        #       the drawing functionality to the child classes.
    def draw (self, dest: window) -> None:
        for i_row in range(len(self.surface.data)):
            dest.addstr(i_row, 0, self.surface.data[i_row])

class TestScreen(Screen):
    def __init__(self):
        self.surface = Surface ([[]])

    def render (self):
        self.surface = Surface ([
            "123",
            "456",
            "789"
        ])

class HomeScreen (Screen):
    def render (self, source: Character):
        data = source.data
        self.surface = Surface ([
f"{data["name"]:<80}",
f"Stats{' ':<75}",
f"STR: {data["stat_str"]:<75}",
f"DEX: {data["stat_dex"]:<75}",
f"CON: {data["stat_con"]:<75}",
f"INT: {data["stat_int"]:<75}",
f"WIS: {data["stat_wis"]:<75}",
f"CHA: {data["stat_cha"]:<75}"
        ])

class StatScreen (Screen):
    def render (self, source: Character):
        data = source.data
        saving_throw_bonus = {
            "str": get_mod(data["stat_str"]) + (data["prof_bonus"] * int(data["prof_st_str"])),
            "dex": get_mod(data["stat_dex"]) + (data["prof_bonus"] * int(data["prof_st_dex"])),
            "con": get_mod(data["stat_con"]) + (data["prof_bonus"] * int(data["prof_st_con"])),
            "int": get_mod(data["stat_int"]) + (data["prof_bonus"] * int(data["prof_st_int"])),
            "wis": get_mod(data["stat_wis"]) + (data["prof_bonus"] * int(data["prof_st_wis"])),
            "cha": get_mod(data["stat_cha"]) + (data["prof_bonus"] * int(data["prof_st_cha"]))
        }
        
        self.surface = Surface ([
f" ~~ ABILITY SCORE PAGE ~~                                                      ",
f"          =============          =============          =============          ",
f"          | ~~ STR ~~ |          | ~~ DEX ~~ |          | ~~ CON ~~ |",
f"          |  {data["stat_str"]:>2}  ({get_mod(data["stat_str"]):+}) |          |  {data["stat_dex"]:>2}  ({get_mod(data["stat_dex"]):+}) |          |  {data["stat_con"]:>2}  ({get_mod(data["stat_con"]):+}) |",
f"          |  ST:  {saving_throw_bonus['str']:>+2}  |          |  ST:  {saving_throw_bonus['dex']:>+2}  |          |  ST:  {saving_throw_bonus['con']:>+2}  |",
f"          =============          =============          =============",
f"",
f"",
f"          =============          =============          =============",
f"          | ~~ INT ~~ |          | ~~ WIS ~~ |          | ~~ CHA ~~ |",
f"          |  {data["stat_int"]:>2}  ({get_mod(data["stat_int"]):+}) |          |  {data["stat_wis"]:>2}  ({get_mod(data["stat_wis"]):+}) |          |  {data["stat_cha"]:>2}  ({get_mod(data["stat_cha"]):+}) |",
f"          |  ST:  {saving_throw_bonus['int']:>+2}  |          |  ST:  {saving_throw_bonus['wis']:>+2}  |          |  ST:  {saving_throw_bonus['cha']:>+2}  |",
f"          =============          =============          =============",
        ])

class CombatScreen (Screen):
    def render (self, source: Character):
        data = source.data
        self.surface = Surface ([
f" ~~ COMBAT PAGE ~~                                                             ",
f"    Initiative bonus: {data["initiative_bonus"]:+}",
f"    Armor Class: {data["armor_class"]}",
f"    Hit Points: {data["hp_max"]} / {data["hp_current"]} {"+ " + str(data["hp_temporary"]) + " temporary" if int(data["hp_temporary"]) > 0 else ""}",
f"    Weapon Attacks:"
        ])
        for i_attack in data["attacks"]:
            self.surface.data.append (f"\t{i_attack}")
