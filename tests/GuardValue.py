from math import inf

# This class simulate a pointer for the guard calculation

"""
In the context of time series analysis, GuardValue helps manage state transitions and ensure values
are correctly propagated and updated. This deferred evaluation mechanism ensures that calculations
dynamically reference the most up-to-date values, similar to how pointers work in other programming languages.
"""



class GuardValue:
    # Unfortunately there isn't the possibility to have multiple constructors in python
    def __init__(self, value, *args):
        self.value = value
        if len(args) > 0:
            self.connected_table = args[0]
            self.index = args[1]
            self.table_name = args[2]

    def get(self):
        # Value is set to infinite if there is no value
        if not (self.value == float(inf)):
            return self.value
        else:
            return self.connected_table[self.index].get()

    def __str__(self):
        return self.get().__str__()

    def __repr__(self):
        return self.__str__()