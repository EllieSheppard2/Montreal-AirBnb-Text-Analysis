import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from collections import Counter
from sklearn.model_selection import train_test_split
from word_db_creation import load_data

# Load + clean
montreal = load_data()
montreal = montreal.dropna(subset=['review_scores_rating']).copy()
montreal['description'] = montreal['description'].fillna('').str.lower()

# Train/test split
train_df, test_df = train_test_split(
    montreal,
    test_size=0.2,
    random_state=42
)

# -------------------------------
# Histogram (optional, full data)
# -------------------------------
#   montreal['review_scores_rating'].plot(kind='hist', bins=50)
#   plt.xlabel("Rating")
#   plt.ylabel("# of Airbnb with Rating")
#   plt.title("Distribution of Airbnb Ratings")
#   plt.xticks(np.arange(0, 5, .125), rotation=45, fontsize=6)
#   plt.tight_layout()
#   plt.show()

# -------------------------------
# WORD DISCREPANCY (TRAIN ONLY)
# -------------------------------
montreal_clean = train_df

text = " ".join(montreal_clean['description'])
words = re.findall(r'\b[a-z]+\b', text)

word_counts = Counter(words)
candidate_words = [w for w, c in word_counts.items() if c >= 30]

results = []

for word in candidate_words:

    has_word = montreal_clean['description'].str.contains(rf'\b{word}\b')

    has = montreal_clean[has_word]
    has_not = montreal_clean[~has_word]

    if len(has) < 10 or len(has_not) < 10:
        continue

    mean_has = has['review_scores_rating'].mean()
    mean_not = has_not['review_scores_rating'].mean()

    diff = mean_has - mean_not

    results.append({
        'word': word,
        'mean_has': mean_has,
        'mean_not': mean_not,
        'diff': diff,
        'abs_diff': abs(diff),
        'count_has': len(has)
    })

results_df = pd.DataFrame(results)

top = results_df.sort_values('abs_diff', ascending=False).head(30)

print(top)
