# -*- coding: utf-8 -*-

import os
import re
import sys
from bs4 import BeautifulSoup


def gathers(dofacs):
	"""Transform TEI XML files from input directory
	"""
	input_content_l = os.listdir(PATH_TO_INPUT)
	if len(input_content_l) == 0:
		print("Nothing in input. Exiting.")
	else:
		for document in input_content_l:
			path_to_document = os.path.join(PATH_TO_INPUT, document)
			input_pages_l = os.listdir(path_to_document)
			if len(input_pages_l) > 0:
				soups_list = []
				for page in input_pages_l:
					path_to_page = os.path.join(path_to_document, page)
					with open(path_to_page, "r") as f:
						page_f = f.read()
					soup = BeautifulSoup(page_f, "xml")
					soups_list.append(soup)
				if len(soups_list) > 0:
					# Making up teiHeader from first teiHeader
					content = soups_list[0]
					header = content.teiHeader
					title = header.title.string
					title = PATTERN_TITLE.sub(" -", title)
					header.title.string.replace_with(title)
					finalsoup = BeautifulSoup("""<TEI xmlns="http://www.tei-c.org/ns/1.0"><placeholder1></TEI>""", "xml")
					finalsoup.TEI.append(header)
					# grouping facs and bodies
					if dofacs:
						gbg, number = title.split(",")
						number, gbg = number.split("-")
						if "(" in number:
							number, gbg = number.split("(")
						number = int(number.strip())
						
						all_facs = [soup.facsimile for soup in soups_list]
						for facs in all_facs:
							finalsoup.TEI.append(facs)
					all_body = [soup.body for soup in soups_list]
					tag_text = BeautifulSoup("""<temptext><placeholder2></temptext>""", "xml")
					tag_text = tag_text.temptext.extract()
					finalsoup.TEI.append(tag_text)
					for body in all_body:
						finalsoup.TEI.temptext.append(body)
					# cleaning TEI
					finalsoup.placeholder1.decompose()
					finalsoup.placeholder2.decompose()
					if dofacs:
						all_zone = finalsoup.find_all("zone")
						for zone in all_zone:
							del zone["subtype"]
					all_tags = finalsoup.TEI.contents
					for tag in all_tags:
						del tag["facs"]

					finalsoup.TEI.temptext.name = "text"
	
					str_finalsoup = str(finalsoup)
					str_finalsoup = PATTERN_BODY.sub("\n", str_finalsoup)
					if dofacs:
						str_finalsoup = str_finalsoup.replace("facs_", "facs_%s_" % number)
					schema = """<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>\n<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>\n<TEI """
					str_finalsoup = str_finalsoup.replace("<TEI ", schema)
					# writing XML file
					path_to_document_out = os.path.join(PATH_TO_OUTPUT, "%s.xml" % document)
					with open(path_to_document_out, "w") as f:
						f.write(str_finalsoup)
	return


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Transform TEI XML files.")
	parser.add_argument("-n", "--nofacs", action="store_false", help="script will ignore facsimile elements.")
	args = parser.parse_args()
#	dofacs = args.nofacs
#	print(dofacs)

	CWD = os.path.dirname(os.path.abspath(__file__))
	PATH_TO_INPUT = os.path.join(CWD, "input")
	PATH_TO_OUTPUT = os.path.join(CWD, "output")
	PATTERN_TITLE = re.compile(r", +\d+ -|, page \d+ -")
	PATTERN_BODY = re.compile(r"</body> *\n* *<body>")

	gathers(args.nofacs)