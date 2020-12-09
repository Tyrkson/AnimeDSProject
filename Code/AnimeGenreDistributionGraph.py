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

fig = plt.figure(figsize=(12,6))

ax = fig.add_axes([0.13, 0.1, 0.8, 0.8])

genres = []
counts = []

#One liners to get the genre and count data separately
[genres.append(i[0]) for i in genreCounts]
[counts.append(i[1]) for i in genreCounts]

y_pos = np.arange(len(genres))

#We used this color for our plot to present it on poster
baseColor = "white"

#to inspect plot from the program output uncomment the following line
#baseColor = 'black'

ax.barh(y_pos, counts, align='center', color="yellow")
ax.set_yticks(y_pos)
ax.set_yticklabels(genres)
ax.spines['left'].set_color(baseColor)
ax.spines['right'].set_color(baseColor)
ax.spines['top'].set_color(baseColor)
ax.spines['bottom'].set_color(baseColor)
ax.tick_params(axis='y', colors=baseColor)
ax.tick_params(axis='x', colors=baseColor)
ax.get_children()[5].set_color([50/255, 168/255, 82/255])

ax.invert_yaxis()  # labels read top-to-bottom
#ax.set_xlabel('Genre Count')
#ax.set_title("Genres popularity")

plt.show()

#plt.savefig('plot.png', transparent=True, dpi=550)
