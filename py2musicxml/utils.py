def fix_pitch_overflow(octave, pitch_class):
    new_pitch_class, new_octave = None, None

    if pitch_class > 11:
        new_pitch_class = pitch_class % 12
        new_octave = octave + pitch_class // 12
        return new_octave, new_pitch_class

    elif pitch_class < 0:
        new_pitch_class = pitch_class % 12
        new_octave = octave + pitch_class // 12
        return new_octave, new_pitch_class

    else:
        return octave, pitch_class
