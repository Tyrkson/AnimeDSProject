import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import math
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import itertools


def MSE(y_target, y_pred):
    a = 0
    for i in range(0, len(y_target)):
        a +=(y_target[i] - y_pred[i])**2
    return a/len(y_target)
    
#https://stackoverflow.com/a/46581125
def clean_dataset(df):
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep].astype(np.float64)

#This method helps to convert user input (anime genres) into a list of 0's and 1's
#where 1 means anime has this genre and 0 means it hasn't
def genresToBinaryForm(genres, template):
    bGenres = []

    for i in template:
        if i in genres:
            bGenres.append(1)
        else:
            bGenres.append(0)

    return bGenres

anime = pd.read_csv('../data/anime.csv')
anime = anime.drop(anime[anime['genre'] == 'hentai'].index)

#The genre value is stored as a String which means we have to
#revalue every value as a list where each item is a genre type the anime has
anime['genre'] = anime['genre'].str.replace(" ", "")
anime['genre'] = anime['genre'].str.split(",")
anime = anime.dropna() #Data cleaning

genres = set(itertools.chain.from_iterable(anime.genre))

#I store every anime genre values as 1 and 0 in this list separated by genre 
#And then later I create a dataframe of it to place the original genre columns because prediction algorithm doesn't know how to distinguish lists and strings
animeGenresInNumerical = []

for i, r in anime.iterrows():
	genreNumeric = []
	for g in genres:
		if g in r['genre']:
			genreNumeric.append(1)
		else:
			genreNumeric.append(0)	
	animeGenresInNumerical.append(genreNumeric)

genreDataFrame = pd.DataFrame(animeGenresInNumerical, columns=genres)
#print(genreDataFrame.head(5))
#print(anime.genre.head(5))

#print(anime.type.head())
data = pd.DataFrame(anime.type)
data = pd.get_dummies(data)
#print(data.head(5))

anime = anime[['episodes', 'members', 'rating']]

anime = anime.join(data)
anime = anime.join(genreDataFrame)

#print(anime.head(5))

#Data cleaning
anime = anime.drop(anime[anime.episodes == "Unknown"].index)
anime = clean_dataset(anime)


X_train, X_test, y_train, y_test = train_test_split(anime.loc[:, anime.columns != 'rating'], anime['rating'], test_size=0.3, random_state=1)


reg = LinearRegression().fit(X_train, y_train)


reg2 = reg.predict(X_test)

print(MSE(y_test.array, reg2))


print(anime.columns.tolist())
print()
toPredictAnimeGenres = genresToBinaryForm(['Shoujo', 'Comdey', 'Drana', 'Romance'], genreDataFrame.columns.tolist())

#Episodes, Members, Movie, ONA, OVA, Special, TV
toPredictAnime = [25.0,  212687.0, 0, 0, 0, 0, 0, 1]
toPredictAnime.extend(toPredictAnimeGenres)
r = reg.predict([toPredictAnime])

print(r)
