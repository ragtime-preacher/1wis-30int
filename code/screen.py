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
        data = source.data
        self.surface = Surface ([
f" ~~ SKILLS PAGE ~~                                                             ",
f"    Proficiency Bonus: {data["prof_bonus"]:+}",
f"    Skills in alphabetical order:",
f"      ({self.get_proficiency_char(data["skills"]["acrobatics"])}) Acrobatics (DEX): {int(get_mod(data["stat_dex"])+data["prof_bonus"]*data["skills"]["acrobatics"]):+}",
f"      ({self.get_proficiency_char(data["skills"]["animal handling"])}) Animal Handling (WIS): {int(get_mod(data["stat_wis"])+data["prof_bonus"]*data["skills"]["animal handling"])}",
f"      ({self.get_proficiency_char(data["skills"]["arcana"])}) Arcana (INT): {int(get_mod(data["stat_int"])+data["prof_bonus"]*data["skills"]["arcana"])}",
f"      ({self.get_proficiency_char(data["skills"]["athletics"])}) Athletics (STR): {int(get_mod(data["stat_str"])+data["prof_bonus"]*data["skills"]["athletics"]):+}",
f"      ({self.get_proficiency_char(data["skills"]["deception"])}) Deception (CHA): {int(get_mod(data["stat_cha"])+data["prof_bonus"]*data["skills"]["deception"])}",
f"      ({self.get_proficiency_char(data["skills"]["history"])}) History (INT): {int(get_mod(data["stat_int"])+data["prof_bonus"]*data["skills"]["history"])}",
f"      ({self.get_proficiency_char(data["skills"]["insight"])}) Insight (WIS): {int(get_mod(data["stat_wis"])+data["prof_bonus"]*data["skills"]["insight"])}",
f"      ({self.get_proficiency_char(data["skills"]["intimidation"])}) Intimidation (CHA): {int(get_mod(data["stat_cha"])+data["prof_bonus"]*data["skills"]["intimidation"])}",
f"      ({self.get_proficiency_char(data["skills"]["investigation"])}) Investigation (INT): {int(get_mod(data["stat_int"])+data["prof_bonus"]*data["skills"]["investigation"])}",
f"      ({self.get_proficiency_char(data["skills"]["medicine"])}) Medicine (WIS): {int(get_mod(data["stat_wis"])+data["prof_bonus"]*data["skills"]["medicine"])}",
f"      ({self.get_proficiency_char(data["skills"]["nature"])}) Nature (INT): {int(get_mod(data["stat_int"])+data["prof_bonus"]*data["skills"]["nature"])}",
f"      ({self.get_proficiency_char(data["skills"]["perception"])}) Perception (WIS): {int(get_mod(data["stat_wis"])+data["prof_bonus"]*data["skills"]["perception"])}",
f"      ({self.get_proficiency_char(data["skills"]["performance"])}) Performance (CHA): {int(get_mod(data["stat_cha"])+data["prof_bonus"]*data["skills"]["performance"])}",
f"      ({self.get_proficiency_char(data["skills"]["persuasion"])}) Persuasion (CHA): {int(get_mod(data["stat_cha"])+data["prof_bonus"]*data["skills"]["persuasion"])}",
f"      ({self.get_proficiency_char(data["skills"]["arcana"])}) Religion (INT): {int(get_mod(data["stat_int"])+data["prof_bonus"]*data["skills"]["religion"])}",
f"      ({self.get_proficiency_char(data["skills"]["sleight of hand"])}) Sleight of Hand (DEX): {int(get_mod(data["stat_dex"])+data["prof_bonus"]*data["skills"]["sleight of hand"]):+}",
f"      ({self.get_proficiency_char(data["skills"]["stealth"])}) Stealth (DEX): {int(get_mod(data["stat_dex"])+data["prof_bonus"]*data["skills"]["stealth"]):+}",
f"      ({self.get_proficiency_char(data["skills"]["survival"])}) Survival (DEX): {int(get_mod(data["stat_wis"])+data["prof_bonus"]*data["skills"]["survival"])}",
        ]) ; return

