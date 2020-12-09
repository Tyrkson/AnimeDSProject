import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import math
import itertools

anime = pd.read_csv('../data/anime.csv')
ratings = pd.read_csv('../data/rating.csv')


ratings = ratings.drop(ratings[ratings.rating == -1].index)

meanRating = ratings.drop(columns=['anime_id'])
meanRating = meanRating.groupby(['user_id']).mean()
meanRating = meanRating.drop(meanRating[meanRating.rating > 5].index)
meanRating = meanRating.sort_values(by=['rating'], ascending=True)

#After doing all that filtering we see that there's only 197 users with these conditions
#Therefore I use them all to find the most liked anime based on their average rating and how many of them watched it

#We do it by setting some passing conditions
#If the critical user rated the anime above 7.0 then this anime goes into the good animes list
#and then later we find out how many critical users rated above 7.0 and based on that we list those animes where the first one has the highest amounts of ratings above 7.0 by the critical users

#Putting user ids into a list
criticalUsers = meanRating.index.tolist()

animeDict = {}

for i in criticalUsers:
	result = ratings[(ratings['user_id'] == i) & (ratings['rating'] >= 7.0)]['anime_id'].tolist()
	if len(result) > 0:
		for y in result:
			if y in animeDict:
				animeDict[y] += 1
			else:
				animeDict[y] = 1
				
#Sorting dictionary and getting a list of tuples
animeCounts = sorted(animeDict.items(), key=lambda item: item[1], reverse=True)
				
'''for i in range(len(animeCounts)):
	if i > 10:
		break
	print(anime[anime['anime_id'] == animeCounts[i][0]][['name', 'rating']].to_string(index=False))'''
	
animeIds = []

for i in range(len(animeCounts)):
	if i > 10:
		break
	animeIds.append(animeCounts[i][0])

r = anime[anime['anime_id'].isin(animeIds)][['name','rating']]
print(r)
