# contains a class for working with ability scores.

# the reason for this class is so that we can have an easy way to deal with
#   the ability score modifier and the '+' or '-' at the front.

class AbiltyScore:
    def __init__(self, value: int):
        self.value = 10
        # a bit of defensive programming going on
        if 0 < value < 30:
            self.value = int(value)
        elif value < 1:
            self.value = 1
        elif 30 < value:
            self.value = 30
        else:
            # I dunno bro
            self.value = 10

    def set_value(self, new_value: int):
        if 0 < new_value < 30:
            self.value = new_value
        elif new_value < 1:
            self.value = 1
        elif 30 < new_value:
            self.value = 30
        else:
            self.value = 10

    def increase_value(self, amount: int):
        self.set_value(self.value + amount)

    def get_mod(self) -> int:
        if self.value >= 10:
            return int(self.value / 2 - 5)
        else:
            return int((self.value-1) / 2 - 5)
        return int(self.value / 2 - 5)

    def __str__(self) -> str:
        if self.get_mod() >= 0:
            return f"{self.value} (+{self.get_mod()})"
        else:
            return f"{self.value} ({self.get_mod()})"

def main ():
    # testing testing
    for i_stat in range(-5, 40):
        print (f"# {i_stat}")
        print (AbiltyScore(i_stat))

if __name__ == "__main__":
    main()
