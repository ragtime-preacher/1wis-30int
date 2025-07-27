# ScreenManager.py
#   The job of this screenmanager class is to contain a "game loop" that'll check for input.

import curses
from Character import Character
from screen import Screen
import shlex

class ScreenManager:
    def __init__ (self, stdscr, source: Character, screens: list[Screen]) :
        self.stdscr = stdscr
        self.source = source
        self.menu = screens
        assert len(self.menu) > 0
        self.current_screen = self.menu[0]
        self.handler = self.normal_mode
        self.command_buffer = ""
        self.current_message = ""

    def mainloop (self) :
        while True:
            # display the current screen (underneath all additions)
            self.current_screen.render (self.source)
            self.current_screen.draw (self.stdscr)
            # draw our message (if we have one)
            self.draw_message()
            # call our handler callback
            self.handler ()
            # Refresh the screen to show the changes
            curses.doupdate()
    
    def normal_mode (self) :
        self.draw_meta("NORMAL")
        # hide the cursor
        curses.curs_set(0)
        key = self.stdscr.getch()
        if key == ord(':'):
            self.handler = self.command_mode
            self.command_buffer = ""
        elif self.handle_scroll_input(key): return
        # other input handlers
    
    def command_mode (self) :
        self.draw_meta("COMMAND")
        # we want the cursor back
        curses.curs_set(1)
        # draw our command buffer to the bottom of the screen
        self.stdscr.addstr(curses.LINES - 1, 0, f":{self.command_buffer}")
        key = self.stdscr.getch() # get next keypress
        if key ==  curses.KEY_ENTER or key == 10:
            # erase the current message
            self.current_message = ""
            self.parse_command(self.command_buffer)
            self.handler = self.normal_mode
        elif key == 27: # ESC
            self.handler = self.normal_mode
            return
        elif key == curses.KEY_BACKSPACE or key == 127:
            # clip the last key off the buffer
            self.command_buffer = self.command_buffer[:-1]
        else:
            # add the key to the buffer
            self.command_buffer += chr(key)

    def parse_command (self, command: str) :
        command_buffer = shlex.split(command)
        if command in ["q", "quit", "exit"]:
            # make sure the cursor comes back
            curses.curs_set(1)
            exit ()
        elif command.startswith("switch "):
            if len(command_buffer) != 2:
                self.current_message = "ERROR: invalid command syntax"
                return
            attempt_screen_switch = self.find_screen(command_buffer[1])
            # ^ this should give us the second item in a char(32) separated
            #       list of all words in our command buffer.
            if attempt_screen_switch == None:
                # the screen name they gave us is bogus.
                self.current_message = f"ERROR: screen '{command_buffer[1]}' not found"
            else:
                self.current_screen = attempt_screen_switch
        elif command.startswith("cast "):
            if len(command_buffer) == 2:
                # assume our two command sections to be "cast" and <spell name>
                # so we'll use the default level spell slot
                self.current_message = self.source.cast_spell(str(command_buffer[1]), 0)
            elif len(command_buffer) == 3:
                self.current_message = self.source.cast_spell(str(command_buffer[1]), int(command_buffer[2]))
            else:
                self.current_message = "ERROR: invalid command syntax"
    
    def find_screen (self, key: str) -> Screen:
        clean_key = key.replace(" ", "") # just in case
        for i_screen in self.menu:
            if type(i_screen.alias) == str:
                if i_screen.alias == clean_key:
                    # we just found our target screen!
                    return i_screen
            elif type(i_screen.alias) == list:
                # oh boy, time for O(n^2)
                for i_alias in i_screen.alias:
                    if i_alias == clean_key:
                        # one of the aliases matched up!
                        return i_screen
        # didn't find anything?
        return None

    def handle_scroll_input (self, key) -> bool :
        if key == curses.KEY_DOWN:
            self.current_screen.update_scroll_index(1)
            return True
        elif key == curses.KEY_UP:
            self.current_screen.update_scroll_index(-1)
            return True
        return False
    
    def draw_meta (self, mode: str) :
        # clear the bottom line
        self.stdscr.addstr(curses.LINES - 1, 0, " "*(curses.COLS-1))
        # draw the mode to the bottom right corner
        mode_str = f"[{self.current_screen.scroll_index}] <{mode}> "
        self.stdscr.addstr(curses.LINES - 1, curses.COLS - (len(mode_str)+1), mode_str)
    
    def draw_message (self) :
        # clear the message line
        self.stdscr.addstr(curses.LINES - 2, 0, " "*(curses.COLS-1))
        if self.current_message == "":
            # nothing to say.
            return
        else:
            # write the message
            self.stdscr.addstr(curses.LINES - 2, 1, f"[ {self.current_message} ]")
