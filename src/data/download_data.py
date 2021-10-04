# -*- coding: utf-8 -*-
# Import datasets in raw directory
import pandas as pd
import subprocess
from dotenv import load_dotenv
load_dotenv()

# Download fake news dataset from kaggle
subprocess.call(['kaggle', 'datasets', 'download',
                 '-d', 'astoeckl/fake-news-dataset-german',
                 '-p', './data/raw'])
                 
# Unzip dataset              
subprocess.call(['unzip', './data/raw/fake-news-dataset-german.zip',
                 '-d', './data/raw'])

#kaggle datasets download -d astoeckl/fake-news-dataset-german -p ./data/raw && unzip ./data/raw/fake-news-dataset-german.zip -d ./data/raw

# Download GermanFakeNC

subprocess.call(['wget', '-P', './data/raw',
                 'https://zenodo.org/record/3375714/files/GermanFakeNC.zip'])

# Unzip dataset
subprocess.call(['unzip', './data/raw/GermanFakeNC.zip',
                 '-d', './data/raw'])