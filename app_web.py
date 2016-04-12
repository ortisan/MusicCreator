from flask import Flask, url_for, render_template, redirect

app = Flask(__name__, static_folder='cadences')
import os
import csv
from random import shuffle
from core.CadencesUtil import CadencesUtil
import numpy as np


class MIDIItem(object):
    def __init__(self, name, midi_link, like_link, dislike_link, predict=0):
        self.name = name
        self.midi_link = midi_link
        self.like_link = like_link
        self.dislike_link = dislike_link
        self.predict = predict


@app.route('/')
def index():
    from os import listdir
    from os.path import isfile, join
    items = []

    cadenceUtil = CadencesUtil()
    cadenceUtil.learnFromDataset()

    for f in listdir('cadences'):
        if isfile(join('cadences', f)) and f.endswith('.midi'):
            cadence_str, intervals, distances = CadencesUtil.extractDistancesFromCadence(f)
            dist_array = np.ndarray(buffer=np.array(distances, dtype=int), shape=(1, 2), dtype=int)
            predict = cadenceUtil.classify(dist_array)[0]
            midi_item = MIDIItem(f, url_for('static', filename=f), ('/like/%s' % f), ('/dislike/%s' % f),
                                 predict=predict)
            items.append(midi_item)

    shuffle(items)

    return render_template('home.html', midi_items=items)


@app.route('/like/<name>')
def like(name):
    with open('like_midis.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([name])

    remove_midi('cadences/{0}'.format(name))

    return redirect('/')


@app.route('/dislike/<name>')
def dislike(name):
    with open('dislike_midis.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([name])

    remove_midi('cadences/{0}'.format(name))

    return redirect('/')


def remove_midi(file):
    os.remove(file)


if __name__ == '__main__':
    app.run(debug=True)
