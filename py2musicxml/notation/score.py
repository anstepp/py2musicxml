import pathlib

from lxml import etree
from typing import Iterable, Optional

from .part import Part
from .rest import Rest
from .measure import Measure
from .beat import Beat


class Score:
    """Generates a MusicXML score from a list of parts (NoteLists) and outputs score to file"""

    def __init__(
        self,
        score_parts: Iterable[Part],
        title: Optional[str] = None,
        composer: Optional[str] = None,
    ):

        self.score_parts = score_parts

        self.title = title
        self.composer = composer
        self._pad_with_empty_measures()


    def _pad_with_empty_measures(self):

            max_len = 0

            # figure out which part is the longest (largest number of measures)
            for part in self.score_parts:
                if len(part.measures) > max_len:
                    max_len = len(part.measures)
                    longest_part = part

            for part in self.score_parts:
                if len(part.measures) < max_len:
                    for idx in range(len(part.measures), max_len):
                        ts = longest_part.measures[idx].time_signature
                        measure_to_append = Measure(ts, 1)
                        full_rest = ts[0]
                        empty_beat = Beat(ts[0])
                        empty_beat.add_note(Rest(full_rest))
                        measure_to_append.add_beat(empty_beat)
                        part.measures.append(measure_to_append)

    def convert_to_xml(self, output_filepath: str) -> None:
        """Entrypoint to Score class
            * converts self.parts (list of NoteLists) to a MusicXML tree
            * writes MusicXML tree to .xml file
        """
        xml_score = self._convert_score_parts_to_xml()
        self._write_xml_to_file(output_filepath, xml_score)

    def _convert_score_parts_to_xml(self) -> etree.ElementTree:
        """Convert self.parts (list of NoteLists) to a MusicXML tree"""

        root = etree.Element("score-partwise", {"version": "3.0"})

        if self.title:
            xml_movement_title = etree.SubElement(root, "movement-title")
            xml_movement_title.text = self.title

        if self.composer:
            xml_identification = etree.SubElement(root, "identification")

            xml_identification_composer = etree.SubElement(
                xml_identification, "creator", {"type": "composer"}
            )

            xml_identification_composer.text = self.composer

        # create part-list
        #   score-part, part-name
        xml_part_list = etree.SubElement(root, "part-list")
        for idx, score_part in enumerate(self.score_parts):
            part_number = idx + 1
            xml_score_part = etree.SubElement(
                xml_part_list, "score-part", {"id": "P" + str(part_number)}
            )
            xml_part_name = etree.SubElement(xml_score_part, "part-name")

        # master Beat Subdivisions = 4

        for idx, score_part in enumerate(self.score_parts):
            part_number = idx + 1
            # print('Processing part: {}'.format(part_number))

            current_measure_count = 1

            # part
            xml_part = etree.SubElement(root, "part", {"id": "P" + str(part_number)})

            xml_measure = etree.SubElement(
                xml_part, "measure", {"number": str(current_measure_count)}
            )

            # part attributes
            #   -> divisions, key, time, clef
            xml_part_attributes = etree.SubElement(xml_measure, "attributes")

            xml_part_divisions = etree.SubElement(xml_part_attributes, "divisions")
            xml_part_divisions.text = str(score_part.measure_factor)

            xml_part_key = etree.SubElement(xml_part_attributes, "key")
            xml_part_fifths = etree.SubElement(xml_part_key, "fifths")
            xml_part_fifths.text = "0"
            xml_part_mode = etree.SubElement(xml_part_key, "mode")
            xml_part_mode.text = 'none'

            current_ts = score_part.time_signatures[0]
            xml_part_time = etree.SubElement(xml_part_attributes, "time")
            xml_part_beats = etree.SubElement(xml_part_time, "beats")
            xml_part_beats.text = str(current_ts[0])
            xml_part_beat_type = etree.SubElement(xml_part_time, "beat-type")
            xml_part_beat_type.text = str(current_ts[1])

            # TODO: eventually we need a clef determinant
            xml_part_clef = etree.SubElement(xml_part_attributes, "clef")
            xml_part_clef_sign = etree.SubElement(xml_part_clef, "sign")
            xml_part_clef_sign.text = "G"
            xml_part_clef_line = etree.SubElement(xml_part_clef, "line")
            xml_part_clef_line.text = "2"

            ## NOTES

            # for each Note in part's NoteList
            current_measure_count = 0
            # print(score_part.measures)
            for measure_index, current_measure in enumerate(score_part.measures):
                current_measure_count += 1
                if current_measure_count != 1:
                    xml_measure = etree.SubElement(
                        xml_part, "measure", {"number": str(current_measure_count)}
                    )
                    if measure_index > 0:
                        if (
                            current_measure.time_signature
                            != score_part.measures[measure_index - 1].time_signature
                        ):
                            xml_measure_attributes = etree.SubElement(
                                xml_measure, "attributes"
                            )
                            xml_measure_time_signature = etree.SubElement(
                                xml_measure_attributes, "time"
                            )
                            xml_measure_time_beats = etree.SubElement(
                                xml_measure_time_signature, "beats"
                            )
                            xml_measure_time_beat_type = etree.SubElement(
                                xml_measure_time_signature, "beat-type"
                            )
                            xml_measure_time_beats.text = str(
                                current_measure.time_signature[0]
                            )
                            xml_measure_time_beat_type.text = str(
                                current_measure.time_signature[1]
                            )
                for current_beat in current_measure.beats:
                    beat_subdivisions = current_beat.subdivisions
                    for current_note in current_beat.notes:
                        if type(current_note) == Rest:
                            xml_note = etree.SubElement(xml_measure, "note")
                            xml_rest = etree.SubElement(xml_note, "rest")
                            xml_rest_duration = etree.SubElement(xml_note, "duration")
                            xml_rest_duration.text = str(current_note.dur)

                        else:
                            # note
                            #   -> pitch, duration, accidental, notation ties
                            xml_note = etree.SubElement(xml_measure, "note")

                            xml_note_pitch = etree.SubElement(xml_note, "pitch")

                            # pitch step
                            xml_note_pitch_step = etree.SubElement(
                                xml_note_pitch, "step"
                            )
                            xml_note_pitch_step.text = current_note.step_name

                            # pitch alter
                            xml_note_pitch_alter = etree.SubElement(
                                xml_note_pitch, "alter"
                            )

                            xml_note_pitch_alter.text = (
                                current_note.alter
                                if xml_note_pitch_alter is not None
                                else 0
                            )

                            # pitch octave
                            xml_note_pitch_octave = etree.SubElement(
                                xml_note_pitch, "octave"
                            )
                            xml_note_pitch_octave.text = str(current_note.octave)

                            # duration
                            xml_note_duration = etree.SubElement(xml_note, "duration")
                            xml_note_duration.text = str(current_note.dur)

                            # accidental
                            if current_note.alter:
                                xml_note_accidental = etree.SubElement(
                                    xml_note, "accidental"
                                )
                                xml_note_accidental.text = current_note.accidental

                            # beam
                            if current_note.beam_start == True:
                                xml_beam = etree.SubElement(xml_note, "beam")
                                xml_beam.text = "begin"
                            elif current_note.beam_continue == True:
                                xml_beam = etree.SubElement(xml_note, "beam")
                                xml_beam.text = "continue"

                            # time modification
                            if current_beat.tuplet == True:
                                xml_time_modification = etree.SubElement(
                                    xml_note, "time-modification"
                                )
                                xml_time_modification_actual = etree.SubElement(
                                    xml_time_modification, "actual-notes"
                                )
                                xml_time_modification_actual.text = str(
                                    current_beat.actual_notes
                                )
                                xml_time_modification_normal = etree.SubElement(
                                    xml_time_modification, "normal-notes"
                                )
                                xml_time_modification_normal.text = str(
                                    current_beat.subdivisions
                                )

                            # notation ties
                            if current_note.tie_start:
                                xml_notations = etree.SubElement(xml_note, "notations")
                                xml_notations_tied = etree.SubElement(
                                    xml_notations, "tied", {"type": "start"}
                                )
                            if current_note.tie_continue:
                                xml_notations = etree.SubElement(xml_note, "notations")
                                xml_notations_tied = etree.SubElement(
                                    xml_notations, "tied", {"type": "continue"}
                                )
                            if current_note.tie_end:
                                xml_notations = etree.SubElement(xml_note, "notations")
                                xml_notations_tied = etree.SubElement(
                                    xml_notations, "tied", {"type": "stop"}
                                )

            serialized = etree.tostring(
                root,
                doctype="<!DOCTYPE score-partwise PUBLIC \"-//Recordare//DTD MusicXML 3.0 Partwise//EN\" \"http://www.musicxml.org/dtds/partwise.dtd\">",
            )

            new_root = etree.XML(serialized)
            musicxml_tree = etree.ElementTree(new_root)

            part_number += 1

        return musicxml_tree

    def _write_xml_to_file(
        self, output_filepath: str, xml_score: etree.ElementTree
    ) -> None:
        """Write MusicXML tree to output file"""
        output_filepath = pathlib.Path(output_filepath)
        xml_score.write(
            str(output_filepath),
            pretty_print=True,
            encoding="UTF-8",
            xml_declaration=True,
        )
