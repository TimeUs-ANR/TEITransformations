# -*- coding: utf-8 -*-

import os
from bs4 import BeautifulSoup

def maketeicorpus(volumes=False, sort=False):
    input_content_l = os.listdir(PATH_TO_INPUT)
    if len(input_content_l) == 0:
        print("Nothing in input. Exit.")
    else:
        input_content_l[:] = (value for value in input_content_l if value != ".DS_Store")
        filename = str(input("Choose a name for output: "))
        filename = filename.replace(".", "_").replace("/", "_").replace("\\", "_")
        if sort:
            # Sorting files from filenames
            document_names = []
            for document in [f for f in input_content_l if f.endswith(".xml")]:
                name, ext = document.split(".")
                try:
                    document_names.append(int(name))
                except TypeError:
                    document_names.append(name)
            document_names.sort()
            temp_list = ["%s.xml" % dn for dn in document_names]
            document_list = temp_list[:]
        else:
            document_list = input_content_l[:]
        sorted_k = {}
        soups_dict = {}
        for document in document_list:
            path_to_document = os.path.join(PATH_TO_INPUT, document)
            with open(path_to_document, "r") as f:
                doc_f = f.read()
            soup = BeautifulSoup(doc_f, "xml")
            title_orig = soup.TEI.teiHeader.titleStmt.title.string
            if volumes:
                # Sorting files from title element
                gbg, piece = title_orig.split(",")
                piece, gbg = piece.split("-")
                if "_duplicated" in piece:
                    piece, gbg = piece.split("_duplicated")
                if "(" in piece:
                    piece, gbg = piece.split("(")
                piece = int(piece.strip())
            else:
                piece = title_orig.replace(" ", "_").replace("/", "-").replace("\\", "-").lower()
            soups_dict[piece] = soup
            if sort:
                # intermediary for sorting
                sorted_k[document] = piece
        list_keys = soups_dict.keys()
        if volumes:
            list_keys = sorted(list_keys)
        if sort:
            list_keys = [sorted_k[dn] for dn in document_list]
        globalheader = '<teiCorpus xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt><title>%s</title></titleStmt><publicationStmt><p></p></publicationStmt><sourceDesc><p></p></sourceDesc></fileDesc></teiHeader></teiCorpus>' % filename
        finalsoup = BeautifulSoup(globalheader, "xml")
        for key in list_keys:
            soup = soups_dict[key]
            tei = soup.TEI
            finalsoup.teiCorpus.append(tei)
        path_to_output_file = os.path.join(PATH_TO_OUTPUT, "%s.xml" % filename)
        str_finalsoup = str(finalsoup)
        schema = '<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>\n<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>\n<teiCorpus '
        str_finalsoup = str_finalsoup.replace("<teiCorpus ", schema)
        # Writing XML file
        with open(path_to_output_file, "w") as f:
            f.write(str_finalsoup)



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transform TEI XML files.")
    parser.add_argument("-i", "--input", action="store", nargs=1, default=["input"], help="path to directory containing file to transform")
    parser.add_argument("-o", "--output", action="store", nargs=1, default=["output"], help="path to directory receiving transformed file.")
    parser.add_argument("-v", "--volumes", action="store_true", help="if title tags in files refer to unique volume numbers, they will be sorted before merging. Not compatible with -s.")
    parser.add_argument("-s", "--sort", action="store_true", help="if filenames are numbers, they will be sorted before merging. Not compatible with -v.")
    args = parser.parse_args()

    CWD = os.path.dirname(os.path.abspath(__file__))
    PATH_TO_INPUT = os.path.join(CWD, args.input[0])
    PATH_TO_OUTPUT = os.path.join(CWD, args.output[0])

    maketeicorpus(args.volumes, args.sort)
