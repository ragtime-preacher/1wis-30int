import json

# Load the JSON data from the file
with open('/home/lurch5-64/progamming/1wis-30int/json_libraries/spell_library.json', 'r') as file:
    spell_data = json.load(file)

# Create a new dictionary to hold the modified data
spell_dict = {}

# Iterate through the list of spells and add them to the dictionary
for spell in spell_data:
    if isinstance(spell, dict) and 'name' in spell:
        spell_name = spell['name'].lower()
        spell_dict[spell_name] = spell

# Save the modified data back to a new JSON file
with open('/home/lurch5-64/progamming/1wis-30int/json_libraries/spell_library_modified.json', 'w') as file:
    json.dump(spell_dict, file, indent=2)

# well, here goes nothing