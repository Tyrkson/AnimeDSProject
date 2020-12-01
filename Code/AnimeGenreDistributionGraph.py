import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import itertools

anime = pd.read_csv('../data/anime.csv')


anime['genre'] = anime['genre'].str.replace(" ", "")
anime['genre'] = anime['genre'].str.split(",")
anime = anime.dropna()
print(anime['genre'].head(5))
test = set(itertools.chain.from_iterable(anime.genre))
print(len(test))

for i in anime.genre:
	if type(i) is not list:
		print(i)
