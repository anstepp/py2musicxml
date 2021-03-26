import py2musicxml.log as logger

logging = logger.get_logger()

class Rest:
    def __init__(self, duration):
        self.dur = self._check_duration(duration)

        self.is_measure = False

    def _check_duration(self, duration: float) -> float:

        if duration < 0:
            logging.error(f"Negative rest duration: {new_duration}")
            raise ValueError(f"Rest duration ({new_duration}) must be positive")
        else:
            return duration

    def change_duration(self, new_duration: float) -> None:
        
        self.dur = self._check_duration(new_duration)



    def __str__(self):
        return 'Duration: {}, is_measure {}'.format(self.dur, self.is_measure)
