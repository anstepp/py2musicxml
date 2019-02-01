from lxml import etree

def convertToXML(list, fname):
	partNumber = 0
	root = etree.Element("score-partwise")
	root.attrib["version"] = "3.0"
	partList = etree.SubElement(root, "part-list")
	partNumber = 0
	for item in theList:
		partNumber += 1
		scorePart = etree.SubElement(partList, "score-part")
		scorePart.attrib["id"] = "P" + str(partNumber)
		partName = etree.SubElement(scorePart, "part-name")
		part = etree.SubElement(root, "part")
		part.attrib["id"] = "P" + str(partNumber)
		subList = []
		currentMeasure = 1	
		measureMax = 8 * item[1]
		subdivisionCount = 0
		measure = etree.SubElement(part, "measure")
		measure.attrib["number"] = str(currentMeasure)
		partAttributes = etree.SubElement(measure, "attributes")
		partDivisions = etree.SubElement(partAttributes, "divisions")
		partDivisions.text = str(2 * item[1])
		partKey = etree.SubElement(partAttributes, "key")
		fifths = etree.SubElement(partKey, "fifths")
		fifths.text = "0"
		mode = etree.SubElement(partKey, "mode")
		mode.text = 'none'
		time = etree.SubElement(partAttributes, "time")
		beats = etree.SubElement(time, "beats")
		beats.text = "4"
		beatType = etree.SubElement(time, "beat-type")
		beatType.text = "4"
		clef = etree.SubElement(partAttributes, "clef")
		sign = etree.SubElement(clef, "sign")
		sign.text = "G"
		line = etree.SubElement(clef, "line")
		line.text = "2"
		for thing in item[0]:
			measure.attrib["number"] = str(currentMeasure)
			if thing.pc is not True:	
				thing.makeOctavePC()
			elif thing.octave is not True:
				thing.makeOctavePC()
			theNote = etree.SubElement(measure, "note")
			thePitch = etree.SubElement(theNote, "pitch")
			theStep = etree.SubElement(thePitch, "step")
			theStep.text = thing.stepName
			theAlter = etree.SubElement(thePitch, "alter")
			if theAlter is not None:
				theAlter.text = thing.alter
			else:
				theAlter.text = 0
			theOctave = etree.SubElement(thePitch, "octave")
			theOctave.text = str(thing.octave)
			theDur = etree.SubElement(theNote, "duration")
			theDur.text = str(thing.dur)
			if thing.alter:
				accidental = etree.SubElement(theNote, "accidental")
				accidental.text = thing.accidental
			subdivisionCount += thing.dur
			if subdivisionCount == measureMax:
				currentMeasure += 1
				measure = etree.SubElement(part, "measure")
				theNote = etree.SubElement(measure, "note")
				thePitch = etree.SubElement(theNote, "pitch")
				theStep = etree.SubElement(thePitch, "step")
				theStep.text = thing.stepName
				theAlter = etree.SubElement(thePitch, "alter")
				theAlter.text = thing.alter
				theOctave = etree.SubElement(thePitch, "octave")
				theOctave.text = str(thing.octave)
				theDur = etree.SubElement(theNote, "duration")
				theDur.text = str(thing.duration)
				if thing.alter:
					accidental = etree.SubElement(theNote, "accidental")
					accidental.text = thing.accidental
				subdivisionCount = 0
			elif subdivisionCount > measureMax:
				currentMeasure += 1
				measure = etree.SubElement(part, "measure")
				subList = []
				#break up things into sub parts?
				counter = thing.duration - subdivisionCount
				while counter > 0:
					newVal = counter - measureMax
					subList.append(newVal)
					counter - newVal
				for it in subList:
					currentMeasure += 1
					measure = etree.SubElement(part, "measure")
					theNote = etree.SubElement(measure, "note")
					thePitch = etree.SubElement(theNote, "pitch")
					theStep = etree.SubElement(thePitch, "step")
					theStep.text = thing.stepName
					theAlter = etree.SubElement(thePitch, "alter")
					theAlter.text = thing.alter
					theOctave = etree.SubElement(thePitch, "octave")
					theOctave.text = str(thing.octave)
					theDur = etree.SubElement(theNote, "duration")
					theDur.text = str(it)
				subdivisionCount = 0
		serialized = etree.tostring(root, doctype="<!DOCTYPE score-partwise PUBLIC \"-//Recordare//DTD MusicXML 3.0 Partwise//EN\" \"http://www.musicxml.org/dtds/partwise.dtd\">")
		newRoot = etree.XML(serialized)
		theTree = etree.ElementTree(newRoot)
		theTree.write(fname, pretty_print=True, encoding="UTF-8", xml_declaration=True)