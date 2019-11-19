class Rest:

    def __init__(self, duration):

        self.dur = duration
        if self.dur > 0:
            self.is_measure = True
        else:
            self.is_measure = False