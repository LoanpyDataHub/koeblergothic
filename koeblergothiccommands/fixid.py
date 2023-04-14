"""
Replace primary key of ``forms.csv``. This can't be done from lexibank script.
Necessary because default keys eat up too much space.
Read and write files with the inbuilt csv package.
"""

import csv

def run(args):
    """
    #. read ``cldf/forms.csv``
    #. Replace contents of column ID with f0, f1, f2, f3,...
    #. Write file.
    
    """
    with open("cldf/forms.csv", "r") as f:
        data = list(csv.reader(f))
    with open("cldf/forms.csv", "w+") as f:
        writer = csv.writer(f)
        writer.writerow(data[0])  # headers
        for i, row in enumerate(data[1:]):
            row[0] = f"f{i+1}"
            writer.writerow(row)
