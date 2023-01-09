

import json
import os
import requests
import sys
import pydash as pydash
import csv

# Get life years of an author using finto json-ld api

base = "https://finto.fi/rest/v1/finaf/data?uri=http%3A%2F%2Furn.fi%2FURN%3ANBN%3Afi%3Aau%3Afinaf%3A" #000085932 
suffix = "&format=application/ld%2Bjson"


# 
counter = 0


with open('astericodes.txt', 'r') as f:
  reader = csv.DictReader(f)
  for row in reader:

    sample = row['ASTERI_ID']

    authurn = base + sample.split(")")[-1] + suffix

    #print("Authurn", authurn)
    #print("\n")

    response = requests.get(authurn)

    # if asteri code is erroneos go to next line.
    if response.status_code == 404:
        print("Notfound;0000;9999;Notfound;{0}".format(sample))
        continue

    json_data = response.json()

    ##print("RAW:\n", json_data)

    dataindex = -1
    if ('http://rdaregistry.info/Elements/a/P50120' in json_data['graph'][-1]) :
        dataindex = -1
    else:
        dataindex = -2

    ##print("Dataindex:", dataindex)


    birthyear= json_data['graph'][dataindex].get('http://rdaregistry.info/Elements/a/P50121',None)
    deathyear= json_data['graph'][dataindex].get('http://rdaregistry.info/Elements/a/P50120',None)


    # ['http://rdaregistry.info/Elements/a/P50428'] -- henkilön toinen identiteetti
    alias = pydash.get(json_data['graph'][-1],"prefLabel.value", "None")   #['prefLabel']['value']
    ##print("Alias: ", alias)

    # http://rdaregistry.info/Elements/a/P50411 - käytettävä nimenmuoto
    authname = pydash.get(json_data['graph'][dataindex], 'prefLabel.value', "None")
    ##print("Authname : ", authname)
    if authname is None:
        authname= "ORIG:" + row['KUVAUS']

    print("{0};{1};{2};{3};{4};{5}".format(authname, birthyear, deathyear, alias,sample, authurn))

    counter += 1

    #if counter >=30:
    #    sys.exit(1)
