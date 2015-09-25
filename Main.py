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

cadencias = [[1, 3, 0], [0, 4, 0, 3], [3, 0]]
len_cadencias = len(cadencias)
quarter_lengths = [.5, .25]

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
        for i in range(0, len(cadencia)):
            chor = copy.deepcopy(chords[cadencia[i]])
            chor.quarterLength = 1
            p1.append(chor)

        res = note_mus21.Rest()
        res.quarterLength = .5
        p1.append(res)

        pitches = chor.pitches

        # Sorteia o numero de notas que serao melodicas
        num_notes = random.randint(3, 6)

        for i in range(0, num_notes):
            n1 = random.randint(0, 2)
            note = copy.deepcopy(note_mus21.Note(pitches[n1]))
            idx_factor_duration = random.randint(0, 1)
            # duracao da nota sera dinamica variando em 0.5 a 0.75
            q_length = quarter_lengths[idx_factor_duration]
            note.quarterLength = q_length
            p1.append(note)

        res = note_mus21.Rest()
        res.quarterLength = .5
        p1.append(res)

    sc.insert(0, p1)
    sc.show()

    mf = midi.translate.streamToMidiFile(sc)
    mf.open("music.midi", "wb")
    mf.write()
    mf.close

