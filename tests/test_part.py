from py2musicxml import Measure, Note, Beat, Part

def test_score():

    test_note_a = Note(4,4,4)
    test_note_b = Note(3,3,3)

    test_list = [test_note_a, test_note_b, test_note_a, test_note_a, test_note_b]

    test_sig = [(3,4), (2,4)]

    test_part = Part(test_list, test_sig)

    assert test_part.measure_list[0].meter == "Triple"
    print(test_part.measure_list, test_part.measure_list[0])
    assert test_part.measure_list[1].meter == "Duple"

    assert test_part.measure_list
    for measure in test_part.measure_list:
        assert measure.measure_map
