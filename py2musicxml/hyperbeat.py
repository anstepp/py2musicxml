class Hyperbeat:

    location = None
    level = None 
    children = list()

    def __init__(self, location: int, level: int):
        level = level
        location = location

    def promote(self):
        new_level = level + 1
        Hyperbeat(self.location, new_level)

    def get_children(self, potential_children: Iterable[list], neighbor: Hyperbeat):
        for potential_child in potential_children:
            if potential_child.level is self.level - 1:
                if potential_child.location is self.location:
                    self.children.append(potential_child)
                elif potential_child.location > self.location and potential_child.location < neighbor.location:
                    self.children.append(potential_child)
                else:
                    pass