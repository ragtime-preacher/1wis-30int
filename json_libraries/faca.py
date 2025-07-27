# Frequently Accessed Character Attributes
# (FACA, or 'knife' in portuguese)

from easygui import integerbox, choicebox

def choose_age (flavor: str) :
    chosen_age = integerbox(flavor, default=25, lowerbound=0)
    return chosen_age

def choose_language (flavor: str) :
    chosen_language = "portuguese" # TODO: actually choose languages
    return chosen_language

# spell_list defaults to wizard. Argue one or more
#   levels of spells (0 = cantrip) to narrow the choices.
def choose_spell (levels: list[int] | int, spell_list: str, flavor: str):
    return "eldritch heckin' blast"