import py2musicxml.log as logger

log = logger.get_logger()

class Rest:
    def __init__(self, duration):

        log.debug(f"Creating New Rest with duration {duration}")

        self.dur = duration
        if self.dur > 0:
            self.is_measure = True
        else:
            self.is_measure = False

    def change_duration(self, new_duration: float) -> None:
        try:
            if new_duration >= 0:
                self.dur = new_duration
        except ValueError as e:
            logging.error(e)
            raise

    def __str__(self):
        return 'Duration: {}, is_measure {}'.format(self.dur, self.is_measure)
