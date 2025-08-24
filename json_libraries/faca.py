# Frequently Accessed Character Attributes
# (FACA, or 'knife' in portuguese)

from easygui import integerbox, choicebox, enterbox, multenterbox
import json

def choose_age (flavor: str) :
    chosen_age = integerbox(flavor, default=25, lowerbound=0)
    return chosen_age

def choose_language (flavor: str, ignore: list[str] | str = "Common") :
    if type(ignore) == list:
        ignore_list = [lang_to_ignore.casefold() for lang_to_ignore in ignore]
    elif type(ignore) == str:
        ignore_list = [ignore.casefold()]

    lang_list = [
            # standard languages
            "Common",
            "Dwarvish",
            "Elvish",
            "Giant",
            "Gnomish",
            "Goblin",
            "Halfling",
            "Orc",
            # exotic languages
            "Abyssal",
            "Celestial",
            "Draconic",
            "Deep Speech",
            "Infernal",
            "Primordial",
            "Sylvan",
            "Undercommon"
        ]
    chosen_language = choicebox(
        msg=flavor,
        title="Language selection",
        choices=[lang for lang in lang_list if lang.casefold() not in ignore_list]
    )
    return chosen_language

# TODO choose n spells with a multibox, allow for multiple spell lists
#   TODO (maybe) show only spells from certain schools of magic
# spell_list defaults to wizard. Argue one or more
#   levels of spells (0 = cantrip) to narrow the choices.
# NOTE
#   So it turns out that Easygui doesn't have functionality to 
#       limit the user to n choices in a multchoicebox.
#   It is therefore possible that I'll eventually have to do a total
#       overhaul of this ui using something like tkinter.
#   que paia.
def choose_spell (levels: list[int] | int, spell_list: str, flavor: str):
    chosen_spell = choicebox(
        msg=flavor,
        title=f"spell selection: {spell_list}",
        choices=spell_filter(levels, spell_list)
    )
    return chosen_spell

# internal use only
# argue 0 for cantrips.
def spell_filter (spell_levels: list[int] | int, spell_list: str) -> list[str]:
    # this dictionary is to help me interface with the spell library's format
    json_ordinals = {
        0: "Cantrip",
        1: "1st-level",
        2: "2nd-level",
        3: "3rd-level",
        4: "4th-level",
        5: "5th-level",
        6: "6th-level",
        7: "7th-level",
        8: "8th-level",
        9: "9th-level"
    }
    spell_library_filename = "/home/feijao/programming/1wis-30int/json_libraries/efficient_spell_library.json"
    spell_library = open(spell_library_filename)
    spell_dict = json.load(spell_library)
    spell_library.close()
    found_spells = []
    for i_spell in spell_dict.keys():
        # first filter out by spell list
        if spell_list.casefold() not in spell_dict[i_spell]["class"].casefold():
            # this spell isn't on our spell list.
            continue # on to the next one
        if type(spell_levels) == int:
            if spell_dict[i_spell]["level"] != json_ordinals[spell_levels]:
                # this isn't the right level.
                continue
        elif type(spell_levels) == list:
            if spell_dict[i_spell]["level"] not in [json_ordinals[i_level] for i_level in spell_levels]:
                # not one of the right levels.
                continue
        # if we made it this far, the spell must line up with our criteria.
        found_spells.append(i_spell)
    if len(found_spells) == 0:
        # for some reason, we didn't find anything. We'll add truly
        #   the most devestating of spells
        found_spells.append("FILTER ERROR: no spells found")
    return found_spells