class SpellScreen (Screen):
    def __init__ (self):
        super().__init__()
        self.alias = "spells"
    
    def render (self, source: Character):
        data = source.data
        self.surface = Surface ([
f" ~~ SPELLS PAGE ~~                                                             ",
f"    Spell Slots (available/total):"
])
        for i_slot_level in data["sc_slots_total"].keys():
            if data["sc_slots_total"][i_slot_level] != 0:
                self.surface.data.append(
f"      {i_slot_level}: {data["sc_slots_available"][i_slot_level]} / {data["sc_slots_total"][i_slot_level]}"
            )
        self.surface.data.append("-"*80)

        if len(data["sc_spells_known"]) == 0:
            # we're dealing with a preparation spellcaster.
            self.subrender_preparation(source)
        else:
            # It's a known-spells spellcaster.
            self.subrender_knowledge(source)
    
    def subrender_preparation (self, source: Character):
        data = source.data
        ps = [
f"    Spells prepared:"
        ]
        # cantrips have to be handled seperately
        if len(data["sc_cantrips_known"]) > 0:
            ps.append (
f"      = Cantrips (0th level) ="
            )
            ps.extend([f"          {i_cantrip["name"]}" for i_cantrip in data["sc_cantrips_known"]])

        # NTH LEVEL
        for nth_level_ordinal in data["sc_slots_total"].keys():
            # type(i_spell_level_ordinal) = str
            # hopefully one of the following: 1st, 2nd, 3rd, 4th, 5th, 6th, 7th, 8th, 9th
            if data["sc_slots_total"][nth_level_ordinal] == 0:
                # we've reached the end of our castable spells
                # write to the surface and bail.
                self.surface.data.extend (ps)
                return
            ps.append (
f"      = {nth_level_ordinal} level ="
            )
            nth_level_spells_list = [
f"{" "*10}{spell["name"]}" for spell in data["sc_spells_prep"] if spell["level"] == f"{nth_level_ordinal}-level"
            ]
            if len (nth_level_spells_list) == 0:
                ps.append(f"{" "*10}n/a")
            else:
                ps.extend(nth_level_spells_list)
            continue

