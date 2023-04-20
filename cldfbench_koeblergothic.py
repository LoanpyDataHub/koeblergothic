import csv
from functools import lru_cache
import pathlib

import attr
from clldutils.misc import slug
from loanpy.scapplier import Adrc
from lingpy import prosodic_string
from pylexibank import Dataset as BaseDataset, Lexeme
import spacy

# install first with $ python -m spacy download de_core_news_lg
nlp = spacy.load('de_core_news_lg')
ad = Adrc("etc/WOT2EAHsc.json", "etc/invsEAH.json")

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
            {"name": "Parameter_ID", "datatype": "string"}
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
                    "Parameter_ID": idx
                    })
                print(f"{i+1}/{len(self.concepts)} meanings checked for word vectors", end="\r")

        args.log.info("added concepts and senses")

        # add language
        languages = args.writer.add_languages()
        args.log.info("added language")

        # add forms
        data = self.raw_dir.read_csv(
            "gothic.tsv", delimiter="\t",
        )
        header = data[0]
        cognates = {}
        cogidx = 1
        adidx = 1

        with open("cldf/adapt.csv", "w+") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Form_ID", "ad100"])
            for i in range(1, len(data)):
                for lex in args.writer.add_forms_from_value(
                        Language_ID="Gothic",
                        Parameter_ID=concepts[data[i][1]], # col "Meaning" ID
                        Value=data[i][0],  # col "Gothic",
                        Source="Kobler1989",
                        Local_ID=f"f{i}"
                        ):
                    pros = prosodic_string(lex["Segments"], _output='cv')
                    lex["ProsodicStructure"] = pros

                    for pred in ad.adapt(lex["Segments"], 100, pros).split(", "):
                        writer.writerow([f"a{adidx}", f"f{str(i)}", pred])
                        adidx += 1
