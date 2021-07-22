from py2musicxml.notation import Measure

class Tempo:

    def __init__(self, tempo, note_value):
        self.tempo = tempo
        self.note_value = note_value
        self.measure = 1

    def set_tempo(self, tempo, note_value):
        self.tempo = tempo
        self.note_value = note_value

    def set_measure(self, measure_no):
        self.measure = measure_no

