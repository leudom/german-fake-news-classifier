# -*- coding: utf-8 -*-

"""FakeNewsClassifier Trainer

This script conduct the following steps (overview):

1. Load the processes dataset from {PROJECT_DIR}/data/processed as dataframe
2. Concatenate title and text in one column
3. Split the dataset into train and test

4. Set up a sklearn pipeline with preprocessor and classifier for the combined column (title+text)
   and perform hyperparam search 
5. Extract best score and best_params for and log it
6. Predict on testset and log the score

7. Pickle best pipe to disk (final model)

"""
# %%
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

import os
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import VotingClassifier
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, f1_score, recall_score, precision_score
from dotenv import find_dotenv, load_dotenv
import nltk
from nltk.stem.snowball import GermanStemmer
from sklearn.feature_extraction.text import CountVectorizer
from custom_transformers import StemmedCountVectorizer
import dagshub
from joblib import dump


load_dotenv(find_dotenv())
#%% Load and split dataset
INPUTFILE = os.path.join(os.getenv('PROJECT_DIR'), 'data', 'processed', 'fake_news_processed.csv')
df = pd.read_csv(INPUTFILE, sep=';')
logger.info('Distribution of fake news in entire dataset: \n%s' % df.fake.value_counts(normalize=True))

X = df['title']+' '+df['text']
y = df['fake']

X_train, X_test, y_train, y_test = train_test_split(X, y,
                    test_size=0.2,
                    stratify=y,
                    random_state=42)

# Download and init stopwordlist
nltk.download('stopwords')
STOPWORD_LIST = nltk.corpus.stopwords.words('german')

#print(X_train[100])

# %% Test with CountVectorizer
"""
count_vec = StemmedCountVectorizer(token_pattern=r'\b[a-zA-Z]{2,}\b',
                                max_features=100,
                                stop_words=STOPWORD_LIST,
                                lowercase=True,
                                stemmer=GermanStemmer(ignore_stopwords=True),
                                ngram_range=(2,2)
                        )

word_counts = count_vec.fit_transform(X_train).todense()

df_body = pd.DataFrame(word_counts, columns=count_vec.get_feature_names())
df_body_trans = pd.DataFrame(df_body.T.sum(axis=1), columns=['count'])
df_body_trans.sort_values(by='count', ascending=False).head(20)

"""

#%% Define param grid for tuning
param_grid = {'vectorizer__max_features':[500],
        'clf__n_estimators': [400],
        'clf__learning_rate': [0.8],
        'clf__max_depth': [5]}

# Constants for training
MODEL_PATH = os.path.join('bin', 'models', 'model.joblib')
CV_SCORING = 'f1'
CV_FOLDS = 3

# %%
with dagshub.dagshub_logger() as dagslog:
        # Pipeline
        pipe = Pipeline(steps=[
        ('vectorizer', StemmedCountVectorizer(stop_words=STOPWORD_LIST,
                                   token_pattern=r'\b[a-zA-Z]{2,}\b',
                                   stemmer=GermanStemmer(ignore_stopwords=True),
                                   lowercase=True)),
        ('clf', CatBoostClassifier())
        ])
        # pipe_title_tune.get_params().keys()
        logger.info('Start training estimator pipeline')
        cv_grid = GridSearchCV(pipe, param_grid, scoring=CV_SCORING, cv=CV_FOLDS, n_jobs=2)
        cv_grid.fit(X_train, y_train)
        #cv_grid.best_estimator_.named_steps['clf'].get_all_params()

        # Log and assign best score and params to var
        logger.info('Best params from GridSearchCV: %s' % str(cv_grid.best_params_))
        dagslog.log_hyperparams({'model_path': MODEL_PATH})
        dagslog.log_hyperparams({'cv_score': CV_SCORING})
        dagslog.log_hyperparams({'best_cv_params': cv_grid.best_params_})

        logger.info('Best %s from GridSearchCV: %s' % (CV_SCORING, str(cv_grid.best_score_)))
        dagslog.log_metrics({'best_cv_score': cv_grid.best_score_})
        
        # Predict on testdata
        y_pred = cv_grid.best_estimator_.predict(X_test)
        logger.info('f1_score for testdata: %s' % str(f1_score(y_test, y_pred)))
        dagslog.log_metrics({'f1_score_on_testdata': f1_score(y_test, y_pred)})
        logger.info('precision_score for testdata: %s' % str(precision_score(y_test, y_pred)))
        dagslog.log_metrics({'precision_score_on_testdata': precision_score(y_test, y_pred)})
        logger.info('recall_score for testdata: %s' % str(recall_score(y_test, y_pred)))
        dagslog.log_metrics({'recall_score_on_testdata': recall_score(y_test, y_pred)})
        logger.info('Classification report for testdata: \n%s' % classification_report(y_test, y_pred))
        logger.info('Confusion matrix for testdata: \n%s' % confusion_matrix(y_test, y_pred))

        # Dump model to disk
        dump(cv_grid.best_estimator_, MODEL_PATH)