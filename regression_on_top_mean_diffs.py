import statsmodels.api as sm
from word_db_creation import load_data

montreal = load_data()

montreal = montreal.dropna(subset=['review_scores_rating']).copy()
montreal['description'] = montreal['description'].fillna('').str.lower()

words_to_use = ['value', 'hostel', 'tourists', 'kitchenette', 'university',
                'student', 'enclave', 'hospitals']

for word in words_to_use:
    montreal[f'has_{word}'] = montreal['description'].str.contains(rf'\b{word}\b').astype(int)

X = montreal[[f'has_{word}' for word in words_to_use]]
X = sm.add_constant(X)
y = montreal['review_scores_rating']
model = sm.OLS(y, X).fit()
print(model.summary())

#added resort, kitchenette, doorman to value, hostel, establishment, onsite, tourists. now onsite is insignificant as well as kitchenette, doorman, establishment, resort

#re-running without those. other variables stay significant

#so, hostel value and tourist key words in description have significance in rating. however, they only explain 0.008 of the variation in scores.

#actually going with printing top 30 out of find_discrepancies, then doing regression with those that have gaps above .20 and look resonable, ie. don't include "st"

#now, remove non-significant at 0.05 level

#final model: value, hostel, tourists, kitchenette, univeristy, student, enclave, hospitals