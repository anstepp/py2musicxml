from py2musicxml.notation import Note, Score, Part, Rest
from py2musicxml.composition import Flute, Clarinet, Violin, Cello

aaron_pitches = [9, 9, 2, 0, 7]
morgan_pitches = [4, 0, 2, 7, 9, 7]
rachel_pitches = [2, -3, 0, 11, 4, 9]
john_pitches = [4, 0, 11, 7]

def fractal_names(generations, list1, list2, offset, start_offset):
    odd_list = list1
    even_list = list2
    return_list = odd_list
    note_list = []
    for i in range(generations):
        temp_list = []
        notes = []
        if offset:
            temp_list.append(Rest(start_offset))
        if i % 2 == 0:
            for item in return_list:
                if type(item) is int:
                    current_pc = item
                elif type(item) is Rest:
                    pass
                elif type(item) is Note:
                    current_pc = item.pc
                if current_pc % 2 == 0:
                    for value in odd_list:
                        temp_list.append(Note(4, 4, value + current_pc))
                        temp_list.append(Rest(2+offset))
                else:
                    for value in even_list:
                        temp_list.append(Note(4, 4, value + current_pc))
                        temp_list.append(Rest(1+ offset))
        else:
            for item in return_list:
                if type(item) is int:
                    current_pc = item
                elif type(item) is Rest:
                    pass
                elif type(item) is Note:
                    current_pc = item.pc
                if current_pc % 2 == 0:
                    for value in odd_list:
                        temp_list.append(Note(3, 4, value + current_pc)) 
                        temp_list.append(Rest(2+offset))
                else:
                    for value in even_list:
                        temp_list.append(Note(3, 4, value + current_pc))
                        temp_list.append(Rest(1+offset))
        return_list = temp_list
    return return_list


list_one = fractal_names(2, rachel_pitches, aaron_pitches, 0, 0)
list_two = fractal_names(2, morgan_pitches, john_pitches, 0, 1)
list_three = fractal_names(2, aaron_pitches, morgan_pitches, 2, 2)
list_four = fractal_names(2, morgan_pitches, rachel_pitches, 1, 3)

lists = [list_one, list_two, list_three, list_four]

flute = Flute()
clarinet = Clarinet()
violin = Violin()
cello = Cello()

instruments = [flute, clarinet, violin, cello]

ts = [(4, 4)]

flute.set_note_list(list_one)
flute.check_range()
clarinet.set_note_list(list_two)
clarinet.constrain_to_chalumeau()
violin.set_note_list(list_three)
violin.check_range()
cello.set_note_list(list_four)
cello.constrain_range([(1,0), (4,0)])

parts = [instrument.make_part(ts) for instrument in instruments]

theScore = Score(score_parts=parts)
theScore.convert_to_xml("d_fractal_long.musicxml")
