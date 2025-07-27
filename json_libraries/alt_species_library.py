# Maybe they're trying something different!
# low key I am. But hold the phone - it might not work.

from easygui import choicebox

import faca

def spe_dwarf (char_data: dict):
    # Stat Increase (both subraces have the CON+2)
    char_data["stat_mods"]["con"].append(2)
    # Age (mostly flavor in any case, unless you're an aaracokra and get spooked by a ghost)
    char_data["age"] = faca.choose_age ("Dwarves mature at the same rate as humans, but they're considered young until they reach the age of 50. On average, they live about 350 years.")
    # Size
    char_data["size"] = "Medium"
    # Speed (or speeds)
    # it's important to note here that a dwarf's speed isn't reduced by heavy armor.
    #   not sure where mechanically I would make a note of this in the ICS, but
    #   I'll feel bad if I don't mention it somewhere. you're welcome.
    char_data["movement"]["walking"] = 25
    # Senses (mostly darkvision)
    char_data["senses"]["darkvision"] = 60
    # Poison resistance
    char_data["st_notes"].append ("ADV vs poison")
    char_data["resistances"]["poison"] = 0.5
    # Dwarven combat training
    char_data["prof_weapons"].extend (["battleaxe, handaxe, light hammer, warhammer"])
    # tool proficiency (time to make a choice)
    chosen_tool_proficiency = choicebox ("", choices=["brewer's supplies", "smith's tools", "mason's tools"])
    if chosen_tool_proficiency == None: # failsafe
        chosen_tool_proficiency = "smith's tools"
    char_data["prof_tools"].append (chosen_tool_proficiency)
    # stonecunning is not appropriate to include mechanically
    # language
    char_data["languages"].append ("dwarvish")
    # This is where the fun begins... subspecies!
    """
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
IMPORTANT
Posting this code as it is now onto Github for public consumption would be
a violation of copyright law and therefore ILEGAL. DON'T DO IT.
I'll probably create a private version.

For deployment, I'll probably have to include the match statement code commented out
    so that big-time nerds (i.e. the intended users of this program) who want to add the subraces they know and love can do
    so without too much re-writing, while preventing WotC from breathing fire
    down my neck.
        """
    # chosen_subspecies = choicebox ("now son, there's roughly speaking two kinds of dwarves: hill dwarves and dwarves that it's ilegal for me to talk about.", choices=["hill dwarf", "ilegal dwarves"])
    chosen_subspecies = "hill dwarf"
    match chosen_subspecies:
        
        case "hill dwarf" | None: # | None marks this as the default if they close out. Hopefully.
            char_data["stat_mods"]["wis"].append(1)
            char_data["hp_mod_per_level"] += 1
        case "ilegal dwarves":
            # other dwarf stuff (STR +2, psionic resistance, etc.)
            pass
        case _:
            # uhhhh what
            pass

def spe_elf (char_data: dict):
    # all elves get the nifty +2 dex. It's kinda OP ngl
    char_data["stat_mods"]["dex"].append(2)
    char_data["age"] = faca.choose_age("Although elves reach physical maturity at about the same age as humans, the elven understanding of adulthood goes beyond physical growth to encompass worldly experience. An elf typically claims adulthood and an adult name around the age of 100 and can live to be 750 years old.")
    char_data["size"] = "Medium"
    char_data["movement"]["walking"] = 30
    char_data["senses"]["darkvision"] = 60
    char_data["skills"]["perception"] = 1
    char_data["st_notes"].append ("ADV vs being charmed")
    # magic can't put you to sleep
    # trance
    char_data["languages"].append ("elvish")
    chosen_subspecies = "high elf"
    match chosen_subspecies:
        case "high elf" | None:
            char_data["stat_mods"]["int"].append (1)
            char_data["prof_weapons"].extend (["longsword, shortsword, shortbow, longbow"])
            char_data["cantrips_known"].append (faca.choose_spell(0, "wizard", "pick a cantrip bro"))
            # language-choosing nightmare
    pass

SPECIES_DICTIONARY = {
    "DWARF": spe_dwarf,
    "ELF": spe_elf
}