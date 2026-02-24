import pandas as pd
import matplotlib.pyplot as plt
from word_db_creation import load_data

montreal = load_data()

montreal['name'] = montreal['name'].fillna('')
montreal['description'] = montreal['description'].fillna('')
montreal['search_text'] = (
    montreal['name'] + " " + montreal['description']
).str.lower()

montreal['has_downtown'] = montreal['search_text'].str.contains(r'\bdowntown\b')
montreal_clean = montreal.dropna(subset=['review_scores_rating'])

downtown = montreal_clean[montreal_clean['has_downtown']]
non_downtown = montreal_clean[~montreal_clean['has_downtown']]

plt.figure()
plt.hist(downtown['review_scores_rating'], bins=30, alpha=0.6, label='Downtown')
plt.hist(non_downtown['review_scores_rating'], bins=30, alpha=0.6, label='No Downtown')
plt.show()

#downtown seems to not be relevant. can copy and paste this with other key words
#TODO: copy and paste this, but obviously modify for other key words. if distribution looks different then add labels o see wich is whic.