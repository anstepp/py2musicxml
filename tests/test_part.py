import pytest

from py2musicxml import Measure, Note, Beat, Part, Score, Rest

expected_note_values = [3, 3, 1, 2, 1, 2, 3, 1, 2, 2, 1]
expected_beat_lens = [1, 1, 2, 2, 1, 2, 2, 1]

test_note_a = Note(4, 4, 4)
test_note_b = Note(3, 3, 3)
test_note_c = Note(6, 6, 6)
test_rest = Rest(1)

test_list = [test_note_b, test_note_a, test_note_b, test_note_c, test_note_a, test_rest]

test_sig = [[3, 4]]

# fmt: off
fj_pitches = [0, 2, 4, 0, 0, 2, 4, 0, 4, 5, 7, 4, 5, 7, 7, 9, 7, 5, 4, 0, 7, 9, 7, 5, 4, 0, 0, -5, 0, 0, -5, 0]
fj_durs = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 4, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 4, 2, 2, 4]
# fmt: on

test_part = Part(test_list, test_sig)

def test_assert_durs():
    note_count = 0
    for index, measure in enumerate(test_part.measures):
        for beat in measure.beats:
            for note in beat.notes:
                expected_note_duration = expected_note_values[note_count]
                
                print('MY TEST')
                print(note)
                print(note_count, beat, beat.notes, note.dur, expected_note_duration)
                
                assert note.dur == expected_note_duration
                note_count += 1

        
def test_assert_unique():
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


test_score = Score(score_parts=[test_part])
test_score.convert_to_xml("test_score_cases.xml")

def test_long_durs():
    # fmt: off
    long_durs = [4,4,4,4,7,1,4,6,7,3,8,6,7,1,5,6,1]
    long_durs_after_break = [4,4,4,4,4,3,1,4,4,2,2,4,1,3,4,4,4,2,2,4,1,1,2,3,1,4,1,1,2]
    # fmt: on

    long_durs_list = [Note(x, 4, x) for x in long_durs]
    long_durs_part = Part(long_durs_list, [(4,4)])

    long_durs_part_halved_list = [Note(x * 0.5, 4, x) for x in long_durs] 

    note_count = 0
    for index, measure in enumerate(long_durs_part.measures):
        for beat in measure.beats:
            for note in beat.notes:
                expected_note_duration = long_durs_after_break[note_count]
                print(note_count, note.dur, expected_note_duration)
                assert note.dur == expected_note_duration
                note_count += 1

    long_durs_score = Score(score_parts=[long_durs_part])
    long_durs_score.convert_to_xml("test_score_long.xml")

def test_frere_jacques():

    fj_ts = [[4,4]]
    fj_list = [Note(dur, 4, pitch) for dur, pitch in zip(fj_durs, fj_pitches)]

    fj_part = Part(fj_list, fj_ts)

    counter = 0
    for measure_index, measure in enumerate(fj_part.measures):
        for beat_index, beat in enumerate(measure.beats):
            for note_index, note in enumerate(beat.notes):
                print(counter, fj_durs[counter], note.dur)
                assert fj_durs[counter] == note.dur
                counter += 1

    score = Score(score_parts=[fj_part])
    score.convert_to_xml("test_score_fj.xml")


def test_fj_three_four():

    # fmt: off
    fj_durs_34 = [2,1,1,2,2,1,1,2,2,1,1,2,2,1,3,2,1,1,2,2,1,1,1,1,2,1,1,1,1,1,1,1,1,2,2,1,1,2,2,1,1,2,3,1,2]
    # fmt: on
    fj_ts = [[3,4]]
    fj_list = [Note(dur, 4, pitch) for dur, pitch in zip(fj_durs, fj_pitches)]

    fj_part = Part(fj_list, fj_ts)

    counter = 0
    for measure_index, measure in enumerate(fj_part.measures):
        for beat_index, beat in enumerate(measure.beats):
            for note_index, note in enumerate(beat.notes):
                print(counter, fj_durs_34[counter], note.dur)
                assert fj_durs_34[counter] == note.dur
                counter += 1

    score = Score(score_parts=[fj_part])
    score.convert_to_xml("test_score_fj_34.xml")

def test_fj_shifting_ts():
    # fmt: off
    fj_durs_shift = [2,2,2,1,1,1,1,2,1,1,2,2,2,2,2,1,1,1,1,3,1,1,1,1,1,2,2,1,1,1,1,1,1,2,1,1,2,2,2,2,2,1,2,1,3]
    # fmt: on
    fj_ts = [(4,4),(3,4),(2,4)]
    fj_list = [Note(dur, 4, pitch) for dur, pitch in zip(fj_durs, fj_pitches)]

    fj_part = Part(fj_list, fj_ts)

    counter = 0
    for measure_index, measure in enumerate(fj_part.measures):
        for beat_index, beat in enumerate(measure.beats):
            for note_index, note in enumerate(beat.notes):
                print(counter, fj_durs_shift[counter], note)
                assert fj_durs_shift[counter] == note.dur
                counter += 1

    score = Score(score_parts=[fj_part])
    score.convert_to_xml("test_score_fj_34.xml")

def test_frere_jacques_subdiv():

    fj_ts = [[4,4]]
    fj_list = [Note(dur, 4, pitch) for dur, pitch in zip(fj_durs, fj_pitches)]

    fj_part = Part(fj_list, fj_ts)

    fj_durs_halved = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 0.5, 0.5, 0.5, 0.5, 1, 1, 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 1, 2, 1, 1, 2]
    fj_halved_list = [Note(dur, 4, pitch) for dur, pitch in zip(fj_durs_halved, fj_pitches)]
    fj_halved_part = Part(fj_halved_list, fj_ts)

    assert fj_halved_part.measure_factor == 2

    counter = 0
    for measure_index, measure in enumerate(fj_part.measures):
        for beat_index, beat in enumerate(measure.beats):
            for note_index, note in enumerate(beat.notes):
                print(counter, fj_durs[counter], note.dur)
                assert fj_durs[counter] == note.dur
                counter += 1

    score = Score(score_parts=[fj_part, fj_halved_part])
    score.convert_to_xml("test_score_fj_subdiv.xml")

    # fmt: off
    fj_durs_shift = [2,2,2,1,1,1,1,2,1,1,2,2,2,2,2,1,1,1,1,3,1,1,1,1,1,2,2,1,1,1,1,1,1,2,1,1,2,2,2,2,2,1,2,1,3]
    # fmt: on
    fj_ts = [(4,4),(3,4),(2,4)]
    fj_list = [Note(dur * 0.5, 4, pitch) for dur, pitch in zip(fj_durs, fj_pitches)]

    fj_part = Part(fj_list, fj_ts)

    # counter = 0
    # for measure_index, measure in enumerate(fj_part.measures):
    #     for beat_index, beat in enumerate(measure.beats):
    #         for note_index, note in enumerate(beat.notes):
    #             print(counter, fj_durs_shift[counter], note)
    #             assert fj_durs_shift[counter] == note.dur
    #             counter += 1






