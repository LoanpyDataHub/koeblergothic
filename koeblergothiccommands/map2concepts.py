"""
Map concepts to concepticon with the pysem library.
"""
import csv

from pysem.glosses import to_concepticon

def run(args):
    """"
    #. Read ``raw/gothic.tsv``
    #. Loop through data and turn it into a dictionary
    #. Input that dictionary to pysem's to_concepticon function
    #. Add the mappings to a new column where available
    #. Write the new file to ``etc/concepts.tsv``

    """
    glo = []
    with open("raw/gothic.tsv", "r") as f:
        data = list(csv.reader(f, delimiter="\t"))
    h = {i: data[0].index(i) for i in data[0]}  # headers

    for row in data[1:]:
        glo.append({"gloss": row[h["Meaning"]]})

    concepticon_dict = to_concepticon(glo, language="de",  max_matches=1)
    #print(concepticon_dict)
    with open("etc/concepts.tsv", "w+") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["Sense", "Concepticon_ID", "Concepticon_Gloss"])
        for row in data[1:]:
            try:
                con = concepticon_dict[row[h["Meaning"]]][0]
                writer.writerow([row[h["Meaning"]], con[0], con[1]])
            except (IndexError, KeyError):  # words that weren't mapped
                writer.writerow([row[h["Meaning"]], "", ""])
