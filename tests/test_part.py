from py2musicxml import Measure, Note, Beat, Part

expected_note_values = [3, 3, 1, 2, 1, 2, 3, 1, 2, 2, 1]
expected_beat_lens = [1, 1, 2, 2, 1, 2, 2, 1]

test_note_a = Note(4, 4, 4)
test_note_b = Note(3, 3, 3)
test_note_c = Note(6, 6, 6)

test_list = [test_note_b, test_note_a, test_note_b, test_note_c, test_note_a]

test_sig = [[3, 4]]

fj_pitches = [0, 2, 4, 0, 0, 2, 4, 0, 4, 5, 7, 4, 5, 7, 7, 9, 7, 5, 4, 0, 7, 9, 7, 5, 4, 0, 0, -5, 0, 0, -5, 0]
fj_durs = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 4, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 4, 2, 2, 4]

test_part = Part(test_list, test_sig)
def assert_durs():
    note_count = 0
    for index, measure in enumerate(test_part.measures):
        for beat in measure.beats:
            for note in beat.notes:
                expected_note_duration = expected_note_values[note_count]
                
                # print('MY TEST')
                # print(note)
                # print(note_count, beat, beat.notes, note.dur, expected_note_duration)
                
                assert note.dur == expected_note_duration
                note_count += 1

#assert_durs()
        
def assert_unique():
    for index_x, x in enumerate(test_part.measures):
        #print(index_x)
        for index_y, y in enumerate(test_part.measures):
            if x is not y:
                #print(index_y, y, y.beats)
                assert not set(y.beats).intersection(set(x.beats))
            else:
                assert set(y.beats).intersection(set(x.beats)) == set(y.beats).union(
                    set(x.beats)
                )

assert_unique()

def frere_jacques():
    fj_pitches = [0, 2, 4, 0, 0, 2, 4, 0, 4, 5, 7, 4, 5, 7, 7, 9, 7, 5, 4, 0, 7, 9, 7, 5, 4, 0, 0, -5, 0, 0, -5, 0]
    fj_durs = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 4, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 4, 2, 2, 4]
    fj_ts = [[4,4]]
    fj_list = []

    for pitch, dur in zip(fj_pitches, fj_durs):
        fj_list.append(Note(dur, pitch, 4))

    fj_part = Part(fj_list, fj_ts)

    counter = 0
    for measure_index, measure in enumerate(fj_part.measures):
        for beat_index, beat in enumerate(measure.beats):
            for note_index, note in enumerate(beat.notes):
                print(counter, fj_durs[counter], note.dur)
                assert fj_durs[counter] == note.dur
                counter += 1

frere_jacques()

