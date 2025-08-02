# Frequently Accessed Character Attributes
# (FACA, or 'knife' in portuguese)

from easygui import integerbox, choicebox

def choose_age (flavor: str) :
    chosen_age = integerbox(flavor, default=25, lowerbound=0)
    return chosen_age

def choose_language (flavor: str) :
    chosen_language = choicebox(
        msg=flavor,
        title="Language selection",
        choices=[
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
    )
    return chosen_language

# TODO
# spell_list defaults to wizard. Argue one or more
#   levels of spells (0 = cantrip) to narrow the choices.
def choose_spell (levels: list[int] | int, spell_list: str, flavor: str):
    return "eldritch heckin' blast"

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