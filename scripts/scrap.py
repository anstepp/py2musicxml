    def generation_algorithm(self, max_generations: int, slices: Tuple[int]):

        slice_start = slices[0]
        slice_end = slices[1]

        current_generation = [self.starting_chord]
        self.generations_list = [current_generation]
        generation = 1

        while generation < max_generations:

            generation_to_process = self.generations_list[generation - 1]
            current_generation = []

            for index, chord in enumerate(generation_to_process):

                if generation % 2 is True:

                    if chord.major is True:
                        new_chord = chord.P()
                        next_chord = new_chord.S()
                        final_chord = next_chord.P()
                        another_chord = final_chord.S()

                        current_generation.extend([chord, new_chord, next_chord, final_chord, another_chord])

                    elif chord.minor is True:
                        new_chord = chord.S()
                        next_chord = new_chord.P()
                        final_chord = next_chord.S()

                        current_generation.extend([chord, new_chord, next_chord, final_chord])

                else:

                    if chord.major is True:
                        new_chord = chord.R()
                        next_chord = new_chord.S()
                        final_chord = next_chord.R()
                        another_chord = final_chord.S()

                        current_generation.extend([chord, new_chord, next_chord, final_chord, another_chord])

                    elif chord.minor is True:
                        new_chord = chord.L()
                        next_chord = new_chord.P()
                        final_chord = next_chord.S()

                        current_generation.extend([chord, new_chord, next_chord, final_chord])

            if (len(current_generation) > slice_end):
                generation_post_slice = current_generation[slice_start:slice_end]
                self.generations_list.append(generation_post_slice)
            else:
                self.generations_list.append(current_generation)
            generation += 1