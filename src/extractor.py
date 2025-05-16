import json
import sys

from xml2rfc import XmlRfcParser
from xml2rfc.writers import TextWriter
from xml2rfc.writers.text import base_joiners, MAX_WIDTH


def main():
    if len(sys.argv) > 1:
        xml_file = sys.argv[1]
        parser = XmlRfcParser(xml_file)
        xmlrfc = parser.parse()
        text = TextWriter(xmlrfc)
        extract = {}

        # abstract
        abstract = ""
        abstract_element = text.root.xpath("//abstract")[0]
        abstract_lines = text.render_abstract(
            e=abstract_element, width=MAX_WIDTH, joiners=base_joiners
        )
        for line in abstract_lines[2:]:
            abstract += line.text.strip() + " "
        extract["abstract"] = abstract

        # authors
        authors = []
        author_elements = text.root.xpath("//rfc/front/author")
        for author in author_elements:
            author_name = text.render_author_name(author, width=MAX_WIDTH).split("\n")[0]
            role = None
            if "(editor)" in author_name:
                author_name = author_name.replace(" (editor)", "")
                role = "editor"
            email = None
            try:
                email = author.xpath("//address/email")[0].text
            except IndexError:
                pass
            authors.append({"author": author_name, "role": role, "email": email})
        extract["authors"] = authors

        # print results
        print(json.dumps(extract, sort_keys=True))
    else:
        print("Are you forgetting something?")


if __name__ == "__main__":
    main()
