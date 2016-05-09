import ezodf
import re

invoiceNumberPrefix = "2016"
oldInvoiceNumber = "0"
newInvoiceNumber = "0"

def findInvoiceNumberAnOccurence(doc):
    lines = []
    for obj in doc.body:
        line = obj.plaintext()
        if "Rechnungs-Nr." in line:
            global oldInvoiceNumber, newInvoiceNumber
            oldInvoiceNumber = getOldInvoiceNumber(line)
            newInvoiceNumber = calcNewInvoiceNumber(oldInvoiceNumber)
            lines.append(obj)
            print obj
        elif "Kunden-Nr." in line:
            lines.append(obj)
    return lines

def replaceInvoiceNumber(lines):
    for line in lines:
        for el in iter(line):
            if oldInvoiceNumber in el:
                el.append_text("x")

def calcNewInvoiceNumber(oldInvoiceNumber):
    newInvoiceNumber = str(int(oldInvoiceNumber)+1)
    return newInvoiceNumber.zfill(3)

def getOldInvoiceNumber(line):
    number = re.findall(r"[0-9]+", line)[0]
    number = number.replace(invoiceNumberPrefix, "")
    return number


if __name__ == "__main__":
    filename = "RE_2016x_name.odt"
    doc = ezodf.opendoc(filename)

    print "Doctype:\t%s\nMimetype:\t%s" % (doc.doctype, doc.mimetype)
    lines = findInvoiceNumberAnOccurence(doc)
    print "Updating old (%s) to new (%s) invoice number" % (oldInvoiceNumber, newInvoiceNumber)
    replaceInvoiceNumber(lines)
    doc.saveas("test.odt")
        
