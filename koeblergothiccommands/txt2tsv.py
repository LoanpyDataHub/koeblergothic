"""
Convert ``raw/gothic.txt`` (2.4MB) to ``raw/gothic.tsv`` (127kB), which
contains two columns: ``Gothic`` and ``Meaning``.
"""
import csv
from re import search, sub

def run(args):
    """
    #. Read ``raw/gothic.txt``, which was copied from
       `https://www.koeblergerhard.de/got/got.html`_
    #. Split by "\n"
    #. Loop through rows
    #. Ignore empty rows
    #. The element left of the first number is the Gothic headword
    #. The element on the right between "nhd. " (i.e. "neuhochdeutsch", i.e.
       standard German) and the semi-colon are the meanings in German
    #. Clean the data by removing special characters and brackets with their
       contents.
    #. Write it to a table called ``raw/gothic.tsv``

    """
    with open("raw/gothic.txt", "r") as f:
        data = f.read().split("\n")

    with open("raw/gothic.tsv", "w+") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["Gothic", "Meaning"])
        for row in data:
            try:  # grab form and clean
                form = search("^[^0-9,]*", row).group(0)
                form = sub("[?* )(-]", "", form)
                # grab German meaning
                meaning = search("nhd. [^;]*", row).group(0)[5:]
                # rm brackets + content
                meaning = sub(" ?\(.*\)", "", meaning)
                # rm chars
                meaning = sub("[-?„“]", "", meaning)
                # remove numbers, empty cells and "Abkürzung"
                if (not meaning.strip() or
                    all(i in "0123456789" for i in meaning.strip())
                    or "Abkürzung" in meaning
                    ):
                    continue
                # add new line
                writer.writerow([form, meaning])
                #TODO write to tsv
            except AttributeError:
                pass
