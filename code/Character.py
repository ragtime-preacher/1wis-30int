# Character class

# In theory, contains everything that a character needs to have in order
#   to be played in Dnd.

from Attribute import Attribute

class Character:
    def __init__(self,
                 character_name: str,
                 character_species,
                 character_alignment: str,
                 character_background: str):
        self.name = ""
        self.species = ""
        self.size = ""
        self.alignment = ""
        self.background = ""
        self.current_xp = 0 

        self.stat_str = Attribute(0)
        self.stat_dex = Attribute(0)
        self.stat_con = Attribute(0)
        self.stat_int = Attribute(0)
        self.stat_wis = Attribute(0)
        self.stat_cha = Attribute(0)

        self.inspiration = False
        
        self.prof_bonus = 2

        # saving throws
        self.prof_st_str = False
        self.prof_st_dex = False
        self.prof_st_con = False
        self.prof_st_int = False
        self.prof_st_wis = False
        self.prof_st_cha = False

        self.prof_weapons = []
        self.prof_armor = []

        # Racial traits
        self.species_traits = []

        # skills
        #   Jack of All Trades will be handled seperately.
        self.prof_skills = []
        self.exp_skills = []

        self.prof_tools = []
        self.languages = []

        # combat data
        self.ac = 10
        self.initiative = self.stat_dex.value
        self.speed = {
                "walking": 30,
                "flying": 0,
                "swimming": 0,
                "climbing": 0,
                "burrowing": 0
                }
        self.hp_max = 1
        self.hp_current = self.hp_max
        self.hit_die = []

        self.attacks = []
        self.equipment = []
        self.money = 0 # measured in copper pieces
        self.resistences = []

        # roleplaying stuff
        self.rp_personality_traits = []
        self.rp_ideals = []
        self.rp_bonds = []
        self.rp_flaws = []
        
        self.rp_appearance = []
        self.rp_backstory = []
        self.rp_allies = []
        self.rp_organizations = []
        self.rp_characteristics = []
        self.rp_treasures = []

        # Gameplaying stuff
        self.class_features = []
        self.feats = []

        # Spellcasting (ugh)
        self.sc_stat = None
        self.sc_dc = 10
        self.dc_attack_bonus = 0

        self.sc_spells_known = []
        self.sc_spells_prep = []
        self.sc_slots = {
                "1st": 0,
                "2nd": 0,
                "3rd": 0,
                "4th": 0,
                "5th": 0,
                "6th": 0,
                "7th": 0,
                "8th": 0,
                "9th": 0
                }


