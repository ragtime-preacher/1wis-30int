# Maybe they're trying something different!
# low key I am. But hold the phone - it might not work.

from easygui import choicebox

import faca

# TODO FOR ALL
#   add common as a known language
#   add the species traits

def spe_dwarf (char_data: dict):
    # for the dwarf, we'll label our species in the subrace selection.
    # Stat Increase (both subraces have the CON+2)
    char_data["stat_mods"]["con"].append(2)
    # Age (mostly flavor in any case, unless you're an aaracokra and get spooked by a ghost)
    char_data["age"] = faca.choose_age ("Dwarves mature at the same rate as humans, but they're considered young until they reach the age of 50. On average, they live about 350 years.")
    char_data["alignment"] = faca.choose_alignment("Most dwarves are lawful, believing firmly in the benefits of a well-ordered society. They tend towards good as well, with a strong sense of fair play and a belief that everyone deserves to share in the benefits of a just order.")
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
Posting this code as it is now (including non-SRD character options) 
onto Github for public consumption would be a violation of copyright
law and therefore ILEGAL. DON'T DO IT.

For deployment, I'll probably have to include the match statement code commented out
    so that big-time nerds (i.e. the intended users of this program) who want to add the subraces they know and love can do
    so without too much re-writing, while preventing WotC from casting disintegrate
    on my future.
        """
    # chosen_subspecies = choicebox ("now son, there's roughly speaking two kinds of dwarves: hill dwarves and dwarves that it's ilegal for me to talk about.", choices=["hill dwarf", "ilegal dwarves"])
    chosen_subspecies = "hill dwarf"
    match chosen_subspecies:
        
        case "hill dwarf" | None: # | None marks this as the default if they close out. Hopefully.
            char_data["species"] = "hill dwarf"
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
    char_data["alignment"] = faca.choose_alignment("Elves love freedom, variety, and self-expression, so they lean strongly toward the gentler aspects of chaos. They value and protect others' freedom as well as their own, and they are more often good than not.")
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
            char_data["species"] = "high elf"
            char_data["stat_mods"]["int"].append (1)
            char_data["prof_weapons"].extend (["longsword, shortsword, shortbow, longbow"])
            char_data["cantrips_known"].append (faca.choose_spell(0, "wizard", "pick a cantrip bro"))
            # language-choosing nightmare
    # other elf cases

def spe_halfling (char_data: dict):
    char_data["stat_mods"]["dex"].append(2)
    char_data["age"] = faca.choose_age("A halfling reaches adulthood at the age of 20 and generally lives into the middle of his or her second century.")
    char_data["alignment"] = faca.choose_alignment("Most halflings are lawful good. As a rule, they are good-hearted and kind, hate to see others in pain, and have no tolerance for oppression. They are also very orderly and traditional, leaning heavily on the support of their community and the comfort of their old ways.")
    char_data["size"] = "Small"
    char_data["movement"]["walking"] = 25
    # lucky notes
    char_data["st_notes"].append ("ADV vs fear")
    # halfling nimbleness
    char_data["languages"].append ("halfling")
    chosen_subspecies = "lightfoot"
    match chosen_subspecies:
        case "lightfoot" | None:
            char_data["species"] = "lightfoot halfling"
            char_data["stat_mods"]["cha"].append(1)
            # TODO naturally stealthy

def spe_human (char_data: dict):
    char_data["species"] = "human"
    for i_stat in char_data["stat_mods"]:
        i_stat.append(1)
    char_data["age"] = faca.choose_age("Humans reach adulthood in their late teens and live less than a century.")
    char_data["alignment"] = faca.choose_alignment("Humans tend toward no particular alignment. The best and the worst are found among them.")
    char_data["size"] = "Medium"
    char_data["movement"]["walking"] = 30
    char_data["languages"].append(faca.choose_language("pick one non-common language"))

def spe_dragonborn (char_data: dict):
    # even though dragonborn don't have a subspecies,
    #   the draconic ancestry almost counts. I'll include that in the
    #   species name, and assign it once the color is chosen.
    char_data["stat_mods"]["str"].append(2)
    char_data["stat_mods"]["cha"].append(1)
    char_data["age"] = faca.choose_age("Young dragonborn grow quickly. They walk hours after hatching, attain the size and development of a 10-year-old human child by the age of 3, and reach adulthood by 15. They live to be around 80.")
    char_data["alignment"] = faca.choose_alignment("Dragonborn tend to extremes, making a conscious choice for one side or the other in the cosmic war between good and evil. Most dragonborn are good, but those who side with evil can be terrible villains.")
    char_data["size"] = "Medium"
    char_data["movement"]["walking"] = 30
    # TODO: draconic ancestry, damage resistance, breath weapon
    ancestry = "i dunno gold I guess"
    char_data["species"] = f"dragonborn ({ancestry})"
    char_data["languages"].append("draconic")
    

def spe_gnome (char_data: dict):
    char_data["stat_mods"]["int"].append(2)
    char_data["age"] = faca.choose_age("Gnomes mature at the same rate humans do, and most are expected to settle down into an adult life by around age 40. They can live 350 to almost 500 years.")
    char_data["alignment"] = faca.choose_alignment("Gnomes are most often good. Those who tend toward law are sages, engineers, researchers, scholars, investigators, or inventors. Those who tend toward chaos are minstrels, tricksters, wanderers, or fanciful jewelers. Gnomes are good-hearted, and even the tricksters among them are more playful than vicious.")
    char_data["size"] = "Small"
    char_data["movement"]["walking"] = 25
    char_data["senses"]["darkvision"] = 60
    char_data["st_notes"].append ("ADV w/ int, wis, cha vs magic")
    char_data["languages"].append("gnomish")
    chosen_subspecies = "rock gnome"
    match chosen_subspecies:
        case "rock gnome" | None:
            char_data["species"] = "rock gnome"
            char_data["stat_mods"]["con"].append(1)
            # TODO artificer's lore
            # TODO tinker

def spe_halfelf (char_data: dict):
    char_data["species"] = "half-elf"
    char_data["stat_mods"]["cha"].append(2)
    # TODO choose others to increase
    char_data["age"] = faca.choose_age("Half-elves mature at the same rate humans do and reach adulthood around the age of 20. They live much longer than humans, however, often exceeding 180 years.")
    char_data["alignment"] = faca.choose_alignment("Half-elves share the chaotic bent of their elven heritage. They value both personal freedom and creative expression, demonstrating neither love of leaders nor desire for followers. They chafe at rules, resent others' demands, and sometimes prove unreliable, or at least unpredictable.")
    char_data["size"] = "Medium"
    char_data["movement"]["walking"] = 30
    char_data["senses"]["darkvision"] = 60
    char_data["st_notes"].append("ADV vs being charmed")
    # TODO magic can't put you to sleep
    # TODO choose 2 skills to be proficient in
    char_data["languages"].append("elvish")
    char_data["languages"].append(faca.choose_language("pick one language beyond common and elvish:"))

def spe_halforc (char_data: dict):
    char_data["species"] = "half-orc"
    char_data["stat_mods"]["str"].append(2)
    char_data["stat_mods"]["con"].append(1)
    char_data["age"] = faca.choose_age("Half-orcs mature a little faster than humans, reaching adulthood around age 14. They age noticeably faster and rarely live longer than 75 years.")
    char_data["alignment"] = faca.choose_alignment("Half-orcs inherit a tendency toward chaos from their orc parents and are not strongly inclined toward good. Half-orcs raised among orcs and willing to live out their lives among them are usually evil.")
    char_data["size"] = "Medium"
    char_data["movement"]["walking"] = 30
    char_data["senses"]["darkvision"] = 60
    char_data["skills"]["intimidation"] = 1
    # TODO relentless endurance
    # TODO savage attacks
    char_data["languages"].append ("orc")

def spe_tiefling (char_data: dict):
    char_data["species"] = "tiefling"
    char_data["stat_mods"]["int"].append(1)
    char_data["stat_mods"]["cha"].append(2)
    char_data["age"] = faca.choose_age("Tieflings mature at the same rate as humans but live a few years longer.")
    char_data["alignment"] = faca.choose_alignment("Tieflings might not have an innate tendency toward evil, but many of them end up there. Evil or not, and independent nature inclines many tieflings toward a chaotic alignment.")
    char_data["size"] = "Medium"
    char_data["movement"]["walking"] = 30
    char_data["senses"]["darkvision"] = 60
    char_data["resistances"]["fire"] = 0.5
    # TODO infernal legacy
    char_data["languages"].append("infernal")


SPECIES_DICTIONARY = {
    "DWARF": spe_dwarf,
    "ELF": spe_elf,
    "HALFLING": spe_halfling,
    "HUMAN": spe_human,
    "DRAGONBORN": spe_dragonborn,
    "GNOME": spe_gnome,
    "HALF-ELF": spe_halfelf,
    "HALF-ORC": spe_halforc,
    "TIEFLING": spe_tiefling
}