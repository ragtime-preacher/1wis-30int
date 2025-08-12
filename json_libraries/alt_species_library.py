# Maybe they're trying something different!
# low key I am. But hold the phone - it might not work.
# UPDATE: it totally did. get owned

from easygui import choicebox

import faca

# TODO FOR ALL
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
    char_data["languages"].append ("common")
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
    char_data["species_traits"]["Fey Ancestry"] = {
        "description": "You have advantage on saving throws against being charmed, and magic can't put you to sleep.",
        "glance": "immune to magical sleep",
        "uses total": -1,
        "uses available": -1,
        "timeframe": "n/a",
    }
    # trance
    char_data["species_traits"]["Trance"] = {
        "description": "Elves don't need to sleep. Instead, they meditate deeply, remaining semiconscious, for 4 hours a day. (The Common word for such meditation is \"trance.\") While meditating, you can dream after a fashion; such dreams are actually mental exercises that have become relflexive through years of practice. After resting in this way, you gain the same benefit that a hunman does from 8 hours of sleep.",
        "glance": "you have 4 hours of every long rest to do whatever you want",
        "uses total": -1,
        "uses available": -1,
        "timeframe": "n/a"
    }
    char_data["languages"].append ("elvish")
    char_data["languages"].append ("common")
    chosen_subspecies = "high elf"
    match chosen_subspecies:
        case "high elf" | None:
            char_data["species"] = "high elf"
            char_data["stat_mods"]["int"].append (1)
            char_data["prof_weapons"].extend (["longsword, shortsword, shortbow, longbow"])
            char_data["cantrips_known"].append (faca.choose_spell(0, "wizard", "pick a cantrip bro"))
            # language-choosing nightmare
            char_data["languages"].append (faca.choose_language("pick an additional language:", char_data["languages"]))
    # other elf cases

def spe_halfling (char_data: dict):
    char_data["stat_mods"]["dex"].append(2)
    char_data["age"] = faca.choose_age("A halfling reaches adulthood at the age of 20 and generally lives into the middle of his or her second century.")
    char_data["alignment"] = faca.choose_alignment("Most halflings are lawful good. As a rule, they are good-hearted and kind, hate to see others in pain, and have no tolerance for oppression. They are also very orderly and traditional, leaning heavily on the support of their community and the comfort of their old ways.")
    char_data["size"] = "Small"
    char_data["movement"]["walking"] = 25
    # lucky
    char_data["species_traits"]["Halfling Lucky"] = {
        "description": "When you roll a 1 on the d20 for an attack roll, ability check, or saving throw, you can reroll the die and must use the new roll.",
        "glance": "re-roll nat 1s",
        "uses total": -1,
        "uses available": -1,
        "timeframe": "n/a",
    }
    char_data["st_notes"].append ("ADV vs fear")
    # halfling nimbleness
    char_data["species_traits"]["Halfling Nimbleness"] = {
        "description": "You can move through the space of any creature that is of a size larger than yours.",
        "glance": "walk under the legs",
        "uses total": -1,
        "uses available": -1,
        "timeframe": "n/a",
    }
    char_data["languages"].append ("halfling")
    char_data["languages"].append ("common")
    chosen_subspecies = "lightfoot"
    match chosen_subspecies:
        case "lightfoot" | None:
            char_data["species"] = "lightfoot halfling"
            char_data["stat_mods"]["cha"].append(1)
            char_data["species_traits"]["Naturally Stealthy"] = {
                "description": "You can attempt to hide even when you are obscured only by a creature that is at least one size larger than you.",
                "glance": "hide behind taller people",
                "uses total": -1,
                "uses available": -1,
                "timeframe": "n/a",
            }

