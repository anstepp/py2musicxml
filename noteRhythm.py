# at one point, this was overloaded


class noteRhythm:
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if key is "samps":
                self.numSamps = value
            elif key is "dur":
                self.duration = value
            elif key is "previous":
                self.previousDuration = value  # should have test for list
