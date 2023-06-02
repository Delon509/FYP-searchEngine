import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score,f1_score , classification_report
from sklearn.model_selection import GridSearchCV
import pickle
from nltk.stem.snowball import SnowballStemmer
import re
def normalize_text(s):
    s = s.lower()

    # remove punctuation that is not word-internal (e.g., hyphens, apostrophes)
    s = re.sub('\s\W',' ',s)
    s = re.sub('\W\s',' ',s)

    # make sure we didn't introduce any double spaces
    s = re.sub('\s+',' ',s)

    return s

listofStopword = [
'a', 'about', 'above', 'above', 'across', 'after', 'afterwards', 'again',
'against', 'all', 'almost', 'alone', 'along', 'already', 'also','although',
'always','am','among', 'amongst', 'amoungst', 'amount',  'an', 'and', 'another',
'any','anyhow','anyone','anything','anyway', 'anywhere', 'are', 'around', 'as',
'at', 'back','be','became', 'because','become','becomes', 'becoming', 'been',
'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides',
'between', 'beyond', 'bill', 'both', 'bottom','but', 'by', 'call', 'can',
'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de', 'describe',
'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight',
'either', 'eleven','else', 'elsewhere', 'empty', 'enough', 'etc', 'even',
'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few',
'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former',
'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get',
'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here',
'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him',
'himself', 'his',  'however', 'hundred', 'ie', 'if', 'in', 'inc',
'indeed', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last',
'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me',
'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly',
'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never',
'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not',
'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only',
'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out',
'over', 'own','part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same',
'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she',
'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some',
'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere',
'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their',
'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby',
'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third',
'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus',
'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two',
'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well',
'were',  'whatever',  'whence', 'whenever',  'whereafter',
'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which',
'while', 'whither',  'whoever', 'whole', 'whom', 'whose',  'will',
'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself',
'yourselves', 'the']

if __name__ == "__main__":
    stemmer = SnowballStemmer("english")
    all_df = pd.read_csv('questions_vs_statements_v1.0.csv')
    df_statement = all_df[all_df['label']=='statement']
    df_statement_downsampled = df_statement.sample(60000)
    df_question = all_df[all_df['label'] == 'question']
    df_question_downsampled = df_question.sample(60000)
    df = pd.concat([df_question_downsampled,df_statement_downsampled])
    df['doc'] = [normalize_text(s) for s in df['doc']]
    df['doc'] = df['doc'].str.split(" ")
    df['doc'] = df['doc'].apply(lambda x: [stemmer.stem(y) for y in x])
    df['doc'] = df['doc'].str.join(" ")

    X_train, X_test, y_train, y_test = train_test_split(df['doc'], df['target'], random_state=42)
    vectorizer = CountVectorizer(strip_accents='ascii', token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b', lowercase=True,
                                 stop_words=listofStopword)
    X_train_cv = vectorizer.fit_transform(X_train)
    X_test_cv = vectorizer.transform(X_test)
    Word_frequency = pd.DataFrame(X_train_cv.toarray(), columns=vectorizer.get_feature_names() )
    top_words = pd.DataFrame(Word_frequency.sum()).sort_values(0, ascending=False )
    print(Word_frequency, '\n')
    print(top_words)
    naive_bayes = MultinomialNB(alpha=700)
    naive_bayes.fit(X_train_cv, y_train)
    predictions = naive_bayes.predict(X_test_cv)

    query = pd.DataFrame({'doc': [
                        "I go to school by bus."
                        ]
                   })
    query['doc'] = [normalize_text(s) for s in query['doc']]
    query['doc'] = query['doc'].str.split(" ")
    query['doc'] = query['doc'].apply(lambda x: [stemmer.stem(y) for y in x])
    query['doc'] = query['doc'].str.join(" ")
    print(X_test)
    print(query)
    print(naive_bayes.predict(vectorizer.transform(query['doc'])))
    print(naive_bayes.predict_proba(vectorizer.transform(query['doc'])))
    query2 = pd.DataFrame({'doc': [
        "what are you doing?"
    ]
    })
    query2['doc'] = query2['doc'].str.split(" ")
    query2['doc'] = query2['doc'].apply(lambda x: [stemmer.stem(y) for y in x])
    query2['doc'] = query2['doc'].str.join(" ")
    print(query2)
    print(naive_bayes.predict(vectorizer.transform(query2['doc'])))
    print(naive_bayes.predict_proba(vectorizer.transform(query2['doc'])))
    #print(naive_bayes.predict(query))
    print('Accuracy score for  model is: ', accuracy_score(y_test, predictions), '\n')
    print('Precision score for  model is: ', precision_score(y_test, predictions), '\n')
    print('Recall score for  model is: ', recall_score(y_test, predictions), '\n')
    print('F1 score for  model is: ', f1_score(y_test, predictions), '\n')
    print(classification_report(y_test, predictions))
    param = {'alpha': [100]}

    grid = GridSearchCV(MultinomialNB(), param, scoring='roc_auc', cv=10, return_train_score=True,verbose=10)
    grid.fit(X_train_cv, y_train)
    print(grid.best_params_)
    grid_predictions = grid.predict(X_test_cv)
    print(classification_report(y_test, grid_predictions))
    with open("finalized_model.pkl", 'wb') as fout:
        pickle.dump((vectorizer, naive_bayes), fout)



