"""
IPA-transcribe Spanish words
"""

from cldfbench_koeblergothic import Dataset as GTH
from lingpy.sequence.sound_classes import ipa2tokens
import epitran

epi = epitran.Epitran("got-Latn").transliterate

def segipa(w):
    return ' '.join(ipa2tokens(epi(w)))

def run(args):
    """
    Read values from forms.csv and IPA-transcribe the Spanish ones
    """
    gth = GTH()
    #ds = Dataset.from_metadata("./cldf/cldf-metadata.json")
    lines = "Grapheme\tIPA"
    wrdlst = []
    for row in gth.cldf_dir.read_csv("forms.csv")[1:]:
        for wrd in row[4].split(" "):
            if wrd not in wrdlst:  # to avoid doublets
                lines += f"\n{wrd}\t{segipa(wrd)}"
                wrdlst.append(wrd)

    # write csv
    with open("etc/orthography.tsv", "w+") as file:
        file.write(lines)
