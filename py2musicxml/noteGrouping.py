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
        for location, item in enumerate(current_list):
            current_count += item.dur
            current_count_floor = current_count // subdivisions
            current_count_mod = current_count % subdivisions
            if current_count_mod == 0 and current_count_floor == 1:
                if item.dur > subdivisions:
                    how_many_measures = current_count // subdivisions
                    what_goes_to_the_first_measure = (
                        item.dur - current_count // subdivisions
                    )
                    last_note_of_old_measure = copy.deepcopy(current_list[location])
                    last_note_of_old_measure.dur = what_goes_to_the_first_measure
                    last_note_of_old_measure.tie_start = True
                    middle_list.append(last_note_of_old_measure)
                    while how_many_measures > 0:
                        whole_measure_note = copy.deepcopy(current_list[location])
                        whole_measure_note.dur = subdivisions
                        if how_many_measures > 1:
                            whole_measure_note.tie_start = True
                        else:
                            whole_measure_note.tie_end = True
                        middle_list.append(whole_measure_note)
                        how_many_measures -= 1
                else:
                    altered_duration = copy.deepcopy(current_list[location])
                    middle_list.append(altered_duration)
                current_count = 0
                if location != len(current_list) - 1:
                    current_list[location + 1].measure_flag = True
            elif current_count_mod == 0 and current_count_floor > 1:
                how_many_measures = current_count // subdivisions
                if location != len(current_list) - 1:
                    current_list[location + 1].measure_flag = True
                how_many_measures = current_count // subdivisions - 1
                what_goes_to_the_first_measure = (
                    item.dur - subdivisions * how_many_measures
                )
                last_note_of_old_measure = copy.deepcopy(current_list[location])
                last_note_of_old_measure.dur = what_goes_to_the_first_measure
                last_note_of_old_measure.tie_start = True
                middle_list.append(last_note_of_old_measure)
                while how_many_measures > 0:
                    note_to_add = copy.deepcopy(current_list[location])
                    note_to_add.dur = subdivisions
                    note_to_add.measure_flag = True
                    middle_list.append(note_to_add)
                    how_many_measures -= 1
                last_current_count = current_count_mod
                current_count = 0
            elif current_count_mod > 0 and current_count_floor == 1:
                current_note = copy.deepcopy(current_list[location])
                overflow = current_count - subdivisions
                if overflow // subdivisions > 1:
                    new_dur = subdivisions
                    current_note.dur = new_dur
                    current_note.tie_start = True
                    middle_list.append(current_note)
                    tied_note = copy.deepcopy(current_list[location])
                    tied_dur = overflow % subdivisions
                    tied_note.dur = new_dur
                    tied_note.tie_end = True
                    tied_note.measure_flag = True
                    middle_list.append(tied_note)
                else:
                    pre_tie = current_list[location].dur - overflow
                    new_dur = pre_tie
                    current_note.dur = new_dur
                    current_note.tie_start = True
                    middle_list.append(current_note)
                    tied_note = copy.deepcopy(current_list[location])
                    tied_dur = overflow % subdivisions
                    tied_note.dur = tied_dur
                    tied_note.tie_end = True
                    tied_note.measure_flag = True
                    middle_list.append(tied_note)
                last_current_count = current_count % subdivisions
                current_count = overflow
            elif current_count_mod > 0 and current_count_floor > 1:
                current_note = copy.deepcopy(current_list[location])
                last_measure_count = subdivisions - last_current_count
                overflow = current_count_mod
                if last_measure_count > 0:
                    how_many_measures = current_count // subdivisions - 1
                    what_goes_to_the_first_measure = subdivisions - last_current_count
                    what_goes_to_the_last_measure = overflow
                    extra_measure_beats = subdivisions * how_many_measures
                else:
                    how_many_measures = current_count // subdivisions
                    what_goes_to_the_first_measure = False
                    what_goes_to_the_last_measure = overflow
                    extra_measure_beats = subdivisions * how_many_measures
                if what_goes_to_the_first_measure:
                    current_note = copy.deepcopy(current_list[location])
                    current_note.dur = what_goes_to_the_first_measure
                    current_note.tie_start = True
                    middle_list.append(current_note)
                while how_many_measures > 0:
                    current_note = copy.deepcopy(current_list[location])
                    current_note.dur = subdivisions
                    current_note.tie_start = True
                    # FIXME: This needs to not get switched on first note
                    current_note.measure_flag = True
                    if what_goes_to_the_last_measure > 0:
                        current_note.tie_end = True
                    current_note.tie_end = True
                    middle_list.append(current_note)
                    how_many_measures -= 1
                if what_goes_to_the_last_measure > 0:
                    current_note = copy.deepcopy(current_list[location])
                    current_note.dur = what_goes_to_the_last_measure
                    current_note.tie_end = True
                    current_note.measure_flag = True
                    middle_list.append(current_note)
                last_current_count = current_count % subdivisions
                current_count = overflow % subdivisions
            elif current_count_mod > 0 and current_count_floor < 1:
                #print("buisness as usual")
                altered_duration = copy.deepcopy(current_list[location])
                middle_list.append(altered_duration)
                last_current_count = current_count_mod
    elif current_list is type(Measure):
        for location, item in enumerate(current_list):
            current_count += item.dur
            current_count_floor = current_count // subdivisions
            current_count_mod = current_count % subdivisions
            if current_count_mod == 0 and current_count_floor == 1:
                if location != len(current_list) - 1:
                    #make this create a new beat
                    current_list[location + 1].beat = True
                if item.dur > subdivisions:
                    duration_of_beat = ???
                    what_goes_to_the_first_beat = (
                        item.dur - current_count // subdivisions
                    )
                    last_note_of_old_beat = copy.deepcopy(current_list[location])
                    last_note_of_old_beat.dur = what_goes_to_the_first_measure
                    last_note_of_old_beat.tie_start = True
                    middle_list.append(last_note_of_old_measure)
                    while how_many_beats > 0:
                        whole_beat_note = copy.deepcopy(current_list[location])
                        whole_beat_note.dur = #current_beat.subdivisions
                        if how_many_beats > 1:
                            whole_beat_note.tie_start = True
                        else:
                            whole_beat_note.tie_end = True
                        middle_list.append(whole_beat_note)
                        how_many_measures -= 1
                else:
                    altered_duration = copy.deepcopy(current_list[location])
                    middle_list.append(altered_duration)
                current_count = 0
            elif current_count_mod == 0 and current_count_floor > 1:
                how_many_beats = current_count // subdivisions
                # Do I still need this?
                if location != len(current_list) - 1:
                    current_list[location + 1].measure_flag = True
                how_many_beats = current_count // subdivisions - 1
                what_goes_to_the_first_beat = (
                    item.dur - subdivisions * how_many_beats
                )
                last_note_of_old_beat = copy.deepcopy(current_list[location])
                last_note_of_old_beat.dur = what_goes_to_the_first_measure
                last_note_of_old_beat.tie_start = True
                middle_list.append(last_note_of_old_beat)
                while how_many_measures > 0:
                    note_to_add = copy.deepcopy(current_list[location])
                    note_to_add.dur = subdivisions
                    note_to_add.measure_flag = True
                    middle_list.append(note_to_add)
                    how_many_beats -= 1
                last_current_count = current_count_mod
                current_count = 0
            elif current_count_mod > 0 and current_count_floor == 1:
                current_note = copy.deepcopy(current_list[location])
                overflow = current_count - subdivisions
                if overflow // subdivisions > 1:
                    new_dur = subdivisions
                    current_note.dur = new_dur
                    current_note.tie_start = True
                    middle_list.append(current_note)
                    tied_note = copy.deepcopy(current_list[location])
                    tied_dur = overflow % subdivisions
                    tied_note.dur = new_dur
                    tied_note.tie_end = True
                    tied_note.measure_flag = True
                    middle_list.append(tied_note)
                else:
                    pre_tie = current_list[location].dur - overflow
                    new_dur = pre_tie
                    current_note.dur = new_dur
                    current_note.tie_start = True
                    middle_list.append(current_note)
                    tied_note = copy.deepcopy(current_list[location])
                    tied_dur = overflow % subdivisions
                    tied_note.dur = tied_dur
                    tied_note.tie_end = True
                    tied_note.measure_flag = True
                    middle_list.append(tied_note)
                last_current_count = current_count % subdivisions
                current_count = overflow
            elif current_count_mod > 0 and current_count_floor > 1:
                current_note = copy.deepcopy(current_list[location])
                last_beat_count = subdivisions - last_current_count
                overflow = current_count_mod
                if last_measure_count > 0:
                    how_many_beats = current_count // subdivisions - 1
                    what_goes_to_the_first_measure = subdivisions - last_current_count
                    what_goes_to_the_last_measure = overflow
                    extra_measure_beats = subdivisions * how_many_measures
                else:
                    how_many_beats = current_count // subdivisions
                    what_goes_to_the_first_measure = False
                    what_goes_to_the_last_measure = overflow
                    extra_measure_beats = subdivisions * how_many_measures
                if what_goes_to_the_first_measure:
                    current_note = copy.deepcopy(current_list[location])
                    current_note.dur = what_goes_to_the_first_measure
                    current_note.tie_start = True
                    middle_list.append(current_note)
                while how_many_measures > 0:
                    current_note = copy.deepcopy(current_list[location])
                    current_note.dur = subdivisions
                    current_note.tie_start = True
                    # FIXME: This needs to not get switched on first note
                    current_note.measure_flag = True
                    if what_goes_to_the_last_measure > 0:
                        current_note.tie_end = True
                    current_note.tie_end = True
                    middle_list.append(current_note)
                    how_many_measures -= 1
                if what_goes_to_the_last_measure > 0:
                    current_note = copy.deepcopy(current_list[location])
                    current_note.dur = what_goes_to_the_last_measure
                    current_note.tie_end = True
                    current_note.measure_flag = True
                    middle_list.append(current_note)
                last_current_count = current_count % subdivisions
                current_count = overflow % subdivisions
            elif current_count_mod > 0 and current_count_floor < 1:
                #print("buisness as usual")
                altered_duration = copy.deepcopy(current_list[location])
                middle_list.append(altered_duration)
                last_current_count = current_count_mod
    else:
        print("Error - wrong type of list")
