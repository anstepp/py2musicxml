class Rest:
    def __init__(self, duration):

        self.dur = duration
        if self.dur > 0:
            self.is_measure = True
        else:
            self.is_measure = False

    def change_duration(self, new_duration: float) -> None:
        try:
            new_duration >= 0
        except ValueError as e:
            logging.error(e)
            raise
        finally:
            self.dur = new_duration

    def __str__(self):
        return 'Duration: {}, is_measure {}'.format(self.dur, self.is_measure)
