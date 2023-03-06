import pathlib
from pylexibank import Dataset as BaseDataset
from clldutils.misc import slug


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "koeblergothic"

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """

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
        args.log.info("added concepts")

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
                args.writer.add_forms_from_value(
                        Language_ID=language,
                        Parameter_ID=concepts[concept],
                        Value=cog,
                        Source="Kobler1989",
                        Cognacy=cogid,
                        )