def spe_human (char_data: dict):
    char_data["species"] = "human"
    for i_stat in char_data["stat_mods"]:
        i_stat.append(1)
    char_data["age"] = faca.choose_age("Humans reach adulthood in their late teens and live less than a century.")
    char_data["alignment"] = faca.choose_alignment("Humans tend toward no particular alignment. The best and the worst are found among them.")
    char_data["size"] = "Medium"
    char_data["movement"]["walking"] = 30
    char_data["languages"].append ("common")
    char_data["languages"].append(faca.choose_language("pick one non-common language", "common"))

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
    # Pseudocode: CHOOSE draconic ancestry
    #   figure out some details to substitute into the description
    draconic_damage_types = {
        "Black": "acid",
        "Blue": "lightning",
        "Brass": "fire",
        "Bronze": "lightning",
        "Copper": "acid",
        "Gold": "fire",
        "Green": "poison",
        "Red": "fire",
        "Silver": "cold",
        "White": "cold"
    }
    breath_shapes = {
        "Black": "5 by 30 ft. line",
        "Blue": "5 by 30 ft. line",
        "Brass": "5 by 30 ft. line",
        "Bronze": "5 by 30 ft. line",
        "Copper": "5 by 30 ft. line",
        "Gold": "15 ft. cone",
        "Green": "15 ft. cone",
        "Red": "15 ft. cone",
        "Silver": "15 ft. cone",
        "White": "15 ft. cone"
    }
    ancestry = str(choicebox(
        msg="Select Draconic Ancestry:",
        title="draconic ancestry",
        choices=draconic_damage_types.keys()
    ))
    if ancestry == None:
        ancestry = "Red" # default
    st_type = "DEX"
    if ancestry in ["Green", "Silver", "White"]: st_type = "CON"
    char_data["species_traits"]["Breath Weapon"] = {
        "description": f"You can use your action to exhale destructive energy. When you use your breath weapon, each creature in the area of the exhalation must make a saving throw. The DC for this saving throw equals 8 + your Constitution modifier + your proficiency bonus. A creature takes 2d6 damage on a failed save, and half as much on a successful one. The damage increases to 3d6 at 6th level, 4d6 at 11th level, and 5d6 at 16th level.",
        "glance": f"Use an action to breathe a {breath_shapes[ancestry]} in front of you. Each creature in the blast must make a {st_type} ST, DC %8+CON+PB. 2d6 {draconic_damage_types[ancestry]} damage on a fail, or half as much on success.",
        "uses total": 1,
        "uses available": 1,
        "timeframe": "shortrest",
        "DC": 0, # TODO assign this
        "damage": "2d6" # TODO somehow update this based on level?
    }
    char_data["species"] = f"dragonborn ({ancestry})"
    char_data["resistances"][draconic_damage_types[ancestry]] = 0.5
    char_data["languages"].append("draconic")
    char_data["languages"].append ("common")
    

def spe_gnome (char_data: dict):
    char_data["stat_mods"]["int"].append(2)
    char_data["age"] = faca.choose_age("Gnomes mature at the same rate humans do, and most are expected to settle down into an adult life by around age 40. They can live 350 to almost 500 years.")
    char_data["alignment"] = faca.choose_alignment("Gnomes are most often good. Those who tend toward law are sages, engineers, researchers, scholars, investigators, or inventors. Those who tend toward chaos are minstrels, tricksters, wanderers, or fanciful jewelers. Gnomes are good-hearted, and even the tricksters among them are more playful than vicious.")
    char_data["size"] = "Small"
    char_data["movement"]["walking"] = 25
    char_data["senses"]["darkvision"] = 60
    char_data["st_notes"].append ("ADV w/ int, wis, cha vs magic")
    char_data["languages"].append("gnomish")
    char_data["languages"].append ("common")
    chosen_subspecies = "rock gnome"
    match chosen_subspecies:
        case "rock gnome" | None:
            char_data["species"] = "rock gnome"
            char_data["stat_mods"]["con"].append(1)
            char_data["species_traits"]["Artificer's Lore"] = {
                "description": "Whenever you make an Intelligence (history) check related to magic items, alchemical objects, or technological devices, you can add twice your proficiency bonus, instead of any proficiency bonus you normally apply.",
                "glance": "expertise in History about magic items, alchemical stuff, or technology.",
                "uses total": -1,
                "uses available": -1,
                "timeframe": "n/a",
            }
            char_data["species_traits"]["Tinker"] = {
                "description": "You have proficiency with artisan's tools (tinker's tools). Using those tools, you can spend 1 hour and 10 gp worth of materials to construct a Tiny clockwork device (AC 5, 1 hp). The device ceases to function after 24 hours (unless you spend 1 hour repairing it to keep the device functioning), or when you use your action to dismantle it; at that time, you can reclaim the materials used to create it. You can have up to three such devices active at a time.",
                "glance": "spend 1 hour and 10 GP of stuff to make a contraption",
                "uses total": -1,
                "uses available": -1,
                "timeframe": "n/a",
            }

