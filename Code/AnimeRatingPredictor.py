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

anime = pd.read_csv('../data/anime.csv')

#The genre value is stored as a String which means we have to
#revalue every value as a list where each item is a genre type the anime has
anime['genre'] = anime['genre'].str.replace(" ", "")
anime['genre'] = anime['genre'].str.split(",")
anime = anime.dropna() #Data cleaning

test = set(itertools.chain.from_iterable(anime.genre))
print(test)
print(pd.get_dummies(pd.DataFrame(anime.genre)).head())

print(anime.type.head())
data = pd.DataFrame(anime.type)
data = pd.get_dummies(data)
print(data.head(5))

anime = anime[['episodes', 'members', 'rating']]

anime = anime.join(data)

print(anime.head(5))

#Data cleaning
anime = anime.drop(anime[anime.episodes == "Unknown"].index)
anime = clean_dataset(anime)


X_train, X_test, y_train, y_test = train_test_split(anime.loc[:, anime.columns != 'rating'], anime['rating'], test_size=0.3, random_state=1)


reg = LinearRegression().fit(X_train, y_train)

reg2 = reg.predict(X_test)

print(MSE(y_test.array, reg2))

r = reg.predict([[949.0, 504862.0, 0, 0, 0, 0, 0, 1]])
r = reg.predict([[12.0, 140604.0, 0, 0, 0, 0, 0, 1]])

print(r)
