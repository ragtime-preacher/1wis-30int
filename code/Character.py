# Character class

# In theory, contains everything that a character needs to have in order
#   to be played in Dnd.

# The actual character data will be stored in a dictionary that we can
#   save to and load from a .json file.

import json

class Character:
    def __init__(self, filename: str):
        self.data_file = open (filename)
        self.data = json.load(self.data_file)
        return
    
    # TODO implement save()
    
    # Close the file
    def __del__(self):
        self.data_file.close()