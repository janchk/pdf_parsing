from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfpage import PDFPage
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.layout import LAParams
from pdfminer3.pdfparser import PDFParser
from pdfminer3.pdfdocument import PDFDocument
from pdfminer3.layout import LTTextBoxHorizontal
import re


def find_cap_descr(start_mark='3334,40'):
    fp = open('/home/jan/Documents/test/Еты-Пуровское/260по/ОПИСАНИЕ+ФОТО/Описание_260.pdf',
              'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    mask1 = "отбора керна до привязки: %s" % (str(start_mark))
    mask2 = r'\d\ слой'
    doc_descr = []
    for i, page in enumerate(PDFPage.create_pages(document)):
        interpreter.process_page(page)
        pdf_item = device.get_result()
        # some document-dependent rules
        for thing in pdf_item:
            if isinstance(thing, LTTextBoxHorizontal):
                # pass

                if thing.get_text().find(mask1) != -1:
                    for thing1 in pdf_item:
                        if isinstance(thing1, LTTextBoxHorizontal):
                            if re.match(mask2, thing1.get_text()):
                                layer_description = [item.get_text() for item in pdf_item if
                                                     (item.y1 == thing1.y1 and isinstance(
                                                         item,
                                                         LTTextBoxHorizontal))]
                                doc_descr.append({"layer length": thing1._objs[1].get_text().split('м')[0],
                                                  "layer number": thing1.get_text().split('слой')[0],
                                                  'layer description': layer_description[1]})
                                # print(layer_description[1])
                                # print(thing1.get_text().split('слой')[0])
                                # print(thing1._objs[1].get_text().split('м')[0])

                    print(thing.get_text())
                    print("page %i" % i)
    return doc_descr
    # print('cap_not_find')

    # for cap in captions:
    # make search mask
    # cap1 = cap.get("top_caption")
    # cap2 = cap.get("bottom_caption")
    # mask = "%s \u2013 %s м" % (cap1[0], cap2[0])
    # mask1 = "%s - %s м" % (cap1[0], cap2[0])


if __name__ == '__main__':
    find_cap_descr()
    # fp = open('/home/jan/Documents/test/Еты-Пуровское/260по/ОПИСАНИЕ+ФОТО/Описание_260.pdf',
    #           'rb')
    # parser = PDFParser(fp)
    # document = PDFDocument(parser)
    # rsrcmgr = PDFResourceManager()
    # laparams = LAParams()
    # device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # interpreter = PDFPageInterpreter(rsrcmgr, device)
    #
    # for i, page in enumerate(PDFPage.create_pages(document)):
    #     interpreter.process_page(page)
    #     pdf_item = device.get_result()
    #     for thing in pdf_item:
    #         if isinstance(thing, LTTextBoxHorizontal):
    #             print('lol')
    # if isinstance(thing, LTImage):
    #     print('img')
    # save_image(thing)
    # if isinstance(thing, LTFigure):
    # print('figure')

    # captions = find_captions_for_img(thing, pdf_item)
    # if captions:
    #     print(i, captions)
