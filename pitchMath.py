from lxml import etree

def convertToXML(theList, fname):
    partNumber = 0
    root = etree.Element("score-partwise")
    root.attrib["version"] = "3.0"
    partList = etree.SubElement(root, "part-list")
    partNumber = 0
    #masterBeatSubdivisions = 4
    for subList in theList:
        currentBeatFactor = subList[1]
        beatMeasure = subList[2]
        beatDivisions = beatMeasure * currentBeatFactor
        partNumber += 1
        scorePart = etree.SubElement(partList, "score-part")
        scorePart.attrib["id"] = "P" + str(partNumber)
        partName = etree.SubElement(scorePart, "part-name")
        part = etree.SubElement(root, "part")
        part.attrib["id"] = "P" + str(partNumber)
        currentMeasure = 1
        measure = etree.SubElement(part, "measure")
        measure.attrib["number"] = str(currentMeasure)
        partAttributes = etree.SubElement(measure, "attributes")
        partDivisions = etree.SubElement(partAttributes, "divisions")
        partDivisions.text = str(currentBeatFactor)
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
        #eventually we need a clef determinant
        clef = etree.SubElement(partAttributes, "clef")
        sign = etree.SubElement(clef, "sign")
        sign.text = "G"
        line = etree.SubElement(clef, "line")
        line.text = "2"
        for currentNote in subList[0]:
            if currentNote.measureFlag is True:
                currentMeasure += 1
                measure = etree.SubElement(part, "measure")
                measure.attrib["number"] = str(currentMeasure)
            else:
            	pass
            if currentNote.pc is not True:
                currentNote.makeOctavePC()
            elif currentNote.octave is not True:
                currentNote.makeOctavePC()
            theNote = etree.SubElement(measure, "note")
            thePitch = etree.SubElement(theNote, "pitch")
            theStep = etree.SubElement(thePitch, "step")
            theStep.text = currentNote.stepName
            theDur = etree.SubElement(theNote, "duration")
            theDur.text = str(currentNote.dur * currentBeatFactor)
            if currentNote.alter:
                accidental = etree.SubElement(theNote, "accidental")
                accidental.text = currentNote.accidental
            theAlter = etree.SubElement(thePitch, "alter")
            if theAlter is not None:
                theAlter.text = currentNote.alter
            else:
                theAlter.text = 0
            if currentNote.tieStart:
                theTie = etree.SubElement(theNote, "tie")
                theTie.attrib["type"] = "start"
                notations = etree.SubElement(theNote, "notations")
                notateTie = etree.SubElement(notations, "tied")
                notateTie.attrib["type"] = "start"
            if currentNote.tieContinue:
                theTie = etree.SubElement(theNote, "tie")
                theTie.attrib["type"] = "continue"
                notations = etree.SubElement(theNote, "notations")
                notateTie = etree.SubElement(notations, "tied")
                notateTie.attrib["type"] = "continue"
            if currentNote.tieEnd:
                theTie = etree.SubElement(theNote, "tie")
                theTie.attrib["type"] = "stop"
                notations = etree.SubElement(theNote, "notations")
                notateTie = etree.SubElement(notations, "tied")
                notateTie.attrib["type"] = "stop"
            theOctave = etree.SubElement(thePitch, "octave")
            theOctave.text = str(currentNote.octave)
        serialized = etree.tostring(
            root,
            doctype="<!DOCTYPE score-partwise PUBLIC \"-//Recordare//DTD MusicXML 3.0 Partwise//EN\" \"http://www.musicxml.org/dtds/partwise.dtd\">",
        )
        newRoot = etree.XML(serialized)
        theTree = etree.ElementTree(newRoot)
        theTree.write(fname, pretty_print=True, encoding="UTF-8", xml_declaration=True)
