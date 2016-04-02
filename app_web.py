from flask import Flask, url_for, render_template, redirect

app = Flask(__name__, static_folder='cadences')


class MIDIItem(object):
    def __init__(self, name, midi_link, liked_link):
        self.name = name
        self.midi_link = midi_link
        self.liked_link = liked_link


@app.route('/')
def index():
    from os import listdir
    from os.path import isfile, join
    items = []
    for f in listdir('cadences'):
        if isfile(join('cadences', f)) and f.endswith('.midi'):
            midi_item = MIDIItem(f, url_for('static', filename=f), ('/liked/%s' % f))
            items.append(midi_item)
    return render_template('home.html', midi_items=items)


@app.route('/liked/<name>')
def like(name):
    import csv
    with open('liked_midis.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([name])

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
