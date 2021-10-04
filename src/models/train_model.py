# -*- coding: utf-8 -*-
# %%
from locale import normalize
import logging
import os
import pandas as pd
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import train_test_split
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
#%%
INPUTFILE = os.path.join(os.getenv('PROJECT_DIR'), 'data', 'processed', 'fake_news_processed.csv')

df = pd.read_csv(INPUTFILE, sep=';')
# %%
df.fake.value_counts(normalize=True)
#%%
X = df[['text', 'title']]
y = df[['fake']]
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
cbc = CatBoostClassifier(iterations=100, learning_rate=1, eval_metric=['Recall', 'Precision'])
# %%
cbc.fit(train_pool, eval_set=valid_pool)
# %%
