from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfpage import PDFPage
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.layout import LAParams
from pdfminer3.pdfparser import PDFParser
from pdfminer3.pdfdocument import PDFDocument
from pdfminer3.layout import LTTextBoxHorizontal
import re

'''Lasciate ogni speranza, voi ch’entrate'''

'''Check if one layer continue another '''


def is_layer_cont(prev_l, curr_l):
    prev_l_end = prev_l.split('\u2013 ')[1].split(' м')[0]
    curr_l_start = curr_l.split(' \u2013')[0]
    if prev_l_end == curr_l_start:
        return True
    else:
        return False


def find_cap_descr(start_mark, descrpath):
    fp = open(descrpath, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    mask1 = "отбора керна до привязки: %s" % (str(start_mark))
    mask2 = r'\d+\ слой'
    doc_descr = []
    for i, page in enumerate(PDFPage.create_pages(document)):
        interpreter.process_page(page)
        pdf_item = device.get_result()
        # some document-dependent rules
        for thing in pdf_item:
            if isinstance(thing, LTTextBoxHorizontal):

                if thing.get_text().find(mask1) != -1:
                    for thing1 in pdf_item:
                        if isinstance(thing1, LTTextBoxHorizontal):
                            if re.match(mask2, thing1.get_text()) and thing1.y0 < thing.y0:
                                layer_description = max([item.get_text() for item in pdf_item if
                                                         (item.y1 == thing1.y1 and isinstance(
                                                             item,
                                                             LTTextBoxHorizontal))], key=len)
                                doc_descr.append({"layer length": thing1._objs[1].get_text().split("м")[0],
                                                  "layer number": thing1.get_text().split("слой")[0],
                                                  "layer description": layer_description,
                                                  "page num": i})

                else:
                    try:
                        if doc_descr[-1:][0]['page num'] + 1 == i:
                            for thing1 in pdf_item:
                                if isinstance(thing1, LTTextBoxHorizontal):

                                    if doc_descr[-1:][0]['layer description'][-2::2] != '.':
                                        doc_descr[-1:][0]['layer description'] += thing1.get_text()

                                    if re.match(mask2, thing1.get_text()) and int(
                                            thing1.get_text().split("слой")[0]) - 1 == int(
                                        doc_descr[-1:][0]['layer number']):

                                        layer_description = max([item.get_text() for item in pdf_item if
                                                                 (item.y1 == thing1.y1 and isinstance(
                                                                     item,
                                                                     LTTextBoxHorizontal))], key=len)
                                        if is_layer_cont(doc_descr[-1:][0]['layer description'], layer_description):
                                            doc_descr.append({"layer length": thing1._objs[1].get_text().split("м")[0],
                                                              "layer number": thing1.get_text().split("слой")[0],
                                                              "layer description": layer_description,
                                                              "page num": i})
                    except IndexError:
                        pass

                    # print(thing.get_text())
                    # print("page %i" % i)
    return doc_descr


if __name__ == '__main__':
    start_mark = '3334,40'
    descrpath = '/home/jan/Documents/test/Еты-Пуровское/260по/ОПИСАНИЕ+ФОТО/Описание_260.pdf'
    find_cap_descr(start_mark, descrpath)
