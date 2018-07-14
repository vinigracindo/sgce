# I place this in the public domain

# This only handles non-nested lists, emphasis, headings and horizontal rules (which are converted to page breaks)
# Sufficient for converting Markdown generated HTML to reportlab flowables...

import xml.sax as sax

from reportlab.platypus import PageBreak, Paragraph


def html_to_rl(html, styleSheet):
    elements = list()

    class Handler(sax.ContentHandler):
        mode = ""
        buffer = ""
        listcounter = 0
        listtype = ""

        def startElement(self, name, attrs):
            if name in ["strong", "em", "i", "b"]:
                self.mode = name
            elif name == "ol":
                self.listcounter = 1
                self.listtype = "ol"
            elif name == "ul":
                self.listtype = "ul"
            elif name == "hr":
                elements.append(PageBreak())

        def endElement(self, name):
            if name.startswith("h") and name[-1] in ["1", "2", "3", "4", "5", "6"]:
                elements.append(Paragraph(self.buffer, styleSheet["Heading%s" % name[-1]]))
            elif name in ["strong", "em", "i", "b"]:
                self.mode = ""
            elif name == "p":
                elements.append(Paragraph(self.buffer, styleSheet["BodyText"]))
            elif name == "li":
                if self.listtype == "ul":
                    elements.append(Paragraph(self.buffer, styleSheet["BodyText"], bulletText=u"•"))
                else:
                    elements.append(Paragraph(self.buffer, styleSheet["BodyText"], bulletText="%s." % self.listcounter))
                    self.listcounter += 1
            elif name in ["ol", "ul"]:
                self.listcounter = 0
                self.listtype = ""

            if name in ["h1", "h2", "h3", "h4", "h5", "h6", "p", "li"]:
                self.buffer = ""

        def characters(self, chars):
            surrounding = None

            if self.mode in ["strong", "em", "i", "b"]:
                if self.mode in ["strong", "b"]:
                    surrounding = "b"
                else:
                    surrounding = "i"

            if surrounding:
                chars = u"<%s>%s</%s>" % (surrounding, chars, surrounding)

            self.buffer += chars

    # Yeah I know... this makes Jesus cry, but unfortunately SAX wants a document element
    # surrounding everything
    sax.parseString(u"<doc>%s</doc>" % html, Handler())

    return elements