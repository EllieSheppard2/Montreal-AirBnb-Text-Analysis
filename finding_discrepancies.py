import pandas as pd
import matplotlib.pyplot as plt
from word_db_creation import load_data
import re
from collections import Counter

montreal = load_data()

montreal['name'] = montreal['name'].fillna('')
montreal['description'] = montreal['description'].fillna('')
montreal['search_text'] = (
    montreal['name'] + " " + montreal['description']
).str.lower()

word_of_interest = ("fully") #change to whatever word we are looking for

montreal['has_word'] = montreal['search_text'].str.contains(rf'\b{word_of_interest}\b')
montreal_clean = montreal.dropna(subset=['review_scores_rating'])

has = montreal_clean[montreal_clean['has_word']]
has_not = montreal_clean[~montreal_clean['has_word']]

plt.figure()
plt.hist(has_not['review_scores_rating'], bins=30, alpha=0.25, color="purple", label='Does Not Have {word_of_interest}'.format(word_of_interest=word_of_interest))
plt.hist(has['review_scores_rating'], bins=30, alpha=0.9, color="pink", label='Has {word_of_interest}'.format(word_of_interest=word_of_interest))
plt.legend()
#plt.show()

#Just from looking at some suspect words graphs,

#not relevant:
#downtown, cozy, modern, heart

#relevant:
#mtl? bright? luxury

#overall, outliers in low ranking seems to be only listings without most common words. maybe investigate having a common keyword as a whole?(not specifics)

#Find the top five words with the biggest difference in rating of listings that have them in description and those that do not
text = " ".join(montreal_clean['description'])

words = re.findall(r'\b[a-z]+\b', text)
word_counts = Counter(words)
candidate_words = [w for w, c in word_counts.items() if c >= 30]

results = []

#This part takes a LONG time to run. To note: making len has/has not and candidate word count too high will give words with
#virtually no difference in rating as it will just return words in almost all listings. However, too low and it will take even longer to run.
#Also, running with len has/has not as 1 and candidate words as 2 yields results where single listings with low ratings get factored in.
#Ideal seems to be len as 10, candidate as 30.
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

top = results_df.sort_values('abs_diff', ascending=False).head(10)

print(top)

#Pasting output as it takes long to run
#               word  mean_has  mean_not      diff  abs_diff  count_has
#931           value  4.418710  4.724992 -0.306282  0.306282         31
#1040         hostel  4.440339  4.725956 -0.285617  0.285617         59
#1041  establishment  4.456364  4.724909 -0.268546  0.268546         33
#1068         onsite  4.989688  4.721500  0.268187  0.268187         64
#304        tourists  4.462250  4.725126 -0.262876  0.262876         40
#729          resort  4.983676  4.721413  0.262264  0.262264         68
#946     kitchenette  4.468611  4.727409 -0.258798  0.258798        108
#624            step  4.478286  4.724879 -0.246593  0.246593         35 is this one good? step could be as in one "step" from downtown, or could just be a filler word
#993         doorman  4.967465  4.721461  0.246004  0.246004         71
#866              st  4.484054  4.724916 -0.240862  0.240862         37 this one is stupid