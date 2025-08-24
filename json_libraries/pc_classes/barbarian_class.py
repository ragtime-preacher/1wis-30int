# The mighty barbarian.

# I'm pretty sure that multiclassing only affects the first level.

import sys, os
current_dir = os.path.dirname(__file__)
lib_path = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(lib_path)

import faca
import easygui as eg

def barbarian_multi_1(char_data: dict):
    pass

def barbarian_level_1(char_data: dict):
    # CON score hasn't been determined yet... so a different function will
    #   have to take care of that a little later. But that's OK because
    #   increasing CON later on makes your entire HP higher as if it had
    #   always been that way, so we'd need somebody to live-reload this
    #   in any case.
    # Fortunately, we should be able to do this through the hit dice...
    char_data["hit_die"].append("d12")
    char_data["prof_armor"].extend("light", "medium", "shields")
    char_data["prof_weapons"].append ("all")
    char_data["prof_st_str"] = True
    char_data["prof_st_con"] = True
    first_skill = faca.choose_skill(
        flavor="pick a barbarian skill",
        # this is a bit of a mess but it's supposed to give us a list
        #   of skills in which we are already proficient
        ignore=[i_skill for i_skill in char_data["skills"].keys() if char_data["skills"][i_skill] > 0.0],
        include=[
            "animal handling",
            "athletics",
            "intimidation",
            "nature",
            "perception",
            "survival"
        ]
    )
    second_skill = faca.choose_skill(
        flavor="pick another barbarian skill",
        # this is a bit of a mess but it's supposed to give us a list
        #   of skills in which we are already proficient
        ignore=[i_skill for i_skill in char_data["skills"].keys() if char_data["skills"][i_skill] > 0.0],
        include=[
            "animal handling",
            "athletics",
            "intimidation",
            "nature",
            "perception",
            "survival"
        ]
    )
    if first_skill == None:
        first_skill = "athletics"
    if second_skill == None:
        second_skill = "intimidation"
    char_data["skills"][first_skill] = 1.0
    char_data["skills"][second_skill] = 1.0
    # equipment time
    if eg.buttonbox(
        msg="select equipment:",
        title="one of many don't worry",
        choices=["a greataxe", "any martial melee weapon"]
    ) == "any martial melee weapon":
        char_data["eq_weapons"].append(faca.choose_weapon(weapon_class="martial", weapon_range="melee"))
    else:
        char_data["eq_weapons"].append("greataxe")
    if eg.buttonbox(
        msg="select again",
        title="i recommend the handaxes",
        choices=["two handaxes", "any simple weapon"]
    ) == "any simple weapon":
        char_data["eq_weapons"].append(faca.choose_weapon("simple"))
    else:
        char_data["eq_weapons"].extend(["handaxe a", "handaxe b"])
    char_data["eq_other"].append("exporer's pack")
    char_data["eq_weapons"].append("4 javelins")
    # we're not done yet!
    # proficiency bonus should be handled outside of classes
    #   in the level-up code.
    # Rage
    char_data["class_features"]["Rage"] = {
        "description": "In battle, you fight with primal ferocity. On your turn, you can enter a rage as a bonus action.",
        "glance": "go nuts and start killing stuff",
        "uses total": 2,
        "uses available": 2,
        "timeframe": "longrest"
    }
    # this will be updated by future levels
    char_data["class_features"]["Unarmored Defense (Barbarian)"] = {
        "description": "While you are not wearing any armor, your Armor Class equals 10 + your Dexterity modifier + your Constitution modifier. You can use a shield and still gain this benefit.",
        "glance": "without any armor, AC = 10 + DEX mod + CON mod.",
        "uses total": -1,
        "uses available": -1,
        "timeframe": "n/a"
    }
    char_data["levels"].append("BARBARIAN 1")

