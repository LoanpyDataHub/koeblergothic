"""

#. Replace badges with plain links

"""


REPLACEBADGES = {  # plain links, no badges

r"\sphinxhref{https://creativecommons.org/licenses/by/4.0/}" +
r"{\sphinxincludegraphics{{/home/viktor/Documents/GitHub/" +
r"koeblergothic/docs/doctrees/images/" +
r"554312bbffabcb804cf4f8c50b1b75a140d3bd2b/by}.svg}}":

r"License: CC BY 4.0\\\\" + "\n",

r"\sphinxhref{https://dl.circleci.com/status-badge/redirect/gh/" +
r"LoanpyDataHub/koeblergothic/tree/main}{\sphinxincludegraphics" +
r"{{/home/viktor/Documents/GitHub/koeblergothic/docs/doctrees/" +
r"images/09619620f04a0b9daccc2b299f02099ffce39f65/main}.svg}}":

r"Continuous integration: " +
r"https://dl.circleci.com/status-badge/redirect/gh/" +
r"LoanpyDataHub/koeblergothic/tree/main\\\\"  + "\n",

r"\sphinxhref{https://koeblergothic.readthedocs.io/en/latest/" +
r"?badge=latest}{\sphinxincludegraphics{{/home/viktor/Documents/GitHub/" +
r"koeblergothic/docs/doctrees/images/" +
r"9b30f25f595f5584c40ef1116026fa820e74e472/" +
r"0f1c33b7db7a03ae02d9075a982c7bfde39b1b7c}.svg}}":

r"Documentation: https://koeblergothic.readthedocs.io/en/latest/\\\\" +
"\n",

r"\sphinxhref{https://github.com/martino-vic/koeblergothic/" +
r"actions?query=workflow\%3ACLDF-validation}{\sphinxincludegraphics" +
r"{{/home/viktor/Documents/GitHub/koeblergothic/docs/doctrees/" +
r"images/580b3fd8a4bcaebea8d57e461cbaf9aac282702f/badge}.svg}}":

r"CLDF validation: " +
r"https://github.com/martino-vic/koeblergothic/" +
r"actions?query=workflow\%3ACLDF-validation\\\\" +
"\n",

r"\sphinxincludegraphics{{/home/viktor/Documents/GitHub/" +
r"koeblergothic/docs/doctrees/images/" +
r"d44641bc24451db56ba1c2f56d656871246a1945" +
r"/Glottolog-100%25-brightgreen}.svg}":

r"Glottolog: 100\%\\\\" + "\n",

r"\sphinxincludegraphics{{/home/viktor/Documents/GitHub/koeblergothic/docs" +
r"/doctrees/images/389eb097b9ce58236a5bb6e1dc3e4464ba4cdea7/" +
r"Concepticon-44%25-red}.svg}":

r"Concepticon: 44\%\\\\" + "\n",

r"\sphinxincludegraphics{{/home/viktor/Documents/GitHub/" +
r"koeblergothic/docs/doctrees/images/" +
r"8610b4fe2e7a97bed23df74a39cd30feda0b8612/Source-100%25-brightgreen}.svg}":

r"Source: 100\%\\\\",

r"\sphinxincludegraphics{{/home/viktor/Documents/GitHub/" +
r"koeblergothic/docs/doctrees/images/" +
r"54c8ae34ac3ec41286b604aef9bcbad15a74f3de/BIPA-100%25-brightgreen}.svg}":

r"BIPA: 100\%\\\\" + "\n",

r"\sphinxincludegraphics{{/home/viktor/Documents/GitHub/" +
r"koeblergothic/docs/doctrees/images/" +
r"64600fa1cdb6b54d89ce1e5ebac95262ca62a8fc/" +
r"b8fdf0ffe8e33ddbdc635aa3b469289f77c84efb}.svg}":

r"CLTS SoundClass: 100\%\\\\" + "\n",

r"\sphinxincludegraphics{{/home/viktor/Documents/GitHub/koeblergothic/" +
r"docs/doctrees/images/" +
r"c3fc0d15caf7cfd7c9ad9b01477f4d06037e63e7/" +
r"fa63eac5f41847bbc5b468c4072572f6e8080f56}" +
".svg}":

r"Vector coverage: 92\%\\\\" + "\n",

r"\sphinxhref{https://pypi.org/project/spacy/}{\sphinxincludegraphics" +
r"{{/home/viktor/Documents/GitHub/koeblergothic/docs/doctrees/images/" +
r"2d081927145272de8a9ed568341618987dcea5d3/SpaCy-v3.5}.1-blue}}":

r"SpaCy: v3.5.1\\\\" + "\n"

}

def process_tex_file(input_filename, output_filename):
    """
    #. Read the file from specified path
    #. Apply changes from dictionaries defined on top
    #. Write file to specified path

    """
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        content = input_file.read()

    for dictionary in [REPLACEBADGES]:
        for key in dictionary:
            content = content.replace(key, dictionary[key])

    with open(output_filename, 'w', encoding='utf-8') as output_file:
        output_file.write(content)


if __name__ == "__main__":
    process_tex_file(
        'docs/latex/koeblergothic.tex',
        'docs/latex/koeblergothic2.tex'
        )
