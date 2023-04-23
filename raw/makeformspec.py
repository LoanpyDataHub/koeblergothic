"""
#. Read raw file
#. Create empty dictionary for formspec
#. Loop through rows
#. If a word ends on -ik: add it as dictionary key.
   Value is the word without -ik
#. Write the dictionary to json
"""

import csv
import json
import re

with open("gothic.tsv", "r") as f:
    dfraw = list(csv.reader(f, delimiter="\t"))

formspec = {}

for row in dfraw:
    if bool(re.findall("an$", row[0])):
        formspec[row[0]] = re.sub("an$", "", row[0])

with open("../etc/formspec.json", "w+") as f:
    json.dump(formspec, f)
