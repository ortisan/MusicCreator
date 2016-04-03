if __name__ == '__main__':




    likes = []
    import re
    import pandas as pd
    with open('like_midis.csv', 'r') as f:
        for line in f.readlines():
            cadence_search = re.search('cad(\d+(-\d)+)\.midi', line, re.IGNORECASE)
            if cadence_search:
                cadence_str = cadence_search.group(1)
                cadence = [int(x) for x in cadence_str.split('-')]
                cadence_dict = {'{0}th'.format(i): val for i, val in enumerate(cadence)}
                # Calculando as distancias entre as notas
                ith_dist_cad = [(x - cadence[i+1]) * -1 for i, x in enumerate(cadence) if i+1 < len(cadence)]
                ith_dist_dict = {'dist_{0}th'.format(i): val for i, val in enumerate(ith_dist_cad)}
                cadence_dict.update(ith_dist_dict)
                likes.append(cadence_dict)

    likes_df = pd.DataFrame(likes)
    print(likes_df)




