from py2musicxml import Measure, Note, Beat, Part


# def test_score():

expected_note_values = [3, 1, 2, 1, 2, 3, 1, 2, 2]
expected_beat_lens = [1, 2, 2, 1, 2, 2, 1]
test_note_a = Note(4, 4, 4)
test_note_b = Note(3, 3, 3)
test_note_c = Note(6, 6, 6)

test_list = [test_note_a, test_note_b, test_note_c, test_note_a]

test_sig = [[3, 4]]


test_part = Part(test_list, test_sig)

note_count = 0
for index, measure in enumerate(test_part.measure_list):
    for beat in measure.beats:
        for note in beat.notes:
            expected_note_duration = expected_note_values[note_count]
            
            print('MY TEST')
            print(note)
            print(note_count, beat, beat.notes, note.dur, expected_note_duration)
            
            assert note.dur == expected_note_duration
            note_count += 1
    #assert len(measure.beats) == expected_beat_lens[index]
        

for index_x, x in enumerate(test_part.measure_list):
    #print(index_x)
    for index_y, y in enumerate(test_part.measure_list):
        if x is not y:
            #print(index_y, y, y.beats)
            assert not set(y.beats).intersection(set(x.beats))
        else:
            assert set(y.beats).intersection(set(x.beats)) == set(y.beats).union(
                set(x.beats)
            )

assert len(test_part.measure_list) == 7

