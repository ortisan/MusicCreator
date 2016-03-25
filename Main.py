__author__ = '56789'
import copy
import random

from music21 import chord as chor_mus21
from music21 import stream
from music21 import note as note_mus21
from music21 import midi

notes_scale = ["C", "D", "E", "F", "G", "A", "B"]
chords = []
sc = stream.Score()
p1 = stream.Part()
p1.id = 'part1'

p2 = stream.Part()
p2.id = 'part2'

cadencias = [[1, 3, 0], [1, 0, 3]]
len_cadencias = len(cadencias)
fator_velocidade = [1, 2]

if __name__ == '__main__':

    for i in range(0, len(notes_scale)):
        note = notes_scale[i] + str(4)
        notes = [note]
        idx_next_note = (i + 2) % 7
        note = notes_scale[idx_next_note] + str(5) if idx_next_note < i else notes_scale[idx_next_note] + str(4)
        notes.append(note)
        idx_next_note = (i + 4) % 7
        note = notes_scale[idx_next_note] + str(5) if idx_next_note < i else notes_scale[idx_next_note] + str(4)
        notes.append(note)
        chor = chor_mus21.Chord(notes)
        chords.append(chor)

    num_sequencias = 8

    for i in range(0, num_sequencias):
        cadencia = cadencias[random.randint(0, len_cadencias - 1)]

        num_notas_array = [8, 3, 5]

        for i in range(0, len(cadencia)):
            chor = copy.deepcopy(chords[cadencia[i]])
            num_notas = num_notas_array[i]
            chor.quarterLength = num_notas * .5
            p2.append(chor)

            # Obtemos as notas do acorde
            pitches = chor.pitches
            # Iteramos as notas do acorde pra a melodia

            velocidade_notas = random.randint(1, 2)

            for i_notas in range(0, num_notas * velocidade_notas):
                idx_pitch = random.randint(0, len(pitches) - 1)
                note = note_mus21.Note(pitches[idx_pitch])
                note.quarterLength = 0.5 / velocidade_notas
                p1.append(note)

    sc.insert(0, p2)
    sc.insert(0, p1)
    # sc.show()

    mf = midi.translate.streamToMidiFile(sc)
    import datetime

    mf.open(('%s.midi' % datetime.datetime.now().strftime("%Y%m%d%H%M%S")), "wb")
    mf.write()
    mf.close
