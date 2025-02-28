# Explanation of spell_library.json
So why is there this six thousand line JSON file in my repo?  

It's to store all the spells in D&D. That's a lot, and I don't really want to
have to dope out a json schema and type all the spells in the game.  

Fortunately, since the last time I tried this project, some random guy on
GitHub already did the work. I just hope that it's valid, consistent JSON.  

Note that use of the file spell_library.json is deprecated - it was set up as an array of nameless objects. Use efficient_spell_library.json isntead - accessing a spell by name has O(1) performance.

spells json can be found here:  
https://github.com/jcquinlan/dnd-spells/blob/master/spells.json