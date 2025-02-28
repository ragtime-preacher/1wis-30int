# A simple class to contain the idea of a two-dimensional array
#   where every sub-array is the same length.
# The subarries can be strings.

class Surface :
    def __init__(self, data = list[list]):
        self.data = data
        if not self.verify():
            self.justify()

    # make sure that every sublist is the same length.
    # Obviously, we'll use recursion.
    def verify (self, subarray_length: int = 0, subarray_index: int = 0) -> bool:
        new_length = len(self.data[subarray_index])
        if subarray_index == 0:
            # this is the first row. we'll let this set the tone for
            #   how long the other lists should be.
            subarray_length = len (self.data[0])
        if (new_length != subarray_length) and (subarray_index != 0):
            # This isn't the first row, so we're comparing the current row
            #   against the previous row.
            # If they don't match, we'll return false, which will cascade through
            #   the recursion.
            return False
        if subarray_index == (len(self.data)-1):
            # This is the last row, meaning that we didn't return False 
            #   anywhere along the way. In other words, all sublists are the
            #   same length.
            return True
        # recursion!!! let's go
        return self.verify (
            subarray_length=subarray_length,
            subarray_index=subarray_index+1
        )

    # The idea with this function is to find which sublist is the longest and
    #   "fill in" the other sublists with the fill character, which is ' ' by
    #   default.
    def justify (self, fill: str = ' '):
        target_length = self._find_longest_sublist()
        for i_sub in range(len(self.data)):
            if len(self.data[i_sub]) < target_length:
                difference = target_length-len(self.data[i_sub])
                if type(self.data[i_sub]) == str:
                    for i_dif in range(difference):
                        self.data[i_sub] += fill
                elif type(self.data[i_sub]) == list:
                    for i_dif in range(difference):
                        self.data[i_sub].append()

    # simply iterate through and return the length of the longest subarry
    #   that we find. This is only to be used internally to find the target
    #   length for Surface.justify().
    def _find_longest_sublist (self) -> int :
        longest_found = 0
        for i_sub in self.data:
            if len(i_sub) > longest_found:
                longest_found = len(i_sub)
        return longest_found
    
    def get_lines (self):
        for line in self.data:
            yield line

# testing code
def main():
    test_surface = Surface([
        "123",
        "46",
        "789"
    ])
    print (test_surface.verify())
    for line in test_surface.get_lines():
        print (line)
    return

if __name__ == "__main__":
    main ()