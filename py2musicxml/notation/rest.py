import copy
from typing import Tuple

import py2musicxml.log as logger

log = logger.get_logger()

class Rest:
    def __init__(self, duration: int):

        log.debug(f"Creating New Rest with duration {duration}")

        if duration <= 0:
            raise ValueError("Rests cannot have negative duration")
        else:
            self.dur = duration
            if self.dur > 0:
                self.is_measure = True
            else:
                self.is_measure = False

    def __str__(self):
        return 'Duration: {}, is_measure {}'.format(self.dur, self.is_measure)

    def split(self, diff) -> Tuple['__class__', '__class__']:
        old_rest = copy.deepcopy(self)
        new_rest = copy.deepcopy(self)

        old_rest.dur = self.dur - diff
        new_rest.dur = diff
        return old_rest, new_rest
