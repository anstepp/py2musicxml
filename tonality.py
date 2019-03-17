#currently pseudocode

from py2musicxml import Note

ranges = {"bass" : [[2, "e"], [4,"c"]], "tenor" : [[3, "c"],[4,"g"]], 
		  "alto" : [[3,"g"], [5,"c"]], "soprano" : [[4, "c"], [5,"a"]]}

soprano, alto, tenor, bass = []

#if generating melody, use this


getTriaic(note):
	return [note - 5, note - 3, note, note + 3, note + 5]

getHarmonyBass(note):
	possibilities = getTriaic(note)


duration = 8

#currently, this will make a melody of quarter note C's - ideal for one phrase
while currentBeat < duration:
	soprano.append(note(1, 9, "C"))

while currentBeat < duration:
	bass.append((getHarmonyBass(soprano[currentBeat])))



