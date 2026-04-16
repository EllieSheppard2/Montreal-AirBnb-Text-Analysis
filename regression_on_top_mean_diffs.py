import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
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

# Final selected words (from TRAIN analysis)
words_to_use = [
    'kitchenette', 'hostel', 'simple',
    'budget'
]
#selected 'kitchenette', 'resort', 'doorman', 'hostel', 'simple', 'homey', 'budget', 'jacuzzi'
#from training set of largest discrencies that logically make sense to cause rating difference.
#dropped resort, doorman, homey, jacuzzi for non-significance.
# Create features
for word in words_to_use:
    train_df[f'has_{word}'] = train_df['description'].str.contains(rf'\b{word}\b').astype(int)
    test_df[f'has_{word}'] = test_df['description'].str.contains(rf'\b{word}\b').astype(int)

# -----------------------
# TRAIN MODEL
# -----------------------
X_train = train_df[[f'has_{word}' for word in words_to_use]]
X_train = sm.add_constant(X_train)
y_train = train_df['review_scores_rating']

model = sm.OLS(y_train, X_train).fit()
print(model.summary())

X_test = test_df[[f'has_{word}' for word in words_to_use]]
X_test = sm.add_constant(X_test)
y_test = test_df['review_scores_rating']

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nTest Performance:")
print("MSE:", mse)
print("R^2:", r2)