import copy
import random

from music21 import chord as chor_mus21
from music21 import midi
from music21 import note as note_mus21
from music21 import stream

from CadenceGenerator import CadenceGenerator


class MusicGenerator(object):
    def __init__(self):
        self.notes_scale = ["C", "D", "E", "F", "G", "A", "B"]
        self.chords = []
        for i in range(0, len(self.notes_scale)):
            note = self.notes_scale[i] + str(4)
            notes = [note]
            idx_next_note = (i + 2) % 7
            note = self.notes_scale[idx_next_note] + str(5) if idx_next_note < i else self.notes_scale[
                                                                                          idx_next_note] + str(4)
            notes.append(note)
            idx_next_note = (i + 4) % 7
            note = self.notes_scale[idx_next_note] + str(5) if idx_next_note < i else self.notes_scale[
                                                                                          idx_next_note] + str(4)
            notes.append(note)
            chor = chor_mus21.Chord(notes)
            self.chords.append(chor)

    def gen_midi_of_cadences(self):
        # TODO
        cadence_generator = CadenceGenerator()
        cadences = cadence_generator.generate()

        for cadence in cadences:
            score = stream.Score()
            part = stream.Part()

            for i in range(0, len(cadence)):
                chor = copy.deepcopy(self.chords[cadence[i]])
                chor.quarterLength = 2
                part.append(chor)
            score.insert(0, part)

            mf = midi.translate.streamToMidiFile(score)
            mf.open(('cadences/cad%s.midi' % '-'.join(str(e) for e in cadence)), "wb")
            mf.write()
            mf.close

    def generate(self):
        cadence_generator = CadenceGenerator()
        cadences = cadence_generator.generate()
        len_cadences = len(cadences)
        num_sequencias = 8
        score = stream.Score()
        part_chords = stream.Part()
        part_melody = stream.Part()

        for i in range(0, num_sequencias):
            cadencia = cadences[random.randint(0, len_cadences - 1)]

            num_notas_array = [8, 3, 5]

            for i in range(0, len(cadencia)):
                chor = copy.deepcopy(self.chords[cadencia[i]])
                num_notas = num_notas_array[i]
                chor.quarterLength = num_notas * .5
                part_melody.append(chor)

                # Obtemos as notas do acorde
                pitches = chor.pitches
                # Iteramos as notas do acorde pra a melodia

                velocidade_notas = random.randint(1, 2)

                for i_notas in range(0, num_notas * velocidade_notas):
                    idx_pitch = random.randint(0, len(pitches) - 1)
                    note = note_mus21.Note(pitches[idx_pitch])
                    note.quarterLength = 0.5 / velocidade_notas
                    part_chords.append(note)

        score.insert(0, part_melody)
        score.insert(0, part_chords)
        # sc.show()

        mf = midi.translate.streamToMidiFile(score)
        import datetime

        mf.open(('musics/%s.midi' % datetime.datetime.now().strftime("%Y%m%d%H%M%S")), "wb")
        mf.write()
        mf.close


if __name__ == '__main__':
    mgen = MusicGenerator()
    mgen.generate()
