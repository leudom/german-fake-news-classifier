# -*- coding: utf-8 -*-

"""FakeNewsClassifier Scoring Script (Entry Point)
This script serves as an entry point to ACI Deployment

"""
# %% Imports
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

import os
import json
import numpy as np
from joblib import load
from azureml.core.model import Model
#%%
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

#MODEL_PATH = os.path.join(os.getenv('PROJECT_DIR'), 'bin', 'models', 'model.pkl')
#model = load(MODEL_PATH)
#type(model)
#X = ["Das ist ein Test, ob dieser Text als Fake News klassifiziert wird", "Ein weiterer Test"]
#results = model.predict_proba(X)
#results.tolist()
# %% Define entry point
def init():
    global model
    model_path = Model.get_model_path(os.getenv('MODEL_NAME'))
    logging.info('Model path is %s' % str(model_path))
    model = load(model_path)
    logging.info('Model successfully loaded')

def run(data):
    try:
        data = json.loads(data)
        result = model.predict_proba(data['data'])
        return {'data': result.tolist(), 'message': "Successfully classified news"}
    except Exception as e:
        error = str(e)
        return {'data': error, 'message': "Failed to classify news"}
