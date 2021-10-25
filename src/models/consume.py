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
text = """Die Liste türkiser Persönlichkeiten, die in Korruptionsermittlungen beschuldigt werden, ist lang: Da wären Altkanzler Sebastian Kurz, seine Berater Gerald Fleischmann und Stefan Steiner; Finanzminister Gernot Blümel, seine Vorgänger Hartwig Löger und Josef Pröll; Kabinettschefs wie Bernhard Bonelli und Clemens-Wolfgang Niedrist; Ex-Vizeparteiobfrau Bettina Glatz-Kremsner, der frühere Öbag-Chef Thomas Schmid und die Abgeordnete Michaela Steinacker – für alle Genannten gilt die Unschuldsvermutung. Auch die ÖVP selbst ist Beschuldigte gemäß Verbandsverantwortlichkeitsgesetz.



EUROPAS ZUKUNFT

In die Zukunft Europas reinhören
Das Verbindungsbüro des Europäischen Parlaments in Österreich informiert in einem Podcast über zukunftsweisende Themen und aktuelle Debatten. ''Thema Zukunft Europa'' erscheint vierteljährlich und lässt Abgeordnete, Experten und Bürger zu Wort kommen.

WERBUNG
Als Verteidigungsstrategie gegen die Ermittlungen der Wirtschafts- und Korruptionsstaatsanwaltschaft (WKStA) versuchen Türkise, immer wieder Nadelstiche zu setzen, um das Vertrauen in die Arbeit der Behörden zu unterminieren. Das erfolgt teils durch diskussionswürdige Kritik, teils durch Unwahrheiten. Dieses Wochenende war es wieder so weit: Aufgewärmt wurde eine alte Geschichte, die sich mit dem Privatleben des fallführenden Staatsanwalts Gregor Adamovic beschäftigt. Die ÖVP stößt sich daran, dass dieser mit jener Wirtschaftsexpertin liiert ist, die für die WKStA Chats aus sichergestellten Smartphones auswertet.

"Fragwürdige Vorgänge"
Der ÖVP-Abgeordnete Wolfgang Gerstl, einst Fraktionsführer im Ibiza-Ausschuss, sieht hier "fragwürdige Vorgänge", weil angeblich Compliance-Regeln in der Justiz verletzt würden. In den Richtlinien dazu heißt es, dass sich Justizbedienstete nicht von "familiären" oder "emotionalen" Interessen leiten lassen dürfen. Damit ist freilich etwas anderes gemeint: zum Beispiel, dass ein Staatsanwalt nicht mit Beschuldigten oder Opfern in seinem Verfahren befreundet sein sollte.


Um in der Beziehung zwischen beigezogener Expertin und fallführendem Staatsanwalt einen Verstoß gegen die Compliance-Richtlinie zu sehen, müsste zweierlei zutreffen: erstens, dass der Staatsanwalt gegen die ÖVP voreingenommen ist und deshalb belastende Inhalte sucht. Zweitens, dass die Wirtschaftsexpertin die Auswahl der Chats manipuliert, um ihrem Partner dabei zu helfen. Die Angelegenheit wurde nach einer anonymen Anzeige, die offenbar aus ÖVP-affinen Justizkreisen stammte, bereits geprüft – und die Zusammenarbeit für unbedenklich erklärt. Abgesehen davon arbeiten an der Causa weit mehr Personen mit: Für die Chatauswertung ist prinzipiell Oberstaatsanwalt Matthias Purkart verantwortlich; geprüft werden die Ergebnisse dann noch von Gruppenleiter und WKStA-Spitze."""

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
