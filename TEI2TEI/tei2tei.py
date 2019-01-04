# -*- coding: utf-8 -*-

import os
import re
from bs4 import BeautifulSoup

PATTERN_TITLE = re.compile(r", +\d+ -|, page \d+ -")
PATTERN_BODY = re.compile(r"</body> *\n* *<body>")
schema = '<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>\n<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>\n<TEI '

def gathers(dofacs=True, volumes=False):
    """Transform TEI XML files from input directory
    """
    #try:
    input_content_l = os.listdir(PATH_TO_INPUT)
    if len(input_content_l) == 0:
        print("Nothing in input. Exiting.")
    else:
        input_content_l[:] = (value for value in input_content_l if value != ".DS_Store")
        for document in input_content_l:
            path_to_document = os.path.join(PATH_TO_INPUT, document)
            if os.path.isfile(path_to_document) is True:
                #If we deal with just a file, we can still process it or not whether the arg -nofacs was used or not
                #This produces the same file, but without <facsimile> and @facs and @n
                with open(path_to_document) as file:
                    fileSoup = BeautifulSoup(file, 'xml')
                if dofacs is False:
                    fileSoup.facsimile.decompose()
                    for tag in fileSoup.findAll('facs' is True):
                        del(tag["facs"])
                    # This removes the  @n attributes in all <lb>
                    for lb in fileSoup.findAll("lb"):
                        del(lb["n"])
                    str_finalsoup = str(fileSoup)
                    str_finalsoup = str_finalsoup.replace("<TEI ", schema)
                    path_to_document_out = os.path.join(PATH_TO_OUTPUT, document)
                    with open(path_to_document_out, "w") as f:
                        f.write(str_finalsoup)
            else:
                input_pages_l = os.listdir(path_to_document)
                if len(input_pages_l) > 0:
                    input_pages_l[:] = (value for value in input_pages_l if value != ".DS_Store")
                    # SORTING PAGES IN RIGHT ORDER
                    sorted_input_pages_l = []
                    page_numbers = []
                    extensions = {}
                    for page in [f for f in input_pages_l if f.endswith(".xml")]:
                        page_number, extension = page.split("-")
                        page_number.strip()
                        try:
                            page_numbers.append(int(page_number))
                            extensions[int(page_number)] = extension
                        except TypeError:
                            page_numbers.append(page_number)
                            extensions[page_number] = extension
                    page_numbers.sort()
                    for page_number in page_numbers:
                        complete_filename = "%s -%s" % (page_number, extensions[page_number])
                        sorted_input_pages_l.append(complete_filename)
                    soups_list = []
                    for page in sorted_input_pages_l:
                        path_to_page = os.path.join(path_to_document, page)
                        with open(path_to_page, "rb") as f:
                            page_f = f.read()
                        soup = BeautifulSoup(page_f, "xml")
                        soups_list.append(soup)
                    if len(soups_list) > 0:
                        # Making up teiHeader from first teiHeader
                        content = soups_list[0]
                        header = content.teiHeader
                        title_orig = header.title.string
                        title = PATTERN_TITLE.sub(" -", title_orig)
                        header.title.string.replace_with(title)
                        finalsoup = BeautifulSoup('<TEI xmlns="http://www.tei-c.org/ns/1.0"><placeholder1></TEI>', "xml")
                        finalsoup.TEI.append(header)
                        # grouping facs and bodies
                        if dofacs:
                            if volumes:
                                gbg, chunck = title.split(",")
                                chunck, gbg = chunck.split("-")
                                if "(" in chunck:
                                    chunck, gbg = chunck.split("(")
                                chunck = chunck.strip()
                            else:
                                chunck_l = title_orig.split(",")
                                chunck = chunck_l[0]
                                chunck = chunck.replace(" ", "").replace("\\","-").replace("/","-").lower()
                            all_facs = [soup.facsimile for soup in soups_list]
                            for facs in all_facs:
                                finalsoup.TEI.append(facs)
                        all_body = [soup.body for soup in soups_list]
                        tag_text = BeautifulSoup('<temptext><placeholder2></temptext>', "xml")
                        tag_text = tag_text.temptext.extract()
                        finalsoup.TEI.append(tag_text)
                        for body in all_body:
                            ####
                            #This removes all the  @facs attributes in <lb>, <pb>, etc.
                            for tag in body.findAll('facs' is True):
                                del(tag["facs"])
                            #This removes the  @n attributes in all <lb>
                            for lb in body.findAll("lb"):
                                del(lb["n"])
                            ####
                            finalsoup.TEI.temptext.append(body)
                        # cleaning TEI
                        finalsoup.placeholder1.decompose()
                        finalsoup.placeholder2.decompose()
                        if dofacs:
                            all_zone = finalsoup.find_all("zone")
                            for zone in all_zone:
                                del zone["subtype"]
                        #Ça ne fonctionne pas, inutile d'appeler "contents" à mon avis. Cf plus haut.
                        '''
                        all_tags = finalsoup.TEI.contents
                        for tag in all_tags:
                            del tag["facs"]
                            '''
                        finalsoup.TEI.temptext.name = "text"

                        str_finalsoup = str(finalsoup)
                        str_finalsoup = PATTERN_BODY.sub("\n", str_finalsoup)
                        if dofacs:
                            str_finalsoup = str_finalsoup.replace("facs_", "facs_%s_" % chunck)
                        str_finalsoup = str_finalsoup.replace("<TEI ", schema)
                        # writing XML file
                        path_to_document_out = os.path.join(PATH_TO_OUTPUT, "%s.xml" % document)
                        with open(path_to_document_out, "w") as f:
                            f.write(str_finalsoup)
'''    except Exception as e:
        print(e)
'''

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transform TEI XML files.")
    parser.add_argument("-n", "--nofacs", action="store_false", help="script will ignore facsimile elements.")
    parser.add_argument("-v", "--volumes", action="store_true", help="script will use volume numbers and not title to calculate modification to facs' xml:ids.")
    parser.add_argument("-i", "--input", action="store", nargs=1, default=["input"], help="path to directory containing file to transform")
    parser.add_argument("-o", "--output", action="store", nargs=1, default=["output"], help="path to directory receiving transformed files.")
    args = parser.parse_args()

    CWD = os.path.dirname(os.path.abspath(__file__))
    PATH_TO_INPUT = os.path.join(CWD, args.input[0])
    PATH_TO_OUTPUT = os.path.join(CWD, args.output[0])

    gathers(args.nofacs, args.volumes)