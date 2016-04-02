from itertools import product
import random


class CadenceGenerator(object):
    def generate(self, size=3, sample_rate=1):
        assert size >= 2
        assert sample_rate <= 1 and sample_rate > 0
        # Generate combinations of x size
        list_cadences = list(product([0, 1, 2, 3, 4, 5, 6], repeat=size))
        total_cases = len(list_cadences)
        number_samples = int(total_cases * sample_rate)
        sample_of_cadences = [list_cadences[i] for i in sorted(random.sample(xrange(total_cases), number_samples))]
        return sample_of_cadences


if __name__ == '__main__':
    cadenceGen = CadenceGenerator()
    generations = cadenceGen.generate(sample_rate=.5)
    print(generations)
