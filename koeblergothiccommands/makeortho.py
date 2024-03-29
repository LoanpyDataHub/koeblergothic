"""
IPA-transcribe and tokenise Gothic words with epitran and lingpy.
The transcription rules were created based on Braune (2004) and contributed
to epitran through a pull request.
"""
import csv

from lingpy.sequence.sound_classes import ipa2tokens
import epitran

epi = epitran.Epitran("got-Latn").transliterate

def run(args):
    """
    #. Read values from ``raw/gothic.tsv``
    #. Loop through this file row by row
    #. Transcribe column ``Gothic`` to `IPA
       <https://www.internationalphoneticassociation.org/sites/default/files/IPA_Kiel_2015.pdf>`_
    #. Tokenise the IPA-transcription
    #. Write the result to ``etc/orthography.tsv``

    """
    #ds = Dataset.from_metadata("./cldf/cldf-metadata.json")
    wrdlst = []
    with open("cldf/forms.csv", "r") as f:
        data = list(csv.reader(f)) #, delimiter="\t"))

    with open("etc/orthography.tsv", "w+") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["Grapheme", "IPA"])
        for row in data[1:]:
            if row[5] not in wrdlst:  # to avoid doublets
                ipa = epi(row[5])
                ipa = ipa2tokens(ipa, merge_vowels=False, merge_geminates=False)
                ipa = " ".join(ipa)
                writer.writerow([row[5], ipa])
                wrdlst.append(row[5])
