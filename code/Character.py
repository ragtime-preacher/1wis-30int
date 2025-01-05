# Character class

# In theory, contains everything that a character needs to have in order
#   to be played in Dnd.

import json

class Character:
    def __init__(self, filename: str):
        self.data_file = open(filename)
        self.data = json.loads(self.data_file)
        return
    
    # Close the file
    def __del__(self):
        self.data_file.close()