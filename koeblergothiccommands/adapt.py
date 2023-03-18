"""
Add reconstructions to hun.tsv
"""

from loanpy.apply import Adrc

BANNED = ("wrong clusters", "wrong phonotactics", "not old",
"wrong vowel harmony")

def run(args):
    """
    Read raw file
    Adapt
    write results to new raw file
    """
    # Read in data on correspondences and inventories
    ad = Adrc(
    "../ronataswestoldturkic/loanpy/WOT2EAHsc.json",
    "../ronataswestoldturkic/loanpy/invsEAH.json"
    )
    # Read TSV file content into a string
    with open("loanpy/got.tsv", "r") as f:
        gottsv = f.read().strip().split("\n")
    lines = gottsv.pop(0) + "\tadapted\tpredicted_phonotactics\tadapted_phonotactics\tbefore_combinatorics"
    # Add reconstructions to new column
    for row in gottsv:
        row_parts = row.split("\t")
        adapted = ad.adapt(row_parts[2], 100, row_parts[3], False, False, 3,
        show_workflow=True)
        if any(i in adapted for i in BANNED):
            continue
        workflow = [str(ad.workflow[i]) for i in ad.workflow]
        lines += "\n" + "\t".join([row, adapted] + workflow)

    # write csv
    with open("loanpy/adgot.tsv", "w+") as file:
        file.write(lines)
