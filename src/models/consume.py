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
text = """ Die Nachricht ist knapp - und sie kommt überraschend: Queen Elizabeth II. werde sich auf medizinischen Rat hin die nächsten Tage ausruhen und nicht wie geplant nach Nordirland reisen, teilte der Buckingham-Palast Mittwoch mit. "Widerwillig" habe die 95-jährige Königin den Rat ihrer Ärzte angenommen - sie sei enttäuscht, ihre geplanten Termine nicht wahrnehmen zu kennen. Die Entscheidung habe nichts mit Corona zu tun, hieß es laut der Nachrichtenagentur PA aus Palastkreisen.

Die Nachricht kam an einem Tag, an dem die Queen verschiedenste Titelseiten damit zierte, wie sie ungewohnt keck ihre Gesundheit betont. Mit einer unkonventionellen Antwort schlug die Königin die "Oldie of the Year"-Auszeichnung aus, die ihr das Seniorenmagazin The Oldie verleihen wollte. "Ihre Majestät glaubt, man ist so alt, wie man sich fühlt", schrieb der Privatsekretär der 95-Jährigen, Tom Laing-Baker, in einer schriftlichen Absage, die in der November-Ausgabe der Zeitschrift veröffentlicht wurde. "Daher ist die Queen der Meinung, dass sie nicht die relevanten Kriterien erfüllt, um die Auszeichnung zu akzeptieren, und hofft, dass sich ein geeigneterer Kandidat findet." Die Zeitschrift feierte die Antwort als "höflichste Absage der Geschichte", der britische Boulevard jubelte. Die Monarchin, so schien es, wollte ihrem Volk versichern, dass es sich keine Sorgen machen müsse. Doch diese dürften nun umso stärker werden."""

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
