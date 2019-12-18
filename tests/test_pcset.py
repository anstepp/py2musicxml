import pytest

from py2musicxml.analysis import PitchClassSet

def test_object_init():

    pcs = PitchClassSet([0,1,5])

    assert pcs.cardinality == 3

    assert pcs.normal_order == [0,1,5]

def test_object_long_set():

    pitch_classes_one = [0,1,2,3,4,5]

    pcs = PitchClassSet(pitch_classes_one)

    assert pcs.normal_order == pitch_classes_one

    pitch_classes_two = [2,3,4,5,6,7]

    pcs2 = PitchClassSet(pitch_classes_two)

    assert pcs2.normal_order != pitch_classes_two
    assert pcs2.normal_order == pitch_classes_one

def test_complex_normal_order():

    oh_one_six = [0,1,7]

    pc_set_one = PitchClassSet(oh_one_six)

    assert pc_set_one.normal_order != oh_one_six
    assert pc_set_one.normal_order == [0,1,6]

    zero_four_seven = [0,4,7]

    pc_set_two = PitchClassSet(zero_four_seven)

    assert pc_set_two.normal_order != zero_four_seven
    assert pc_set_two.normal_order == [0,3,7]

    one_two_seven = [1,2,7]

    pc_set_three = PitchClassSet(one_two_seven)

    assert pc_set_three.normal_order != one_two_seven
    assert pc_set_three.normal_order != oh_one_six
    assert pc_set_three.normal_order == [0,1,6]
    assert pc_set_three.normal_order == pc_set_one.normal_order

def test_pc_start_finish_same_interval():

    the_set_to_test = [0,1,4,5]

    test_pcset = PitchClassSet(the_set_to_test)

    assert test_pcset.normal_order == the_set_to_test

    harder_test_to_set = [0,1,2,5,6]

    harder_test_pcset = PitchClassSet(harder_test_to_set)

    assert harder_test_pcset.normal_order == harder_test_to_set

    harder_test_tricky = [0,1,4,5,6]

    tricky_pcs = PitchClassSet(harder_test_tricky)

    assert tricky_pcs.normal_order == harder_test_to_set

    very_tricky_test = [0,1,3,4,6,7]

    very_tricky_pcs = PitchClassSet(very_tricky_test)

    assert very_tricky_pcs.normal_order == very_tricky_test

    even_trickier_test = [1,2,4,5,7,8]

    even_trickier_pcs = PitchClassSet(even_trickier_test)

    assert even_trickier_pcs.normal_order == very_tricky_test

def test_out_of_order():

    test_set = [7, 1, 0]

    test_pcs = PitchClassSet(test_set)

    assert test_pcs.normal_order == [0,1,6]


def test_transpose():

    test_pcs = PitchClassSet([0,1,7])

    assert test_pcs.normal_order == [0,1,6]
    assert test_pcs.ordered_list == [0,1,7]

    new_pcs = test_pcs.transpose(4)

    assert new_pcs.normal_order == test_pcs.normal_order == [0,1,6]
    assert new_pcs.ordered_list != test_pcs.ordered_list
    assert new_pcs.ordered_list == [4,5,11]