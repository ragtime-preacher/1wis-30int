# This file is to hold some functions that we'll need to work with dictionaries
#   of dnd stuff.

def lookup (d: dict, key: str) -> any:
    try:
        return d[key]
    except KeyError:
        return "key not found"

def main () :
    pass

if __name__ == "__main__" :
    main ()