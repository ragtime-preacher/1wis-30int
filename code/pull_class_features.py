import json
json_file = open("/home/feijao/programming/1wis-30int/json_libraries/class_features_library.json")
class_dict = json.load(json_file)
json_file.close()


# YEAH RECURSION BABY
def get_barbarian_features(level: int, all_features: list = [], constants: dict = {"rages/long rest": 0, "rage damage": 0}):
    if level < 1:
        # we're done. Tack constants onto the beginning of our feature list and get out.
        return [constants] + all_features
    new_features = class_dict[f"BARBARIAN_{level}"]["new class features"]
    all_features[:0] = new_features
    for i_key in class_dict[f"BARBARIAN_{level}"]["constants"].keys():
        if i_key in constants.keys():
            constants[i_key] += class_dict[f"BARBARIAN_{level}"]["constants"][i_key]
        else:
            constants[i_key] = class_dict[f"BARBARIAN_{level}"]["constants"][i_key]
    return get_barbarian_features(level-1, all_features=all_features, constants=constants)

print (get_barbarian_features(10, []))
