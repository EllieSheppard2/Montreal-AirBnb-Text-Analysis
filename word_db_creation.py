import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from collections import Counter

montreal = pd.read_csv('listings.csv')
#print(montreal.head(10))
montreal['review_scores_rating'].plot(kind='hist', bins = 50)
plt.xticks(np.arange(0, 5, .125), fontsize=3)
#plt.show()
#choose "highly rated" threshold at 4.75

montreal_clean = montreal.dropna(subset=['review_scores_rating'])

high_rated = montreal_clean[
    montreal_clean['review_scores_rating'] >= 4.75
].copy()

high_rated['name'] = high_rated['name'].fillna('')
high_rated['description'] = high_rated['description'].fillna('')

def get_word_counts(series):
    text = ' '.join(series.astype(str)).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()

    #filler words (not relevant) add more as i look through what comes up
    fillers = {
        'the', 'and', 'a', 'to', 'of', 'in', 'for', 'is', 'on', 'with', 'this', 'that',
        'it', 'as', 'at', 'an', 'be', 'are', 'from', 'by', 'or', 'your', 'you',
        'our', 'we', 'has', 'have', 'will', 'can', 'all', 'more', 'also', 'montreal', 'montral', 'bed'
    }

    filtered = [w for w in words if w not in fillers and len(w) > 2]

    return Counter(filtered)

name_counts = get_word_counts(high_rated['name'])

name_df = pd.DataFrame(
    name_counts.most_common(30),
    columns=['word', 'count']
)

print("Most common words in name of listing")
print(name_df)

description_counts = get_word_counts(high_rated['description'])

description_df = pd.DataFrame(
    description_counts.most_common(30),
    columns=['word', 'count']
)

print("\nMost common words in description of listing")
print(description_df)