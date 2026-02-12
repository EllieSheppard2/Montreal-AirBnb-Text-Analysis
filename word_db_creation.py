import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

montreal = pd.read_csv('listings.csv')
print(montreal.head(10))
montreal['review_scores_rating'].plot(kind='hist', bins = 50)
plt.xticks(np.arange(0, 5, .125), fontsize=3)
plt.show()
#choose "highly rated" threshold at 4.75
#TODO: create db of highly rated, and one of low rated listings, only include "word" cols

#TODO: created a dataframe of words in each column for both. words and counts
