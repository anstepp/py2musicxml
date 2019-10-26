from .note import Note
from .notelist import NoteList
from .measure import Measure
from .beat import Beat

def group_notes(input_list: Iterable[Union[NoteList,Measure]], divisions: int or list):
    current_list = input_list
    current_count = 0
    last_current_count = 0
    divisions_list = divisions
    current_note_group = list()
    if current_list is type(NoteList):

    elif current_list is type(Measure):

    else:
        print("Error - wrong type of list")
