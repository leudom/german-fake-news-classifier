# -*- coding: utf-8 -*-

"""FakeNewsClassifier Deployment Script



"""
# %% Imports
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

import os
import pandas as pd
import numpy as np
from joblib import load

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv(os.getenv('PROJECT_DIR')))

# %%
MODEL_PATH = os.path.join(os.getenv('PROJECT_DIR'), 'bin', 'models', 'model.pkl')
model = load(MODEL_PATH)
type(model)
# %%
X = ["Das ist ein Test, ob dieser Text als Fake News klassifiziert wird", "Ein weiterer Test"]
model.predict_proba(X)
# %%
