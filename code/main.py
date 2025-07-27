import curses
from screen import HomeScreen, StatScreen, CombatScreen, SkillScreenPAS, SkillScreenABS, SpellScreen
from Character import Character
from screenmanager import ScreenManager

def main(stdscr):
    testCharacter = Character ("/home/feijao/programming/1wis-30int/code/test_character_data_with_spells.json")
    testCharacter._populate_spells()
    manager = ScreenManager (
        stdscr=stdscr,
        source=testCharacter,
        screens=[
            HomeScreen(),
            StatScreen(),
            CombatScreen(),
            SkillScreenPAS(),
            SkillScreenABS(),
            SpellScreen()
        ]
    )
    manager.mainloop ()

if __name__ == "__main__":
    curses.wrapper(main)
