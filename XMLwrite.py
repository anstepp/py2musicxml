import pitchMath
#convertToXML: [list, scale], file name
import noteList
# noteList: variance, seed
# noteList.getList:type, starting octave, starting note, generations, tonic
import random

random.seed(2)

array = list()
for x in range(0, 12):
	array.append(noteList.noteList(0.8, x))

listList = list()
for item in array:
	"""the noteList.getList() function is where the algorithmic stuff happens. For the
	variables: 
	"SG" for 12-tone or "SWG" for diatonic, (hopefully more to come)
	starting octave, 
	starting note,
	generations, 
	tonic note,
	Remainders "EU" or Bjorklund "ES",
	max feed to the rhythm machine or list """
	
	grammar = "SG" # stochastic grammar
	starting_octave = 2
	starting_note = 8
	generations = 1
	starting_pitch = 8
	rtype = "EU"
	rhythm = 45


	thing = item.getList(
		grammar,
		starting_octave,
		starting_note,
		generations, 
		starting_pitch,
		rtype, 
		rhythm
	)
	choices = [2]
	scale = random.choice(choices)
	appendMe = [thing, scale]
	listList.append(appendMe)

pitchMath.convertToXML(listList, "XML.xml")
