"""
IPA-transcribe Spanish words
"""
import csv

from lingpy.sequence.sound_classes import ipa2tokens
import epitran

epi = epitran.Epitran("got-Latn").transliterate

def run(args):
    """
    Read values from ``raw/gothic.tsv`` and IPA-transcribe + segment them
    """
    #ds = Dataset.from_metadata("./cldf/cldf-metadata.json")
    wrdlst = []
    with open("raw/gothic.tsv", "r") as f:
        data = list(csv.reader(f, delimiter="\t"))

    with open("etc/orthography.tsv", "w+") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["Grapheme", "IPA"])
        for row in data[1:]:
            if row[0] not in wrdlst:  # to avoid doublets
                ipa = epi(row[0])
                ipa = ipa2tokens(ipa, merge_vowels=False, merge_geminates=False)
                ipa = " ".join(ipa)
                writer.writerow([row[0], ipa])
                wrdlst.append(row[0])