# maybe adjust this so alignment is so wordy. Or maybe not.
#   alignment in 5e is largely optional anyway, so it probably doesn't matter that much.
def choose_alignment (flavor: str) :
    alignment_options = {
        "LG": "Lawful good creatures can be counted on to do the right thing as expected by society.",
        "NG": "Neutral good folk do the best they can to help others according to their needs.",
        "CG": "Chaotic good creatures act as their conscience directs, with little regard for what others expect.",
        "LN": "Lawful neutral individuals act in accordance with law, tradition, or personal codes.",
        "N" : "Neutral is the alignment of those who prefer to steer clear of moral questions and don't take sides, doing what seems best at the time.",
        "CN": "Chaotic neutral creatures follow their whims, holding their personal freedom above all else.",
        "LE": "Lawful evil creatures methodically take what they want, within the limits of a code or tradition, loyalty, or order.",
        "NE": "Neutral evil is the alignment of those who do whatever they can get away with, without compassion or qualms.",
        "CE": "Chaotic evil creatures act with arbitrary violence, spurred by their greed, hatred, or bloodlust."
    }
    chosen_alignment = choicebox(
        msg=flavor,
        title="alignemnt",
        choices=[f"{alignment_key}: {alignment_options[alignment_key]}" for alignment_key in alignment_options.keys()],
        preselect=4
    )
    return chosen_alignment

def choose_ability_score (flavor: str, ignore: list[str] | str):
    if type(ignore) == list:
        ignore_list = [stat_to_ignore.casefold() for stat_to_ignore in ignore]
    elif type(ignore) == str:
        ignore_list = [ignore.casefold()]

    stat_list = [
        "Strength",
        "Dexterity",
        "Constitution",
        "Intelligence",
        "Wisdom",
        "Charisma"
    ]
    chosen_ability_score = str(choicebox(
        msg=flavor,
        title="Ability Score selection",
        choices=[stat for stat in stat_list if stat.casefold() not in ignore_list]
    ))
    if chosen_ability_score == None:
        chosen_ability_score = "Dexterity"
    return chosen_ability_score

def choose_skill (flavor: str, ignore: list[str] | str, include: list[str] | None):
    if type(ignore) == list:
        ignore_list = [i_skill.casefold() for i_skill in ignore]
    elif type(ignore) == str:
        ignore_list = [ignore.casefold()]
    skill_list = [
        "Acrobatics",
        "Animal Handling",
        "Arcana",
        "Athletics",
        "Deception",
        "History",
        "Insight",
        "Intimidation",
        "Investigation",
        "Medicine",
        "Nature",
        "Perception",
        "Performance",
        "Persuasion",
        "Religion",
        "Sleight of Hand",
        "Stealth",
        "Survival"
]
    if (include != None) and (len(include) > 0):
        skill_list = include
    chosen_skill = choicebox (
        msg=flavor,
        title="skill selection",
        choices = [skill.lower() for skill in skill_list if skill.casefold() not in ignore_list]
    )
    return chosen_skill

def choose_name ():
    name = enterbox(
        msg="under what label will your character's heroic exploits be sung by generations yet unborn?",
        title="my least favorite part"
    )
    if name == None:
        name = "just a random guy"
    return name

def determine_stats () -> list[int]:
    stats_str = multenterbox (
        msg="pick your stats. Be honest now. Also please use integers or it will cause problems",
        title="the most important part :)",
        fields=["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"],
        values=["10" for i in range(6)]
    )
    if stats_str == None:
        stats_str = ["10" for i in range(6)]
    stats_int = []
    for i_stat in stats_str: # type: ignore
        try:
            stats_int.append(int(i_stat))
        except ValueError:
            # we ended up with something other than a string
            stats_int.append(10)
    return stats_int

def choose_weapon (
        weapon_class: str | None = 'all',
        weapon_range: str | None = 'all',
        custom: list[str] | None = None
    ) -> str:
    weapon_library = open ("/home/feijao/programming/1wis-30int/json_libraries/weapon_library.json")
    weapon_dict = json.load(weapon_library)
    weapon_library.close ()
    weapon_choices = []

