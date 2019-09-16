import bjorklund.py
from .note import Note
from .beat import Beat

class Measure():
	index = None
	beats = []
	weight = None
	subdivisions = None 
	meter = []
	time_signature = tuple()

	def __init__(self, notes: Iterable[NoteList]):
		self.get_subdivisions()
		self.notes = notes

	def get_subdivisions(self, factor: int, divisions: int):
		time_factor = factor
		smallest_division = divisions
		self.subdivisions = factor * divsions

	def divide_measure(self):
		current_count = 0
		current_beat = 0
		measure_map = []
		for beat in self.meter:
			measure_map.append(beat * self.subdivisions)
		for current_note in self.notes:
			current_count += current_note.dur
			if current_count > 