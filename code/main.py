import curses
from screen import CombatScreen
from Character import Character

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # Create instances
    testScreen = CombatScreen()
    testCharacter = Character("/home/lurch5-64/progamming/1wis-30int/test_character_data.json")

    # Render and draw
    testScreen.render(testCharacter)
    testScreen.draw(stdscr)

    # Refresh the screen to show the changes
    stdscr.refresh()

    # Wait for user input before exiting
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)