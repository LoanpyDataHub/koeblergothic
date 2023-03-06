"""
Map concepts to concepticon and make a wordlist.
"""

from cldfbench_koeblergothic import Dataset as GTH
from pysem.glosses import to_concepticon

def run(args):
    """"
    read gothic.tsv,
    link data to concepticon,
    write concepts.tsv
    """
    gth = GTH()
    glo = []
    for row in gth.raw_dir.read_csv("gothic.tsv", delimiter="\t")[1:]:
        glo.append({"gloss": row[1]})  # Sense
    lines = "Sense\tConcepticon_ID\tConcepticon_Gloss"

    condict = to_concepticon(glo, language="de",  max_matches=1)

    for row in gth.raw_dir.read_csv("gothic.tsv", delimiter="\t")[1:]:
        try:
            lines += f"\n{row[1]}\t{condict[row[1]][0][0]}\t{condict[row[1]][0][1]}"
        except IndexError:  # words that weren't mapped
            lines += f"\n{row[1]}\t\t"  # get an empy line

    with open(gth.etc_dir / "concepts.tsv", "w+") as file:
        file.write(lines)
