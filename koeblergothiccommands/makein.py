"""
Generated by ChatGPT 3.5 on March 16 2023
Reads forms.csv and parameters.csv
Creates new input file for loanpy with 3 columns:
Segments, ID, Meanings
"""

import csv
import re

def clean(text):
    text = re.sub(r'\s*\d+\s*', ' ', text).strip()
    return text

def run(args):
    """
    """
    # Read in the two csv files
    with open('cldf/forms.csv', 'r') as forms_file:
        forms_reader = csv.reader(forms_file)
        forms_lines = list(forms_reader)

    with open('cldf/parameters.csv', 'r') as params_file:
        params_reader = csv.reader(params_file)
        params_lines = list(params_reader)

    # Create a dictionary to map parameter IDs to their corresponding names
    params_dict = {}
    for line in params_lines[1:]:
        param_id, param_name = line[0], clean(line[1])
        params_dict[param_id] = param_name

    # Create a list to hold the lines of the new csv file
    new_lines = ['ID\tForm_ID\tSegments\tProsody\tMeaning\n']

    # Iterate over the lines of the forms csv file, merging in the parameter names
    count = 0
    for line in forms_lines[1:]:
        param_name = params_dict.get(line[3], '')
        new_line = f"{count}\t{line[0]}\t{line[6]}\t{line[-1]}\t{param_name}\n"
        new_lines.append(new_line)
        count += 1

    # Write the new csv file
    with open('loanpy/got.tsv', 'w+') as new_file:
        new_file.writelines(new_lines)