def barbarian_level_2(char_data: dict):
    char_data["hit_die"].append("d12")
    char_data["class_features"]["Reckless Attack"] = {
        "description": "Starting at 2nd level, you can throw aside all concern for defense to attack with fierce desperation. When you make your first attack on your turn, you can decide to attack recklessly. Doing so gives you advantage on melee weapon attack rolls using Strength during this turn, but attack rolls against you have advantage until your next turn.",
        "glance": "attack with advantage. Any surviving foes have advantage against you.",
        "uses total": -1,
        "uses available": -1,
        "timeframe": "n/a"
    }
    char_data["class_features"]["Danger Sense"] = {
        "description": "At 2nd level, you gain an uncanny sense of when things nearby aren't as they should be, giving you an edge when you dodge away from danger. You have advantage on Dexterity saving throws against effects that you can see, such as traps and spells. To gain this benefit, you can't be blinded, deafened, or incapacitated.",
        "glance": "adv on pretty much all DEX ST",
        "uses total": -1,
        "uses available": -1,
        "timeframe": "n/a"
    }
    char_data["levels"].append("BARBARIAN 2") 

def barbarian_level_3(char_data: dict):
    char_data["hit_die"].append("d12")
    # this is the level when we'll handle subclass choice
    chosen_sc = eg.choicebox(
        msg="Subclass time! Pick one from below:",
        title="totem warrior op",
        choices=["Path of the Berserker", "Also path of the Berserker"]
    )
    match chosen_sc:
        case "Path of the Berserker" | None:
            barbarian_sc_berserker_3(char_data=char_data)
        case _:
            pass
    char_data["levels"].append("BARBARIAN 3")
    

def barbarian_level_4(char_data: dict):
    char_data["hit_die"].append("d12")
    scores_to_mod = faca.ability_score_increase({
        "STR": char_data["stat_str"],
        "DEX": char_data["stat_dex"],
        "CON": char_data["stat_con"],
        "INT": char_data["stat_int"],
        "WIS": char_data["stat_wis"],
        "CHA": char_data["stat_cha"]
    })
    for i_score in scores_to_mod:
        char_data["stat_mods"][i_score.lower()].append(1)
    # This will probably have to be copypasted in almost every level
    char_data["levels"].append("BARBARIAN 4")

def barbarian_level_5(char_data: dict):
    char_data["hit_die"].append("d12")
    char_data["class_features"]["Extra Attack"] = {
        "description": "Beginning at 5th level, you can attack twice, instead of once, whenever you take the Attack action on your turn.",
        "glance": "2 attacks/turn",
        "uses total": -1,
        "uses available": -1,
        "timeframe": "n/a"
    }
    char_data["class_features"]["Fast Movement"] = {
        "description": "Starting at 5th level, your speed increases by 10 feet while you aren't wearing heavy armor.",
        "glance": "speed +10",
        "uses total": -1,
        "uses available": -1,
        "timeframe": "n/a"
    }
    # We might actually have to do something with this. 
    char_data["movement"]["walking"] += 10
    char_data["levels"].append("BARBARIAN 5")

def barbarian_level_6(char_data: dict):
    pass

def barbarian_level_7(char_data: dict):
    pass

def barbarian_level_8(char_data: dict):
    pass

def barbarian_level_9(char_data: dict):
    pass

def barbarian_level_10(char_data: dict):
    pass

def barbarian_level_11(char_data: dict):
    pass

def barbarian_level_12(char_data: dict):
    pass

def barbarian_level_13(char_data: dict):
    pass

def barbarian_level_14(char_data: dict):
    pass

def barbarian_level_15(char_data: dict):
    pass

def barbarian_level_16(char_data: dict):
    pass

def barbarian_level_17(char_data: dict):
    pass

def barbarian_level_18(char_data: dict):
    pass

def barbarian_level_19(char_data: dict):
    pass

def barbarian_level_20 (char_data: dict):
    pass

# Now how should subclasses work?
def barbarian_sc_berserker_3 (char_data: dict):
    char_data["class_features"]["Frenzy (Path of the Berserker)"] = {
        "description": "Starting when you choose this path at 3rd level, you can go into a frenzy when you rage. If you do so, for the duration of your rage you can make a single melee weapon attack as a bonus action on each of your turns after this one. When your rage ends, you suffer one level of exhaustion (as described in appendix PH-A).",
        "glance": "while raging, make an extra attack as a bonus action. Suffer +1 exhaustion after the rage",
        "uses total": -1,
        "uses available": -1,
        "timeframe": "n/a"
    }
    char_data["levels"].append("BARBARIAN-SC-BERSERKER 3")

def barbarian_sc_berserker_6 (char_data: dict):
    pass

def barbarian_sc_berserker_10 (char_data: dict):
    pass

def barbarian_sc_berserker_14 (char_data: dict):
    pass
