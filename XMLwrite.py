import pitchMath
#convertToXML: [list, scale], file name
import noteList
# noteList: variance, seed
# noteList.getList:type, starting octave, starting note, generations, tonic
import random

random.seed(20)

array = list()
for x in range(0, 2):
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
	generations = 12 # 12 before
	# 8 is octave A flat
	thing = item.getList("SWG", 6, 8, generations, 8, "ES", 45)
	choices = [2]
	scale = random.choice(choices)
	appendMe = [thing, scale]
	listList.append(appendMe)

pitchMath.convertToXML(listList, "XML.xml")
