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

anime = pd.read_csv('../data/rating.csv')


k = anime['user_id'] == 3624

l =  anime['rating'] != -1

r = anime[k & l]

print(r)

'''k = anime['user_id'] == 7
r = r['anime_id'].tolist()
l = anime[anime['anime_id'] == 15451 & anime['user_id'] == 69976] 

print(l)

print(anime(k & l))
anime
#kimi no na wa 32281 10, a silent voice 28851 8, the garden of words 16782 7, spirited away 199 10, 5 centimeters per second 1689 10, '''
