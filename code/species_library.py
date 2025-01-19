from Species import Species

from Character import Character


# Dwarf
def hilldwarf_callback(target: Character):
    target.size = "Medium"
    target.stat_con.increase_value(2)
    target.speed["Walking"] = 25
    target.resistences.append("Poison")
    target.species_traits.append("Dwarven Resilience: ADV on ST against poison, resistance against poison damage")
    target.prof_weapons.append("battleaxe", "handaxe", "light hammer", "warhammer")
