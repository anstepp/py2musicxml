from lxml import etree


def convertToXML(theList, fname):
    partNumber = 0
    root = etree.Element("score-partwise")
    root.attrib["version"] = "3.0"
    partList = etree.SubElement(root, "part-list")
    partNumber = 0
    # print(theList)
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
        # print(item)
        # I may need to group the measures in the noteList file, but then note objects would need
        # some sort of measure tag. Or, are there measure objects with notes in them? There could
        # be a structure that self checks using the groupList() function as a method for a
        # measure object?
        for thing in item[0]:
            if thing.measureFlag is True:
                currentMeasure += 1
                # print(thing)
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
                # it seems like I may not need this with the lines 20-45 in noteList.py (groupList)
                # but there's no barlines otherwise...
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
        serialized = etree.tostring(
            root,
            doctype="<!DOCTYPE score-partwise PUBLIC \"-//Recordare//DTD MusicXML 3.0 Partwise//EN\" \"http://www.musicxml.org/dtds/partwise.dtd\">",
        )
        newRoot = etree.XML(serialized)
        theTree = etree.ElementTree(newRoot)
        theTree.write(fname, pretty_print=True, encoding="UTF-8", xml_declaration=True)
