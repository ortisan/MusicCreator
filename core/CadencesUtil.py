from itertools import product
import random


class CadencesUtil(object):
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
        cadences_str = []
        import re
        import pandas as pd
        with open(path_file, 'r') as f:
            for line in f.readlines():
                cadence_search = re.search('cad(\d+(-\d)+)\.midi', line, re.IGNORECASE)
                if cadence_search:
                    cadence_str = cadence_search.group(1)
                    cadences_str.append(cadences_str)
                    cadence = [int(x) for x in cadence_str.split('-')]
                    cadence_dict = {'{0}th'.format(i): val for i, val in enumerate(cadence)}
                    # Calculando as distancias entre as notas
                    ith_dist_cad = [(x - cadence[i + 1]) * -1 for i, x in enumerate(cadence) if i + 1 < len(cadence)]
                    ith_dist_dict = {'dist_{0}th'.format(i): val for i, val in enumerate(ith_dist_cad)}
                    cadence_dict.update(ith_dist_dict)
                    likes_dislikes.append(cadence_dict)

        likes_dislikes_df = pd.DataFrame(likes_dislikes)
        likes_dislikes_df.set_index(cadences_str)
        return likes_dislikes_df
