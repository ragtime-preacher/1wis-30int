# Screen
#   contains functionality to display information about a given class.

import curses
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
        # Screen.alias
        #   This variable is used to identify the specific child of Screen
        #       when switching between screens based on user input.
        #   It can be a string (for a single alias) or a list of strings
        #       for various aliases.
        self.alias = "abstract"
        self.scroll_index = 0


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
    def draw (self, dest: curses.window) -> None:
        # We'll switch to using a pad so we can scroll data that's too big.
        for i_row in range(self.scroll_index, len(self.surface.data)):
            try:
                dest.addstr(i_row-self.scroll_index, 0, self.surface.data[i_row])
            except curses.error:
                pass
    
    def update_scroll_index (self, amount: int) :
        if len(self.surface.data) < curses.LINES:
            # the data on screen is smaller than our window.
            # we don't need to scroll here.
            return
        self.scroll_index += amount
        # now we need to repair the damage
        if self.scroll_index < 0:
            self.scroll_index = 0
        elif self.scroll_index > len(self.surface.data)-curses.LINES+1:
            self.scroll_index = len(self.surface.data)-curses.LINES+1
        # TODO impliment this
        

        # get_proficiency_char ()
        #   This function is needed by two of our subclasses, so I decided to 
        #       keep it here.
    def get_proficiency_char (self, prof: float) :
        if prof == 0.0: # no proficiency
            return " "
        if prof == 0.5: # jack of all trades
            return "-"
        if prof == 1.0: # proficiency
            return "/"
        if prof == 2.0: # expertise
            return "X"

class TestScreen(Screen):
    def __init__(self):
        self.surface = Surface ([[]])
        self.alias = "test"

    def render (self):
        self.surface = Surface ([
            "123",
            "456",
            "789"
        ])

class HomeScreen (Screen):
    def __init__(self):
        super().__init__()
        self.alias = "home"

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
    def __init__ (self):
        super().__init__()
        self.alias = "stat"

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
    def __init__ (self):
        super().__init__()
        self.alias = "combat"

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

# The screen for showing skills, grouped together by the parent attribute
# read "ParentAttributeSort"
class SkillScreenPAS (Screen):
    def __init__ (self):
        super().__init__()
        self.alias = "skill24"

    def render (self, source: Character):
        data = source.data
        self.surface = Surface ([
f" ~~ SKILLS PAGE ~~                                                             ",
f"    Proficiency Bonus: {data["prof_bonus"]:+}",
f"    Skills by parent attribute:",
f"    = STRENGTH ({get_mod(data["stat_str"]):+}) =",
f"      ({self.get_proficiency_char(data["skills"]["athletics"])}) Athletics: {int(get_mod(data["stat_str"])+data["prof_bonus"]*data["skills"]["athletics"]):+}",
f"    = DEXTERITY ({get_mod(data["stat_dex"]):+}) =",
f"      ({self.get_proficiency_char(data["skills"]["acrobatics"])}) Acrobatics: {int(get_mod(data["stat_dex"])+data["prof_bonus"]*data["skills"]["acrobatics"]):+}",
f"      ({self.get_proficiency_char(data["skills"]["sleight of hand"])}) Sleight of Hand: {int(get_mod(data["stat_dex"])+data["prof_bonus"]*data["skills"]["sleight of hand"]):+}",
f"      ({self.get_proficiency_char(data["skills"]["stealth"])}) Stealth: {int(get_mod(data["stat_dex"])+data["prof_bonus"]*data["skills"]["stealth"]):+}",
f"    = CONSTITUTION ({get_mod(data["stat_con"]):+}) =",
f"      n/a",
f"    = INTELLIGENCE ({get_mod(data["stat_int"]):+}) =",
f"      ({self.get_proficiency_char(data["skills"]["arcana"])}) Arcana: {int(get_mod(data["stat_int"])+data["prof_bonus"]*data["skills"]["arcana"])}",
f"      ({self.get_proficiency_char(data["skills"]["history"])}) History: {int(get_mod(data["stat_int"])+data["prof_bonus"]*data["skills"]["history"])}",
f"      ({self.get_proficiency_char(data["skills"]["investigation"])}) Investigation: {int(get_mod(data["stat_int"])+data["prof_bonus"]*data["skills"]["investigation"])}",
f"          passive: {int(10 + get_mod(data["stat_int"]) + data["prof_bonus"] * data["skills"]["investigation"])}",
f"      ({self.get_proficiency_char(data["skills"]["nature"])}) Nature: {int(get_mod(data["stat_int"])+data["prof_bonus"]*data["skills"]["nature"])}",
f"      ({self.get_proficiency_char(data["skills"]["arcana"])}) Religion: {int(get_mod(data["stat_int"])+data["prof_bonus"]*data["skills"]["religion"])}",
f"    = WISDOM ({get_mod(data["stat_wis"]):+}) =",
f"      ({self.get_proficiency_char(data["skills"]["animal handling"])}) Animal Handling: {int(get_mod(data["stat_wis"])+data["prof_bonus"]*data["skills"]["animal handling"])}",
f"      ({self.get_proficiency_char(data["skills"]["insight"])}) Insight: {int(get_mod(data["stat_wis"])+data["prof_bonus"]*data["skills"]["insight"])}",
f"          passive: {int(10 + get_mod(data["stat_wis"]) + data["prof_bonus"] * data["skills"]["insight"])}",
f"      ({self.get_proficiency_char(data["skills"]["medicine"])}) Medicine: {int(get_mod(data["stat_wis"])+data["prof_bonus"]*data["skills"]["medicine"])}",
f"      ({self.get_proficiency_char(data["skills"]["perception"])}) Perception: {int(get_mod(data["stat_wis"])+data["prof_bonus"]*data["skills"]["perception"])}",
f"          passive: {int(10 + get_mod(data["stat_wis"]) + data["prof_bonus"] * data["skills"]["perception"])}",
f"      ({self.get_proficiency_char(data["skills"]["survival"])}) Survival: {int(get_mod(data["stat_wis"])+data["prof_bonus"]*data["skills"]["survival"])}",
f"    = CHARISMA ({get_mod(data["stat_cha"]):+}) =",
f"      ({self.get_proficiency_char(data["skills"]["deception"])}) Deception: {int(get_mod(data["stat_cha"])+data["prof_bonus"]*data["skills"]["deception"])}",
f"      ({self.get_proficiency_char(data["skills"]["intimidation"])}) Intimidation: {int(get_mod(data["stat_cha"])+data["prof_bonus"]*data["skills"]["intimidation"])}",
f"      ({self.get_proficiency_char(data["skills"]["performance"])}) Performance: {int(get_mod(data["stat_cha"])+data["prof_bonus"]*data["skills"]["performance"])}",
f"      ({self.get_proficiency_char(data["skills"]["persuasion"])}) Persuasion: {int(get_mod(data["stat_cha"])+data["prof_bonus"]*data["skills"]["persuasion"])}",
    ]) ; return
    


# The screen for showing skills, sorted alphabetically
# read "AlphaBeticalSort"
class SkillScreenABS (Screen):
    def __init__ (self):
        super().__init__()
        self.alias = "skill14"

    def render (self, source: Character) :
        pass