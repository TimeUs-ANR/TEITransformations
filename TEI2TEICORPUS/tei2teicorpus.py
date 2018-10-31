# -*- coding: utf-8 -*-

import os
import re
from bs4 import BeautifulSoup

CWD = os.path.dirname(os.path.abspath(__file__))
PATH_TO_INPUT = os.path.join(CWD, "input")
PATH_TO_OUTPUT = os.path.join(CWD, "output")

def maketeicorpus(filename=None):
	input_content_l = os.listdir(PATH_TO_INPUT)
	if len(input_content_l) == 0:
		print("Nothing in input. Exit.")
	else:
		filename = filename or input("Choose a name for output file : ")
		filename = filename.replace(".", "_").replace("/", "_").replace("\\", "_") 
		soups_dict = {}
		for document in input_content_l:
			path_to_document = os.path.join(PATH_TO_INPUT, document)
			with open(path_to_document, "r") as f:
				document_f = f.read()
			soup = BeautifulSoup(document_f, "xml")
			title = soup.TEI.teiHeader.titleStmt.title.string
			gbg, number = title.split(",")
			number, gbg = number.split("-")
			if "(" in number:
				number, gbg = number.split("(")
			number = int(number.strip()) 
			soups_dict[number] = soup
		list_num = soups_dict.keys()
		list_num = sorted(list_num)
		globalheader = '<teiCorpus xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt><title>%s</title></titleStmt><publicationStmt><p></p></publicationStmt><sourceDesc><p></p></sourceDesc></fileDesc></teiHeader></teiCorpus>' % filename 
		finalsoup = BeautifulSoup(globalheader, "xml")
		for num in list_num:
			soup = soups_dict[num]
			tei = soup.TEI
			finalsoup.teiCorpus.append(tei)
		path_to_output_file = os.path.join(PATH_TO_OUTPUT, "%s.xml" % filename)
		str_finalsoup = str(finalsoup)
		schema = '<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>\n<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>\n<teiCorpus '
		str_finalsoup = str_finalsoup.replace("<teiCorpus ", schema)
		# Writing XML file
		with open(path_to_output_file, "w") as f:
			f.write(str_finalsoup)
	return


if __name__ == "__main__":
	maketeicorpus()