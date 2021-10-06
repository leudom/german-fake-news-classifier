# -*- coding: utf-8 -*-
# %%
import logging
import os
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

import nltk
#%%
INPUTFILE = os.path.join(os.getenv('PROJECT_DIR'), 'data', 'processed', 'fake_news_processed.csv')

df = pd.read_csv(INPUTFILE, sep=';')
# %%
df.fake.value_counts(normalize=True)
#%%
X = df['title']
y = df['fake']
#%%
X_train, X_test, y_train, y_test = train_test_split(X, y,
                    test_size=0.2,
                    stratify=y,
                    random_state=42)

#%%
train_pool = Pool(X_train, y_train,
                  text_features=['text', 'title'],
                  feature_names=list(X_train)
                  )
valid_pool = Pool(X_test, y_test,
                  text_features=['text', 'title'],
                  feature_names=list(X_train)
                  )
# %%
cbc = CatBoostClassifier(iterations=100,
        learning_rate=0.8,
        eval_metric='Precision',
        use_best_model=True)
# %%
cbc.fit(train_pool, eval_set=valid_pool)


# %% Sklearn preprocessing with nltk, CountVectorizer
nltk.download('stopwords')
stopword_list = nltk.corpus.stopwords.words('german')
stemmer = nltk.stem.snowball.GermanStemmer(ignore_stopwords=True)

# %%
class StemmedCountVectorizer(CountVectorizer):
    def __init__(self, stemmer, **kwargs):
        super(StemmedCountVectorizer, self).__init__(**kwargs)
        self.stemmer = stemmer

    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (self.stemmer.stem(w) for w in analyzer(doc))
#%%
StemmedCountVectorizer(stemmer)
# %%
count_vec_body = CountVectorizer(token_pattern=r'\b[a-zA-Z]{2,}\b',
                                  max_features=100)
                                  #ngram_range=(2,2)
                                #)

count_vec_body.fit(X_train)
word_counts_in_body = count_vec_body.transform(X_train).todense()
# %%
df_body = pd.DataFrame(word_counts_in_body, columns=count_vec_body.get_feature_names())
df_body_trans = pd.DataFrame(df_body.T.sum(axis=1), columns=['count'])
df_body_trans.sort_values(by='count', ascending=False).head(20)
# %%
pipe = Pipeline(steps=[
        ('vectorizer', StemmedCountVectorizer(stop_words=stopword_list,
                                  token_pattern=r'\b[a-zA-Z]{2,}\b',
                                  max_features=300,
                                  stemmer=stemmer)),
        ('clf', CatBoostClassifier(iterations=100,
                                learning_rate=0.1))
])

# %%

pipe.fit(X_train, y_train)
# %%
pred = pipe.predict(X_test)
# %%
print(classification_report(y_test, pred))
# %%