def spe_halfelf (char_data: dict):
    char_data["species"] = "half-elf"
    char_data["stat_mods"]["cha"].append(2)
    first_stat = faca.choose_ability_score("choose one ability score to increase by 1:", ["Charisma"])
    second_stat = faca.choose_ability_score("choose a different ability score to increase by 1:", ["Charisma", first_stat])
    char_data["stat_mods"][first_stat[0:3].lower()].append(1)
    char_data["stat_mods"][second_stat[0:3].lower()].append(1)
    char_data["age"] = faca.choose_age("Half-elves mature at the same rate humans do and reach adulthood around the age of 20. They live much longer than humans, however, often exceeding 180 years.")
    char_data["alignment"] = faca.choose_alignment("Half-elves share the chaotic bent of their elven heritage. They value both personal freedom and creative expression, demonstrating neither love of leaders nor desire for followers. They chafe at rules, resent others' demands, and sometimes prove unreliable, or at least unpredictable.")
    char_data["size"] = "Medium"
    char_data["movement"]["walking"] = 30
    char_data["senses"]["darkvision"] = 60
    char_data["st_notes"].append("ADV vs being charmed")
    char_data["species_traits"]["Fey Ancestry"] = {
        "description": "You have advantage on saving throws against being charmed, and magic can't put you to sleep.",
        "glance": "immune to magical sleep",
        "uses total": -1,
        "uses available": -1,
        "timeframe": "n/a",
    }
    skills_to_ignore = []
    for i_skill in  char_data["skills"].keys():
        if char_data["skills"][i_skill] >= 1.0:
            skills_to_ignore.append(i_skill)
    first_skill = faca.choose_skill("pick a skill:", skills_to_ignore)
    skills_to_ignore.append(first_skill)
    second_skill = faca.choose_skill("pick another skill", skills_to_ignore)
    char_data["skills"][first_skill] = 1.0
    char_data["skills"][second_skill] = 1.0
    char_data["languages"].append("elvish")
    char_data["languages"].append ("common")
    char_data["languages"].append(faca.choose_language("pick one language beyond common and elvish:", ["common", "elvish"]))

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
    char_data["species_traits"]["Relentless Endurance"] = {
        "description": "When you are reduced to 0 hit points but not killed outright, you can drop to 1 hit point instead. You can't use this feature again until you finish a long rest.",
        "glance": "Drop to 1 HP instead of 0",
        "uses total": 1,
        "uses available": 1,
        "timeframe": "longrest",
    }
    char_data["species_traits"]["Savage Attacks"] = {
        "description": "When you score a critical hit with a melee weapon attack, you can roll one of the weapon's damage dice one additional time and add it to the extra damage of the critical hit.",
        "glance": "Roll 1 extra dice when you crit",
        "uses total": -1,
        "uses available": -1,
        "timeframe": "n/a",
    }
    char_data["languages"].append ("orc")
    char_data["languages"].append ("common")

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
    char_data["languages"].append ("common")


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