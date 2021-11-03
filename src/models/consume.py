# -*- coding: utf-8 -*-

"""FakeNewsClassifier - Consume endpoint

Script to consume endpoint

"""
# %%
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

import os
import requests
import json
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# %%
with open ('/Users/dominikl/Desktop/greta_heute.txt', 'r') as file:
    text = file.read().replace('\n', ' ')

print(text)
# %%
endpoint_url = 'http://698e25a3-0344-4883-8b19-d67fa4aeb89f.westeurope.azurecontainer.io/score'
payload = {'data': [text]}
headers = {'Content-Type':'appliction/json'}
r = requests.post(url=endpoint_url,
                  data=(json.dumps(payload)),
                  headers=headers)
logging.info(r.status_code)
logging.info(r.json())
# %%
