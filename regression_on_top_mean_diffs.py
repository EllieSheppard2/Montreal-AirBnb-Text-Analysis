import statsmodels.api as sm
from word_db_creation import load_data

montreal = load_data()

montreal = montreal.dropna(subset=['review_scores_rating']).copy()
montreal['description'] = montreal['description'].fillna('').str.lower()

words_to_use = ['value', 'hostel', 'establishment', 'onsite', 'tourists']

for word in words_to_use:
    montreal[f'has_{word}'] = montreal['description'].str.contains(rf'\b{word}\b').astype(int)

X = montreal[[f'has_{word}' for word in words_to_use]]
X = sm.add_constant(X)
y = montreal['review_scores_rating']
model = sm.OLS(y, X).fit()
print(model.summary())

#may consider adding more words to this model? establishment becomes non significant