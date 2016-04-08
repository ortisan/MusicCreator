import os.path
import random
from itertools import product

import pandas as pd
from sklearn.externals import joblib
from sklearn.multiclass import OutputCodeClassifier
from sklearn.svm import LinearSVC



class CadencesUtil(object):
    MODEL_CLF = '../model/cadence_clf.pkl'

    def __init__(self):
        if os.path.isfile(CadencesUtil.MODEL_CLF):
            self.clf = joblib.load(CadencesUtil.MODEL_CLF)

    def generate(self, size=3, sample_rate=1):
        assert size >= 2
        assert sample_rate <= 1 and sample_rate > 0
        # Generate combinations of x size
        list_cadences = list(product([0, 1, 2, 3, 4, 5, 6], repeat=size))
        total_cases = len(list_cadences)
        number_samples = int(total_cases * sample_rate)
        sample_of_cadences = [list_cadences[i] for i in sorted(random.sample(xrange(total_cases), number_samples))]
        return sample_of_cadences

    def getLikesCadences(self):
        cadences = []
        import re
        with open('like_midis.csv', 'r') as f:
            for line in f.readlines():
                cadence_search = re.search('cad(\d+(-\d)+)\.midi', line, re.IGNORECASE)
                if cadence_search:
                    cadence_str = cadence_search.group(1)
                    cadence = [int(x) for x in cadence_str.split('-')]
                    cadences.append(cadence)
        return cadences

    def getDataframeFromCsvLikeDislike(self, path_file):
        likes_dislikes = []
        import re

        with open(path_file, 'r') as f:
            for line in f.readlines():
                cadence_search = re.search('cad(\d+(-\d)+)\.midi', line, re.IGNORECASE)
                if cadence_search:
                    cadence_str = cadence_search.group(1)
                    cadence = [int(x) for x in cadence_str.split('-')]
                    cadence_dict = {'{0}th'.format(i): val for i, val in enumerate(cadence)}
                    cadence_dict['cadence'] = cadence_str
                    # Calculando as distancias entre as notas
                    ith_dist_cad = [(x - cadence[i + 1]) * -1 for i, x in enumerate(cadence) if i + 1 < len(cadence)]
                    ith_dist_dict = {'dist_{0}th'.format(i): val for i, val in enumerate(ith_dist_cad)}
                    cadence_dict.update(ith_dist_dict)
                    likes_dislikes.append(cadence_dict)

        likes_dislikes_df = pd.DataFrame(likes_dislikes)

        return likes_dislikes_df

    def learnFromDataset(self):
        like_df = self.getDataframeFromCsvLikeDislike('../like_midis.csv')
        like_df['like'] = 1
        dislike_df = self.getDataframeFromCsvLikeDislike('../dislike_midis.csv')
        dislike_df['like'] = 0

        data_concat = pd.concat([like_df, dislike_df])

        data_model = (data_concat[['dist_0th', 'dist_1th']]).as_matrix()
        # Transforma o [[1],[2],[3]] em [1,2,3]
        labels = (data_concat[['like']].astype('str')).as_matrix().ravel()

        self.clf = OutputCodeClassifier(LinearSVC(random_state=0), code_size=2, random_state=0)
        self.clf.fit(data_model, labels)

        joblib.dump(self.clf, CadencesUtil.MODEL_CLF)

    def classify(self, rows):
        assert (self.clf is not None), "Model must be initialized"
        return self.clf.predict(rows)


if __name__ == '__main__':
    cadence = CadencesUtil()
    cadence.getDataframeFromCsvLikeDislike('../like_midis.csv')

    cadence.learnFromDataset()
