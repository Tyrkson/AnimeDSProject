import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import itertools

anime = pd.read_csv('../data/anime.csv')


#The genre value is stored as a String which means we have to
#revalue every value as a list where each item is a genre type the anime has
anime['genre'] = anime['genre'].str.replace(" ", "")
anime['genre'] = anime['genre'].str.split(",")
anime = anime.dropna() #Data cleaning

#Here we store the count of animes for every genre
genreCounts = {}

#Filling genreCounts
for i in anime.genre:
	for y in i:
		if y in genreCounts:
			genreCounts[y] += 1
		else:
			genreCounts[y] = 1 
		

#Sorting dictionary and getting a list of tuples
genreCounts = sorted(genreCounts.items(), key=lambda item: item[1])

#Creating the horizontal bar plot
fig, ax = plt.subplots()

genres = []
counts = []

#One liners to get the genre and count data separately
[genres.append(i[0]) for i in genreCounts]
[counts.append(i[1]) for i in genreCounts]

y_pos = np.arange(len(genres))
performance = 5 + 11 * np.random.rand(len(genres))



ax.barh(y_pos, counts, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(genres)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Genre Count')
ax.set_title("Genres popularity")

plt.show()