# gotta love match statements
    match [weapon_class, weapon_range]:
        case ['all', 'all']:
            weapon_choices = weapon_dict.keys()
        case ['simple'|'martial', 'all'|None]:
            for i_weapon in weapon_dict.keys():
                if weapon_class in weapon_dict[i_weapon]["tags"]:
                    weapon_choices.append(i_weapon)
        case ['all'|None, 'melee'|'ranged']:
            for i_weapon in weapon_dict.keys():
                if weapon_range in weapon_dict[i_weapon]["tags"]:
                    weapon_choices.append(i_weapon)
        case ['simple'|'martial', 'melee'|'ranged']:
            for i_weapon in weapon_dict.keys():
                if weapon_class in weapon_dict[i_weapon]["tags"] and \
                    weapon_range in weapon_dict[i_weapon]["tags"]:
                    weapon_choices.append(i_weapon)
        case [None, None]:
            if type(custom) == list and len(custom) > 0:
                for i_weapon in custom:
                    if i_weapon in weapon_dict.keys():
                        weapon_choices.append(i_weapon)

# LEGACY (hopefully)
    # if weapon_class == 'all' and weapon_range == 'all':
    #     weapon_choices = weapon_dict.keys()

    # elif weapon_class != None and weapon_range in [None, 'all']:
    #     for i_weapon in weapon_dict.keys():
    #         if weapon_class in weapon_dict[i_weapon]["tags"]:
    #             weapon_choices.append(i_weapon)
        
    # elif weapon_class in [None, 'all'] and weapon_range != None:
    #     for i_weapon in weapon_dict.keys():
    #         if weapon_range in weapon_dict[i_weapon]["tags"]:
    #             weapon_choices.append(i_weapon)

    # elif weapon_class != None and weapon_range != None:
    #     for i_weapon in weapon_dict.keys():
    #         if weapon_class in weapon_dict[i_weapon]["tags"] and weapon_range in weapon_dict[i_weapon]["tags"]:
    #             weapon_choices.append(i_weapon)

    # elif weapon_class == None and weapon_range == None:
    #     if type(custom) == list and len(custom) > 0:
    #         for i_weapon in custom:
    #             if i_weapon in weapon_dict.keys():
    #                 weapon_choices.append(i_weapon)

    if len(weapon_choices) == 0:
        # there must have been some mistake. We'll default to everything
        # This should be a catch-all for any and all potential
        #   parameter problems.
        weapon_choices = weapon_dict.keys()

    chosen_weapon = choicebox(
        msg="choose a weapon",
        title="I recommend the really expensive ones, actually",
        choices=weapon_choices
    )
    if chosen_weapon == None:
        # x'd out
        chosen_weapon = "club"
    return str(chosen_weapon)

def ability_score_increase (current_scores: dict):
    # I think the best way to do this might be to just offer two +1 choices,
    #   allowing the user to choose the same ability score twice if they want.
    scores_to_mod = []
    f_current_scores = f"Strength: {current_scores["STR"]}\nDexterity: {current_scores["DEX"]}\nConstitution: {current_scores["CON"]}\nIntelligence: {current_scores["INT"]}\nWisdom: {current_scores["WIS"]}\nCharisma: {current_scores["CHA"]}"
    first_score = choicebox (
        msg=f"pick a score to +1:\n{f_current_scores}",
        title="con is never a bad option",
        choices=["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    )
    if first_score == None:
        first_score = "DEX"
    current_scores[first_score] += 1
    scores_to_mod.append(first_score)
    f_current_scores = f"Strength: {current_scores["STR"]}\nDexterity: {current_scores["DEX"]}\nConstitution: {current_scores["CON"]}\nIntelligence: {current_scores["INT"]}\nWisdom: {current_scores["WIS"]}\nCharisma: {current_scores["CHA"]}"
    second_score = choicebox (
        msg=f"pick another score to +1 (it can be the same as the first):\n{f_current_scores}",
        title="con is never a bad option",
        choices=["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    )
    if second_score == None:
        second_score = "DEX"
    scores_to_mod.append(second_score)
    # no need to update the scores to reflect our second choice, because that will be 
    #   handled by the ability score modifiers.
    return scores_to_mod



# some testing
def main () :
    print (choose_weapon(
        weapon_class='simple',
        weapon_range='melee',
    ))
    return 0

if __name__ == "__main__":
    main ()