from functools import lru_cache

import attr
import csv
from loanpy.scapplier import Adrc
import pathlib
from pylexibank import Dataset as BaseDataset, Lexeme
from clldutils.misc import slug
from lingpy import prosodic_string
import spacy

# install first with $ python -m spacy download de_core_news_lg
nlp = spacy.load('de_core_news_lg')
ad = Adrc("etc/WOT2EAHsc.json")

@lru_cache(maxsize=None)
def filter_vectors(meaning):
    """
    filter out stopwords, add only if vector available.
    """
    return meaning if nlp(meaning).has_vector else None

@attr.s
class CustomLexeme(Lexeme):
    ProsodicStructure = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "koeblergothic"
    lexeme_class = CustomLexeme

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """

        #add sense table
        args.writer.cldf.add_component(
            "SenseTable",
            {"name": "Spacy", "datatype": "string"},
            {"name": "Form_ID", "datatype": "string"}
        )

        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = {}
        for i, concept in enumerate(self.concepts):
            idx = str(i)+"_"+slug(concept["Sense"])
            concepts[concept["Sense"]] = idx
            args.writer.add_concept(
                    ID=idx,
                    Name=concept["Sense"],
                    Concepticon_ID=concept["Concepticon_ID"],
                    Concepticon_Gloss=concept["Concepticon_Gloss"],
                    )
            for j, sense_desc in enumerate(concept["Sense"].split(", ")):
                vector = filter_vectors(sense_desc)
                args.writer.objects["SenseTable"].append({
                    "ID": str(i) + "_" + slug(sense_desc) + "-" + str(j + 1),
                    "Entry_ID": 0,
                    "Description": sense_desc.strip(),
                    "Spacy": vector,
                    "Form_ID": idx
                    })
                print(f"{i+1}/{len(self.concepts)} meanings checked for word vectors", end="\r")

        args.log.info("added concepts and senses")

        # add language
        languages = args.writer.add_languages()
        args.log.info("added languages")

        # add forms
        data = self.raw_dir.read_csv(
            "gothic.tsv", delimiter="\t",
        )
        header = data[0]
        cognates = {}
        cogidx = 1

        with open("cldf/adapt.csv", "w+") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Form_ID", "ad100"])
            for i in range(1, len(data)):
                cognates = dict(zip(header, data[i]))
                #print(cognates)
                concept = data[i][1]  # col "Sense"
                for language in languages:
                    #print(language)
                    cog = cognates.get(language, "").strip()
                    #print(cog)
                    if concept not in cognates:
                        cognates[concept] = cogidx
                        cogidx += 1

                    cogid = cognates[concept]
                    #print(cogid, type(cogid))
                    for lex in args.writer.add_forms_from_value(
                            Language_ID=language,
                            Parameter_ID=concepts[concept],
                            Value=cog,
                            Source="Kobler1989",
                            Cognacy=cogid,
                            ):
                        lex["ProsodicStructure"] = prosodic_string(lex["Segments"], _output='cv')

                        for j, pred in enumerate(ad.adapt(lex["Segments"], 100).split(", ")):
                            primarykey = str(j) + "_" + lex["Form"] + "-" + str(i)
                            writer.writerow([primarykey, lex["ID"], pred])
