from Character import Character


class Species:
    def __init__(self,
                 species_name: str,
                 subspecies_name: str,
                 apply_callback: callable):
        self.name = species_name
        self.sub_name = subspecies_name
        self.apply_callback = apply_callback

    def apply(self, character: Character):
        self.apply_callback(character)

