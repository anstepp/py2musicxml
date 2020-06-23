# Py2MusicXML
Convert Python Algorithms to Notation via MusicXML.

Py2MusicXML is designed for prototyping musical ideas in Python. You prototype ideas using the builtin objects that represent elements of musical notation. Then, you can export the representation in Python to MusicXML, and open the .musicxml file in commercial notation software to explore your ideas further.

It's fun - try it!

## Basic Functionality

There are several builtin objects used to represent notation in Python.

These are:

* Note
* Rest
* Measure
* Part
* Score

## "Hello, World!"

A smiple score that produces a middle C would be as follows:

```python
from py2musicxml.notation import Note, Part, Score

duration = 4
octave = 4
pitch_class = 0

middle_c = Note(duration, octave, pitch_class)

note_list = [middle_c]

time_signature = [(4,4)]

our_first_part = Part(note_list, time_signature)

part_list = [our_first_part]

our_first_score = Score(part_list)
our_first_score.convert_to_xml("middlec.musicxml")
```
