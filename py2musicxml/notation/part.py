import copy
import fractions, math
import logging

from lxml import etree
from typing import Iterable, List, Optional, NamedTuple, Tuple, Union

from .measure import Measure
from .note import Note
from .beat import Beat
from .rest import Rest

logging.basicConfig(level=logging.DEBUG)

# from collections import namedtuple

TimeSignature = Tuple[int, int]
TimeSignatures = List[Tuple[int, int]]


class CurrentCountDivisions(NamedTuple):
    """
    A class containing all the relevant divisions related to current_count.

    A class to be invoked to keep track of various subdivisions needed 
    when grouping the current_list into Beat objects inside Measure objects.
    Should not be created or called by the end user.

    Attributes:
    -----------

    beat_floor (int): floor division of current_count the remainder of
    current_note

    beat_mod (int): modulo division of current_count and the remainder of
    current_note

    measure_floor (int): floor divsion of current_count and the max measure divsions

    measure_mod (int): mod division of current_count and the max measure divisions 

    Methods:
    --------

    None.

    """
    beat_floor: int
    beat_mod: int
    measure_floor: int
    measure_mod: int


class Part:

    """
    The part class represents a musical part. A Part can contain more than
    one staff.

    A part object can be invoked inside an instrument.

    Attributes:
    -----------
    
    current_list: a list of note objects that can be operated upon

    measures: a list of measures. This begins empty, and is created when 
    _get_measure_list() is invoked inside create_part on instantiation.

    time_signatures: a list or singleton of time_signatures that is cycled
    over to generate each measure's time signature.

    time_signature_index: a counter for the current time signature.

    subdivisions:

    max_subdivisions:
    
    current_beat_count:

    current_measure:

    current_count_mod:

    current_count_floor:

    measure_factor:

    Methods:
    --------

    create_part: create the part with the current Time Signatures.

    """

    def __init__(self, 
        input_list: Iterable[Note], 
        time_signatures: TimeSignatures, 
        key = 0,
        clef='G',
        line=2):
        """
        Create a Part object.

        Creating a Part object sets off a cascade of events, creating a list of Measure objects
        containing Beat objects, containing Note objects. Measures should generally not be created
        directly by the end user, but through modifying the note list, then calling create_part().
        Otherwise, there is no guarantee that the measure object is accurately taken into account
        with the other arguments given.

        Arguments:
        ----------

        input_list (list[Note]): a list of Note objects. They can be of any duration.

        time_signatures (tuple[TimeSignature]): a tuple of TimeSignature(s). If one TimeSignature
        is given, the entire part is that time signature. Otherwise, the Time Signatures are cycled
        through.

        key (int): pitch class for the major key of the desired key signature.

        clef (char): Letter Name for the clef for the part.

        line (int): line for the clef to be "centered" on.

        Returns:
        --------

        A Part object.

        """

        self.current_list = input_list

        for note in self.current_list:
            if note is type(Note):
                note._get_step_name(key)

        self.measures = []

        # TS stuff
        self.time_signatures = time_signatures
        self.time_signature_index = 0

        self.subdivisions, self.max_subdivisions = None, None

        # where we are in the cumulative beats
        self.current_beat_count = None
        self.current_measure = None
        # value of note duration that needs to be written
        # current count gets incremented when we intake the next note
        # gets decremented when we write a measure
        self.current_count = 0

        # current count mod or floor divided by current cumulative beat
        self.current_count_mod, self.current_count_floor = None, None

        #  self.current_measure_mod, self.current_measure_floor

        dur_uniques = self.get_note_uniques()
        denominator_uniques = self.get_ts_uniques()
        self.measure_factor = self._get_factor(dur_uniques) * max(denominator_uniques)

        self.create_part()

    """default behavior is to simply clean an input list to 4/4
       it's also an option to feed extra arguments with keywords to 
       modify behavior for optional cleaning methods or user choices
       for measure groupings of factors"""

    def _test_for_low_bottom_time_sig(self, time_sig: TimeSignature, measure_factor: int) -> int:
        """
        Evaulates if TimeSignature is valid or needs to be scaled.

        Arguments:
        ----------
        time_sig: a TimeSignature

        measure_factor (int): a scaling factor for the measure (usually acquired internally).

        """
        if time_sig[1] < 3:
            new_measure_factor = measure_factor * time_sig[1]
            return new_measure_factor
        elif time_sig[1] > 4:
            new_measure_factor = (4 / time_sig[1])
            return new_measure_factor
        else:
            return measure_factor


    def create_part(self):
        """
        Transform input list of notes into a list of measures.

        Wrapper function for the plethora of actions taken to divide the current_list into
        measures.

        Arguments:
        ----------

        None.

        Returns:
        --------

        Nothing. List is handled internally.
        """
        self._group_list_to_measures()

    def get_note_uniques(self) -> list:
        """
        Removes dupes of durs in list of Note objects.

        If a duration has yet to be listed, it appends it to the uniques. This is essential
        toward developing the factor, as note values are dependant upon being 1) integers, 
        and 2) scaled to the time signature of the XML in MusicXML.

        Arguments:
        ----------

        None.

        Returns:
        --------

        uniques (list[int]): a list of unique durations in the current_list.


        """
        uniques = []
        for item in self.current_list:
            if item.dur not in uniques:
                uniques.append(item.dur)
            else:
                pass
        return uniques

    def get_ts_uniques(self) -> list:
        '''unique durations of the notes in the list'''
        uniques = []
        for item in self.time_signatures:
            if item[1] not in uniques:
                uniques.append(item[1])
            else:
                pass
        return uniques

    def _get_factor(self, input_list: list) -> int:
        """
        Returns a factor (int) that scales all duration values to ints.
    
        Converts all durations to fractions, then finds the least common multiple. This is
        then returned as the factor to scale durations for MusicXML.

        Arguments:
        ----------

        input_list (list[float]): list of unique durations. (See _get_uniques).

        Returns:

        factor (int): scaling factor for MusicXML.    

        """
        fractional_list = [fractions.Fraction(x).limit_denominator(128) for x in input_list]
        denominators = [x.denominator for x in fractional_list]
        if denominators:
            lcm = denominators[0]
            for i in denominators[1:]:
                lcm = int(lcm * i / math.gcd(lcm, i))
            factor = lcm
        else:
            factor = 1

        return factor

    def _assign_measure_weight(self):
        """
        Assign weight for hypermetric ranking.

        Assigns a weight to the measure based on rules. Not yet implemented.

        Arguments:
        ----------

        None.

        Returns:
        --------

        None.
        """
        weight = 0
        for index, measure in enumerate(self.measures):
            self._get_change_pitch(10)

    def _compare_weight(self):
        pass

    def _get_index_range(self, index: int, search_range: int) -> Tuple[int, int]:
        """
        Returns range for searching for hypermetric analysis.

        Not yet implemented. Cleans a search range for beginning and ends of a list.

        Arguments:
        ----------

        index (int): location of note to compare in measure list.

        search_range (int): adjacent measures on both sides
        """
        if index < search_range:
            return 0, search_range + index
        else:
            return index - search_range, index + search_range

    def _get_change_pitch(self, index: int) -> None:
        """
        Tests the change in pitch between measure starts in search range and
        weights the measure appropriately.

        Evaluates the differences in measure pitch between search index, ranking a pitch
        that is a local maxima higher and weighting the measure accordingly.

        Arguments:
        ----------

        index (int): index of measure to evaulate.

        Returns:
        --------

        None, measure ranking is held in measure object.
        """
        index_range_low, index_range_high = self._get_index_range(index)
        test_measure_pitch = self.measures[index].beats[0]

        # test downbeats
        for measure in self.measures[index_range_low:index_range_high]:
            if measure.beats[0] > test_measure_pitch:
                break
            else:
                self.weight += 1
        for measure in self.measures:
            if measure.beats[0] < test_measure_pitch:
                break
            else:
                self.weight += 1

    def _get_change_group(self):
        """
        Placeholder.
        """
        pass

    def _get_implied_meter(self):
        """
        Evaluate note list to break into groupings of 2 and 3 and attempts to define
        metric weight and assigns a TimeSignature to groupings.

        Evaluates pitch strength in metric and hypermetric terms, and attempts to create
        a TimeSignature to subdivide note list. Not accurate, very risky, use at own risk.

        Arguments:
        ----------

        None.

        Returns:
        --------

        None.
        """
        location_map = []
        pitch_locations = self.get_change_pitch()
        meter_locations = self.get_change_group()
        highest_level = [
            pitch
            for pitch, meter in zip(pitch_locations, meter_locations)
            if pitch == meter
        ]
        last_location = 0
        # perhaps wrap this in a smaller function and make it recurisve? Is there a non-recusrive way to make this work?
        for location in highest_level:
            subgroup = self.current_list[last_location:location]
            groups_2_and_3 = self.metric_finder(
                subgroup
            )  # or should I use the .get_change_pitch() and .get_change_group()
            location_map.append(groups_2_and_3)
            location = last_location
        implied_list = self.group_by_map(location_map)
        return implied_list

    def _advance_time_signature_index(self) -> None:
        """
        Advances the time signature index in the list or cycle object.

        Called when a note plus current_count equals or exceeds the maximum duration
        of current_measure. Does not perform any cleanup for measure termination in
        grouping algorithm.

        Arguments:
        ----------

        None.

        Returns:
        --------

        None.
        """
        self.time_signature_index = (self.time_signature_index + 1) % len(
            self.time_signatures
        )

    def _append_and_increment_measure(self) -> None:
        """
        Called when a measure is full to clean up last Measure and instantiate new
        Measure object.

        Cleans up the current_measure by filling with last Beat, appending the Measure,
        advancing the TimeSignature, and defining characteristics of the new measure.

        Arguments:
        ----------

        None.

        Returns:
        --------

        None.

        Call this function to advance to the next measure.
            This should only be called when a measure is full, that is,
            current_beat_count is full, or the subdivisions are full.

        """

        if len(self.current_beat.notes) > 0:
            self.current_measure.add_beat(self.current_beat)

        logging.debug(f"Appending measure: {len(self.current_measure.beats)}")

        self.measures.append(self.current_measure)

        self._advance_time_signature_index()
        self.current_measure_factor = self.measure_factor

        self.current_measure = Measure(
            self.time_signatures[self.time_signature_index], self.current_measure_factor
        )

        self.max_subdivisions = self.current_measure.total_cumulative_beats
        self.current_beat_count = 0
        self.subdivisions = self.current_measure.cumulative_beats[
            self.current_beat_count
        ]

        self.current_beat = Beat(self.subdivisions)

        self.current_beat_count = 0


    def advance_current_beat_count(self) -> None:
        """If the measure is full of beats, we need to append the measure
        and advance to a new measure. Otherwise, just advance the current
        count"""


        self.current_beat_count += 1
        if self.current_beat_count >= len(self.current_measure.cumulative_beats):
            pass
        else:
            self.current_measure.add_beat(self.current_beat)
            self.subdivisions = self.current_measure.cumulative_beats[
                self.current_beat_count
            ]

    def make_whole_measure_note(self, 
        note: Note, 
        duration: int, 
        advance: int, 
        tie: bool, 
        first: bool, 
    ) -> None:
        """
        Invoked when a current_note or a subdivsion thereof is a complete measure to flag a
        whole_measure_note in the current_beat.

        Creates a deep copy of the current note, changes the duration to the measure, and
        flags for ties appropriately. Evaulation is based on the boolean arguments first and
        and tie, and sets flags directly.

        Arguments:
        ----------

        duration (int): duration of the measure.

        advance (int): unused placeholder.

        tie (bool): does this note need a tie, True/False.

        first (bool): is this the first subdivision of the note: True/False.
        """

        logging.debug("in make whole measure")
        note_to_add = copy.deepcopy(note)

        logging.debug("dur is", duration)
        note_to_add.dur = duration * self.current_measure_factor
        #print(note_to_add)

        if isinstance(note_to_add, Note):
            if tie and first:
                note_to_add.set_as_tie('tie_start')
            elif tie and not first:
                note_to_add.set_as_tie('tie_continue')
            elif not first:
                note_to_add.set_as_tie('tie_end')
            else:
                pass
        else:
            pass
        # print(note_to_add)
        self.current_beat.add_note(note_to_add)
        self.current_beat.multi_beat = True
        self._append_and_increment_measure()

    def _make_multi_beat_rest(self, rest: Rest, advance: int) -> None:
        """
        In the case that a rest is more than one beat, appropriately divide and add it
        to current_measure.

        Not quite musically accurate yet.

        Arguments:
        ----------

        rest (Rest): pass the current_note as a rest in.

        advance (int): measures the advance for the current beat.

        Returns:
        --------

        None.
        """
        multi_beat = Beat(self.subdivisions)
        multi_beat.add_note(rest)
        self.current_measure.add_beat(multi_beat)
        for index in range(advance):
            self._advance_current_beat_count()

    def _full_measure_tie_check(self) -> bool:
        """
        Evaluates if the the note that lasts the duration of current_measure
        needs to be tied.

        If current_measure_floor exceeds 1, the note is set to tie, as there is duration
        left to be portioned out to a the next Measure. Else, do not attempt to set tie
        flag in the note.

        Arguments:
        ----------

        None.

        Returns:
        --------

        Bool.
        """
        if self.current_measure_floor >= 1:
            return True
        else:
            return False

    def _sub_measure_divisions(self, note: Note, remiainder: float, div: int, first: bool) -> Optional[Note]:
        """
            Args:
                div: current beat divisions
        """

        logging.debug('in sub measure divisions', self.current_count, div)
        leftover_note = None

        if self.current_count > div * self.current_measure_factor:
            logging.debug("first div", self.current_count, div)
            self.make_whole_measure_note(note, div, div, True, first)
            logging.debug('pre minus', div, self.current_count)
            self.current_count -= div * self.current_measure_factor
            self.set_current_count_adjacencies()
            logging.debug('post minus', div, self.current_count)
            # This seems impossible, but there's zero value notes somehow...
            if self.current_count > 0:
                leftover_note = copy.deepcopy(note)
                leftover_note.dur = self.current_count
        
        elif self.current_count == div * self.current_measure_factor:
            logging.debug('second div', self.current_count, div)
            self.make_whole_measure_note(note, div, div, False, first)
            self.current_count = 0
            self.set_current_count_adjacencies()
        
        elif self.current_count < div * self.current_measure_factor:
            logging.debug('third div', self.current_count, div)
            leftover_note = copy.deepcopy(note)
            logging.debug("current", self.current_count)
            leftover_note.dur = self.current_count
            if isinstance(leftover_note, Note):
                leftover_note.set_as_tie('tie_end')
        
        if leftover_note:
            logging.debug('leftover')
            return leftover_note
        else:
            logging.debug('no leftover_note', self.current_count)
            return None


    def get_internal_measures(self, note: Note, remainder: float, post_tie: bool) -> int:

        # Get any remainder of the note that belongs in the last measure

        logging.debug("current_count", self.current_count)

        leftover_note = None
        first = post_tie

        # Test for all subdivisions being equal

        if remainder:
            logging.debug('in remainder')
            note_dur_for_old_measure = self.measure_max_subdivisions - remainder
            note_to_add_to_old_measure = copy.deepcopy(note)
            note_to_add_to_old_measure.dur = note_dur_for_old_measure
            note_to_add_to_old_measure.set_as_tie('tie_start')
            self.current_beat.add_note(note_to_add_to_old_measure)
            self.current_count -= self.measure_max_subdivisions
            self.append_and_increment_measure()



        if self.current_measure.equal_divisions:

            logging.debug('in equal divisions')

            counter = 0
            # how many measures do we need to write
            for x in range(self.current_measure_floor):
                logging.debug('while both are greater', self.current_measure_floor, self.current_count)
                """This uses the type of measure to write a whole measure.
                Eventually, we need to take cases of dotted notes that cross
                one level of subdivisions, as well as half notes in 3 and 4/4"""
                if self.current_measure.meter_division == "Duple":
                    div = 2
                    leftover_note = self._sub_measure_divisions(note, remainder, div, first)

                elif self.current_measure.meter_division == "Triple":
                    div = 3
                    leftover_note = self._sub_measure_divisions(note, remainder, div, first)

                elif self.current_measure.meter_division == "Quadruple":
                    div = 4
                    leftover_note = self._sub_measure_divisions(note, remainder, div, first)

                first = False

        # FIXME: break for asymmetric meter - ANS
        else:
            pass


        if leftover_note:      
            last_current_count = leftover_note.dur
        else:
            last_current_count = 0
        return last_current_count, leftover_note

    def _set_current_count_adjacencies(self) -> None:
        self.current_count_floor = self.current_count // self.subdivisions
        self.current_count_mod = self.current_count % self.subdivisions
        self.current_measure_floor = self.current_count // self.max_subdivisions
        self.current_measure_mod = self.current_count % self.max_subdivisions

    def _get_current_count_divisions(
        self,
        current_count: int,
        measure_subdivisions: int,
        measure_max_subdivisions: int,
    ) -> CurrentCountDivisions:
    """
    
    """
        return CurrentCountDivisions(
            beat_floor=current_count // measure_subdivisions,
            beat_mod=current_count % measure_subdivisions,
            measure_floor=current_count // measure_max_subdivisions,
            measure_mod=current_count % measure_max_subdivisions,
        )


    def wrap_up(self, remainder: int) -> None:
        if remainder:
            the_final_rest = Rest(remainder)
            the_final_rest.is_measure = False
            final_beat = Beat(remainder)
            final_beat.add_note(the_final_rest)
            self.current_measure.add_beat(final_beat)
            self.measures.append(self.current_measure)


    def _test_for_chord(
        self, 
        note: Union[Note, Rest], 
        advance_note: Union[Note, Rest], 
    ) -> bool:

        if not isinstance(note, Rest):

            if isinstance(advance_note, Note):

                if advance_note.is_chord_member:

                    """Do not advance current count if note is member of a chord."""

                    self.current_beat.add_note(note)
                    return False

                else:

                    self.current_count += round(note.dur * self.current_measure_factor)
                    return True

            else:
                self.current_count += round(note.dur * self.current_measure_factor)
                return True

        else:

            self.current_count += round(note.dur * self.current_measure_factor)
            return True



    def _group_list_to_measures(self) -> None:

        self.current_measure_factor = self.measure_factor

        self.current_measure = Measure(
            self.time_signatures[self.time_signature_index], self.current_measure_factor
        )

        if self.current_measure.equal_divisions is False:
            denominator = self.current_measure.time_signature[1]
            if denominator > 4:
                self.current_measure_factor = self.current_measure_factor * (denominator / 2)
            else:
                pass

        # how many beats in measure we have traveled
        self.current_beat_count = 0

        # keep track of how full the beat is

        # MEASURE subdivisions and max subdivisions
        self.subdivisions = self.current_measure.cumulative_beats[
            self.current_beat_count
        ]

        self.current_beat = Beat(self.subdivisions)

        self.max_subdivisions = self.current_measure.total_cumulative_beats

        remainder = 0
        for location, note in enumerate(self.current_list):

            if location + 1 < len(self.current_list):
                advance_location = location + 1
                advance_note = self.current_list[advance_location]
            else:
                advance_location = False
                advance_note = False

            """Iterate through the list of notes and group them into
            measures and beats. As we iterate, we advance a counter called
            current_count (that persists outside this function) to measure
            how many counts that need to be allocated. It gets
            incrememted when we have a new note, and either set to zero or 
            decrememted when measures pass."""            

            if note:

                if advance_note:
                    non_chord = self._test_for_chord(
                        note, advance_note
                    )

                else:
                    non_chord = True
                    self.current_count += round(note.dur * self.current_measure_factor)
                    #print("current count",self.current_count)
                    
                if non_chord:

                    logging.debug("new iteration", note, self.current_count, self.current_beat.notes)

                    """We call this function now, and when current count changes
                    to set variables to measure the relationship of the current count
                    to the measure length."""
                    self._set_current_count_adjacencies()

                    if self.current_measure_floor == 1 and self.current_measure_mod == 0:
                        measure_or_less_test = True
                    else:
                        measure_or_less_test = False

                    if measure_or_less_test or self.current_measure_floor == 0:
                        logging.debug("less than a measure, location {}, note {}, remainder {}, current_count {}, current_measure_floor {}, current_measure_mod {}, max_subdivisions {}".format(location, note, remainder, self.current_count, self.current_measure_floor, self.current_measure_mod, self.max_subdivisions))
                        note_to_add = copy.deepcopy(note)
                        note_to_add.dur = self.current_measure_factor * note_to_add.dur
                        #print("adding note", note_to_add)
                        self.current_beat.add_note(note_to_add)

                        if self.current_count < self.max_subdivisions:
                            remainder = self.current_count

                        else:
                            self._append_and_increment_measure()
                            self.current_count = 0
                            self._set_current_count_adjacencies()
                            remainder = 0

                    if self.current_measure_floor >= 1:
                        logging.debug("over a measure, location {}, note {}, remainder {}, current_measure_floor {}, current_measure_mod {}, current_count {}, max_subdivisions {}".format(location, note, remainder, self.current_measure_floor, self.current_measure_mod, self.current_count, self.max_subdivisions))
                        if remainder > 0:
                            """In this case, we have leftover note duration from the previous
                            measure. We write that note, then decrement current_count to reflect
                            that note being written."""
                            if self.current_count >= self.max_subdivisions:
                                logging.debug('current count bigger than max subdivisions')
                                last_measure_remaining_duration = (
                                    self.max_subdivisions - remainder
                                )
                                note_to_add_to_old_measure = copy.deepcopy(
                                    note
                                )
                                note_to_add_to_old_measure.notation = []
                                note_to_add_to_old_measure.dur = (
                                    last_measure_remaining_duration
                                )
                                if isinstance(note_to_add_to_old_measure, Note):
                                    note_to_add_to_old_measure.set_as_tie('tie_start')
                                else:
                                    pass
                                # print(note_to_add_to_old_measure)
                                self.current_beat.add_note(note_to_add_to_old_measure)
                                self.current_count -= self.max_subdivisions
                                logging.debug("cc", self.current_count)
                                # print(self.current_count)
                                self._append_and_increment_measure()
                                self._set_current_count_adjacencies()
                                # print("over a measure adj, location {}, note {}, current_measure_floor {}, current_measure_mod {}, current_count {}, max_subdivisions {}".format(location, note, self.current_measure_floor, self.current_measure_mod, self.current_count, self.max_subdivisions))
                                remainder = 0

                            else:
                                logging.debug('in over else', note)
                                self.current_beat.add_note(note)
                                remainder = self.max_subdivisions - self.current_count

                                logging.debug('remainder', remainder)
                                self.set_current_count_adjacencies()

                        # Our current count exceeds the max duration of the current measure
                        if (
                            self.current_measure_floor >= 1
                            and self.current_count >= self.max_subdivisions
                        ):
                            logging.debug("get_internal_measures, ")
                            # use this to clean up the measures that exist

                            # there is at least one measure to be filled
                            # ie break into measures and beats
                            if note.dur > self.current_count:
                                first = False
                            else:
                                first = True

                            remainder, leftover_note = self.get_internal_measures(note, remainder, first)

                            if leftover_note:
                                logging.debug("adding leftovers", leftover_note, remainder)
                                self.current_beat.add_note(leftover_note)
                                self.current_count = leftover_note.dur

                        elif self.current_count > 0:
                            logging.debug("tail, location {}, dur {}, current_count {}".format(location, note.dur, self.current_count))
                            note_to_add_to_old_measure = copy.deepcopy(note)
                            note_to_add_to_old_measure.dur = self.current_count
                            self.current_beat.add_note(note_to_add_to_old_measure)

                            remainder = self.current_count

                    else:
                        pass

                else:
                    pass

        if remainder:
            self.current_measure.add_beat(self.current_beat)
            self._wrap_up(self.max_subdivisions - remainder)
        else:
            self.measures.append(self.current_measure)