# keep this for the comment documentation
    def subrender_preparation_legacy (self, source: Character):
        data = source.data
        # NOTE:
        #   This function is a big mess because I don't want to render levels
        #       of spells if our source doesn't have the capacity to cast
        #       those spells.
        #   There's probably a better way to deal with this problem, but I
        #       don't know what it is.
        ps = [
f"    Spells prepared:",
        ]
        # Not every spellcaster gets cantrips...
        #   (paladins, I'm looking at you)
        if len(data["sc_cantrips_known"]) > 0:
            ps.append (
f"      = Cantrips (0th level) ="
            )
            ps.extend([f"          {i_cantrip["name"]}" for i_cantrip in data["sc_cantrips_known"]])
        # past the cantrip point, we can check if we're allowed to each level of spells by looking
        #   at the number of spell slots that we have for each level.
        # if we don't have any nth level spell slots, we can assume that our
        #   character doesn't have the capacity to cast nth level spells, and
        #   there's no point in rendering that level.
        # at that point, we are good to exit our function.
        # But only if we've already extended our surface.
        
        # 1ST LEVEL
        if data["sc_slots_total"]["1st"] == 0:
            self.surface.data.extend(ps)
            return
        # otherwise, we'd better render our spells
        ps.append(
f"      = 1st level ="
        )
        level1_spells_list = [f"          {spell["name"]}" for spell in data["sc_spells_prep"] if spell["level"] == "1st-level"]
        # this if/else might seem a bit redundant, since earlier we are
        #   already checking if we are allowed to cast 1st level spells.
        # however, this double-checking would be helpful in a hypothetical
        #   situation where a higher-level spellcaster neglects to prepare any
        #   spells of a certain level - say a cleric, in a fit of insanity,
        #   neglects to prepare inflict wounds, or perhaps a paladin focuses
        #   her meager quantity of known spells on cool stuff like find steed,
        #   knowing full well that the best 1st-level paladin spell is 
        #   SMITE and there's hardly any point in preparing anything else.
        if len(level1_spells_list) == 0:
            ps.append(f"          n/a")
        else:
            ps.extend(level1_spells_list)

        # 2ND LEVEL
        if data["sc_slots_total"]["2nd"] == 0:
            self.surface.data.extend(ps)
            return

        ps.append(
f"      = 2nd level ="
        )
        level2_spells_list = [f"          {spell["name"]}" for spell in data["sc_spells_prep"] if spell["level"] == "2nd-level"]
        if len(level2_spells_list) == 0:
            ps.append(f"          n/a")
        else:
            ps.extend(level2_spells_list)

        # 3RD LEVEL
        if data["sc_slots_total"]["3rd"] == 0:
            self.surface.data.extend(ps)
            return
        ps.append(
f"      = 3rd level ="
        )
        level3_spells_list = [f"          {spell["name"]}" for spell in data["sc_spells_prep"] if spell["level"] == "3rd-level"]
        if len(level3_spells_list) == 0:
            ps.append(f"          n/a")
        else:
            ps.extend(level3_spells_list)

        # 4TH LEVEL
        if data["sc_slots_total"]["4th"] == 0:
            self.surface.data.extend(ps)
            return
        ps.append(
f"      = 4th level ="
        )
        level4_spells_list = [f"          {spell["name"]}" for spell in data["sc_spells_prep"] if spell["level"] == "4th-level"]
        if len(level4_spells_list) == 0:
            ps.append(f"          n/a")
        else:
            ps.extend(level4_spells_list)
        
        # 5TH LEVEL
        if data["sc_slots_total"]["5th"] == 0:
            self.surface.data.extend(ps)
            return
        ps.append(
f"      = 5th level ="
        )
        level5_spells_list = [f"          {spell["name"]}" for spell in data["sc_spells_prep"] if spell["level"] == "5th-level"]
        if len(level5_spells_list) == 0:
            ps.append(f"          n/a")
        else:
            ps.extend(level5_spells_list)

        # 6TH LEVEL
        if data["sc_slots_total"]["6th"] == 0:
            self.surface.data.extend(ps)
            return
        ps.append(
f"      = 6th level ="
        )
        level6_spells_list = [f"          {spell["name"]}" for spell in data["sc_spells_prep"] if spell["level"] == "6th-level"]
        if len(level6_spells_list) == 0:
            ps.append(f"          n/a")
        else:
            ps.extend(level6_spells_list)

        # 7TH LEVEL
        if data["sc_slots_total"]["7th"] == 0:
            self.surface.data.extend(ps)
            return
        ps.append(
f"      = 7th level ="
        )
        level7_spells_list = [f"          {spell["name"]}" for spell in data["sc_spells_prep"] if spell["level"] == "7th-level"]
        if len(level7_spells_list) == 0:
            ps.append(f"          n/a")
        else:
            ps.extend(level7_spells_list)

        # 8TH LEVEL
        if data["sc_slots_total"]["8th"] == 0:
            self.surface.data.extend(ps)
            return
        ps.append(
f"      = 8th level ="
        )
        level8_spells_list = [f"          {spell["name"]}" for spell in data["sc_spells_prep"] if spell["level"] == "8th-level"]
        if len(level8_spells_list) == 0:
            ps.append(f"          n/a")
        else:
            ps.extend(level8_spells_list)

        # 9TH LEVEL
        if data["sc_slots_total"]["9th"] == 0:
            self.surface.data.extend(ps)
            return
        ps.append(
f"      = 9th level ="
        )
        level9_spells_list = [f"          {spell["name"]}" for spell in data["sc_spells_prep"] if spell["level"] == "9th-level"]
        if len(level9_spells_list) == 0:
            ps.append(f"          n/a")
        else:
            ps.extend(level9_spells_list)

        # tack our postscript onto the main surface (assuming we 
        #   haven't already left the function)
        self.surface.data.extend(ps)
        return


    def subrender_knowledge (self, source: Character):
        pass
