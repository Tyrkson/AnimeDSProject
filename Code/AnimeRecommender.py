import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

'''

THIS CODE IS BASED ON ANOTHER CODE FROM THE LINK BELOW:
https://www.kaggle.com/shahrukhkhan/which-anime-should-you-watch-next?select=rating.csv

'''

anime = pd.read_csv('../data/anime.csv')
rating = pd.read_csv('../data/rating.csv')


#Testisime meie peal, lisasime ennast
bokuanimedenimed = [5114, 121, 31772, 31704, 30276, 34134, 16498, 31964, 33486, 25777, 199, 164, 1535, 431, 11757, 20]
bokuanimederatingud = [10, 8, 8, 10, 10, 7, 10, 10, 10, 8, 10, 10, 10, 10, 4, 6]


bokuanimedenimed = [32281, 28851, 16782, 199, 1689]
bokuanimederatingud = [3, 4, 2, 3, 5]

bokuanimedenimed = [8460, 17895]
bokuanimederatingud = [10, 8]

#print(len(rating))
for i in range(len(bokuanimederatingud)):
    rating.loc[-1] = [100000, bokuanimedenimed[i], bokuanimederatingud[i]]
    rating.index = rating.index + 1
    rating = rating.sort_index()
#print(len(rating))
#print(rating[rating['user_id'] == 100000])

def puhasta(user):
    animede_list = rating[(rating['rating'] != -1) & (rating['user_id'] == user)]['anime_id'].tolist()
    if len(animede_list) == 0:
        return []
    sarnased_hinnangud = rating[(rating['rating'] != -1) & rating['anime_id'].isin(animede_list)]['user_id'].tolist()
    tulemus = []
    protsent = 1
    dictionary = {}
    for i in sarnased_hinnangud:
        if i in dictionary:
            dictionary[i] += 1
        else:
            dictionary[i] = 1

    while len(tulemus) < 1000:
        for i in dictionary:
            if i not in tulemus:
                if dictionary[i] >= len(animede_list) * protsent:
                    tulemus.append(i)

        protsent *= 0.75
        #print(len(tulemus))
    return tulemus


def leidaparimanime(kasutajad, algkasutajavaadatud):
    dictionary = {}
    kasutajaVaadatud = []
    for i in kasutajad:
        animed = rating[(rating['user_id'] == i) & (rating['rating'] > 5)]['anime_id'].tolist()
        for y in animed:
            kasutajaVaadatud.append(y)

    for i in kasutajaVaadatud:
        if i in dictionary:
            dictionary[i] += 1
        else:
            dictionary[i] = 1

    for i in algkasutajavaadatud:
        if i in dictionary:
            del dictionary[i]
    dictSorted = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)

    #print(dictSorted[0])
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    '''for i in dictSorted:
    	if i[1] > 2:
    		print(anime[anime['anime_id'] == i[0]])'''
    print(anime[anime['anime_id'] == dictSorted[0][0]])


user = 100000

#print(len(rating))
puhastatud = puhasta(user)

if len(puhastatud) == 0:
    print("Sa ei ole midagi hinnanud või vaadanud!")
    import sys
    sys.exit(0)

rating = rating[rating['user_id'].isin(puhastatud)]
#print(len(rating))

#times_rated = rating.groupby(['anime_id'])['rating'].count()
#times_rated = times_rated.rename('times_rated')

#rating = rating.merge(times_rated, on='anime_id')
# rating = rating[rating['times_rated']>10]

anime_rating = anime.merge(rating, on='anime_id')
# print(anime_rating.head())

anime_pivot = pd.pivot_table(index='user_id', columns='name', values='rating_y', data=anime_rating)

anime_pivot.fillna(value=0, inplace=True)

#print(anime_pivot.head())

from scipy.sparse import csr_matrix

anime_mat = csr_matrix(anime_pivot.values)

#print("peale maatriksi loomist")

from sklearn.neighbors import NearestNeighbors

anime_nbrs = NearestNeighbors(metric='cosine', algorithm='auto').fit(anime_mat)
distances, indices = anime_nbrs.kneighbors(anime_mat)

#print("peale sin-cos bullshitti")

anime_names = list(anime_pivot.index)

kimi_no_nawa_index = anime_names.index(user)
distances, indices = anime_nbrs.kneighbors(anime_pivot.iloc[kimi_no_nawa_index, :].values.reshape(1, -1),
                                           n_neighbors=10)
indices_flat, distances_flat = indices.flatten(), distances.flatten()

#print("enne lõpu for tsüklit")

tulemused = []
algTulemused = []

for index, anime_index in enumerate(indices_flat):
    anime_name = anime_names[anime_index]
    if (index == 0):
        print(f'Animes similar to {anime_name}:')
        algTulemused = rating[(rating['user_id'] == anime_name)]['anime_id'].tolist()
    else:
        print(f'\t {anime_name} with score ---> {distances_flat[index]}')
        tulemused.append(anime_name)

leidaparimanime(tulemused, algTulemused)
