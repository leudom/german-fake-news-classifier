# -*- coding: utf-8 -*-

"""FakeNewsClassifier Deployment Script



"""
# %% Imports
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

import pandas as pd
import numpy as np
from joblib import load

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())