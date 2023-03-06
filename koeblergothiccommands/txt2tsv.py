"""
Convert raw txt to tsv
"""

from re import search, sub

def run(args):
    """
    Read values from forms.csv and IPA-transcribe the Spanish ones
    """
    #ds = Dataset.from_metadata("./cldf/cldf-metadata.json")
    lines = "Gothic\tMeaning"
    with open("raw/koebler.txt", "r") as f:
        for row in f.read().split("\n"):
            try:  # grab form and clean
                form = search("^[^0-9,]*", row).group(0)
                form = sub("[?* (-]", "", form)
                # grab German meaning
                meaning = search("nhd. [^;]*", row).group(0)[5:]
                # rm brackets + content
                meaning = sub(" ?\(.*\)", "", meaning)
                # rm chars
                meaning = sub("[-?„“]", "", meaning)
                # add new line
                lines += f"\n{form}\t{meaning}"
                #TODO write to tsv
            except AttributeError:
                pass

    # write csv
    with open("raw/koebler.tsv", "w+") as file:
        file.write(lines)
