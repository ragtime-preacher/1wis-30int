import curses
from screen import HomeScreen, StatScreen, CombatScreen, SkillScreenPAS, SkillScreenABS
from Character import Character
from screenmanager import ScreenManager

def main(stdscr):
    testCharacter = Character ("/home/lurch5-64/progamming/1wis-30int/test_character_data.json")
    manager = ScreenManager (
        stdscr=stdscr,
        source=testCharacter,
        screens=[
            HomeScreen(),
            StatScreen(),
            CombatScreen(),
            SkillScreenPAS(),
            SkillScreenABS()
        ]
    )
    manager.mainloop ()

if __name__ == "__main__":
    curses.wrapper(main)