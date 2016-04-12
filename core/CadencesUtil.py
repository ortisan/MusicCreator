import os.path
import random
import re
from itertools import product, combinations_with_replacement

import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn.linear_model import Perceptron
from Configs import Configs


class CadencesUtil(object):
    MODEL_CLF = '%s/model/cadence_clf.pkl' % Configs.get_project_home()

    @classmethod
    def extractDistancesFromCadence(cls, filename):
        cadence_search = re.search('cad(\d+(-\d)+)\.midi', filename, re.IGNORECASE)
        if cadence_search:
            cadence_str = cadence_search.group(1)
            intervals = [int(interval) for interval in cadence_str.split('-')]
            # distances from intervals
            distances = [(interval - intervals[i + 1]) * -1 for i, interval in enumerate(intervals) if
                         i + 1 < len(intervals)]
            return cadence_str, intervals, distances
        else:
            raise Exception('Invalid file name')

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
        with open('%s/like_midis.csv' % Configs.get_project_home(), 'r') as f:
            for line in f.readlines():
                cadence_search = re.search('cad(\d+(-\d)+)\.midi', line, re.IGNORECASE)
                if cadence_search:
                    cadence_str = cadence_search.group(1)
                    cadence = [int(x) for x in cadence_str.split('-')]
                    cadences.append(cadence)
        return cadences

    def getDataframeFromCsvLikeDislike(self, path_file):
        likes_dislikes = []
        with open(path_file, 'r') as f:
            for line in f.readlines():
                cadence_str, intervals, distances = CadencesUtil.extractDistancesFromCadence(line)
                cadence_dict = {'{0}th'.format(i): val for i, val in enumerate(distances)}
                cadence_dict['cadence'] = cadence_str
                ith_dist_dict = {'dist_{0}th'.format(i): val for i, val in enumerate(distances)}
                cadence_dict.update(ith_dist_dict)
                likes_dislikes.append(cadence_dict)
        likes_dislikes_df = pd.DataFrame(likes_dislikes)

        return likes_dislikes_df

    def learnFromDataset(self):

        if os.path.isfile(Configs.get_project_home() + '/like_midis.csv') and os.path.isfile(
                        Configs.get_project_home() + '/dislike_midis.csv'):
            like_df = self.getDataframeFromCsvLikeDislike(Configs.get_project_home() + '/like_midis.csv')
            like_df['like'] = 1
            dislike_df = self.getDataframeFromCsvLikeDislike(Configs.get_project_home() + '/dislike_midis.csv')
            dislike_df['like'] = 0

            data_concat = pd.concat([like_df, dislike_df])

            data_model = (data_concat[['dist_0th', 'dist_1th']]).as_matrix()
            # Transforma o [[1],[2],[3]] em [1,2,3]
            labels = (data_concat[['like']].astype('str')).as_matrix().ravel()

            self.clf = Perceptron()
            self.clf.fit(data_model, labels)

            joblib.dump(self.clf, CadencesUtil.MODEL_CLF)

    def classify(self, rows):
        assert (self.clf is not None), "Model must be initialized"
        return self.clf.predict(rows)


if __name__ == '__main__':
    cadence = CadencesUtil()
    cadence.learnFromDataset()

    combinations = combinations_with_replacement([1, 2, 3, 4, 5], 2)

    x = np.array(list(combinations), dtype=int)
    print cadence.classify(x)

    y = np.ndarray(buffer=np.array([1, 1]), shape=(1, 2))
    print cadence.classify(y)
