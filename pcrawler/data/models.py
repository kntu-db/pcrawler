class Problem:
    def __str__(self):
        return f"Problem{self.__dict__}"

    def __repr__(self):
        return self.__str__()
