import pandas as pd
import matplotlib.pyplot as plt
from word_db_creation import load_data

montreal = load_data()

montreal['name'] = montreal['name'].fillna('')
montreal['description'] = montreal['description'].fillna('')
montreal['search_text'] = (
    montreal['name'] + " " + montreal['description']
).str.lower()

word_of_interest = "bright" #change to whatever word we are looking for

montreal['has_word'] = montreal['search_text'].str.contains(rf'\b{word_of_interest}\b')
montreal_clean = montreal.dropna(subset=['review_scores_rating'])

has = montreal_clean[montreal_clean['has_word']]
has_not = montreal_clean[~montreal_clean['has_word']]

plt.figure()
plt.hist(has_not['review_scores_rating'], bins=30, alpha=0.25, color="purple", label='Does Not Have {word_of_interest}'.format(word_of_interest=word_of_interest))
plt.hist(has['review_scores_rating'], bins=30, alpha=0.9, color="pink", label='Has {word_of_interest}'.format(word_of_interest=word_of_interest))
plt.legend()
plt.show()

#not relevant:
#downtown, cozy, modern

#relevant:
#mtl? bright?

#overall, outliers in low ranking seems to be only listings without most common words. maybe investigate having a common keyword as a whole?(not specifics)

#TODO: run multiple linear regression on 5 most promising words?