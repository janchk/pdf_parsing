from binascii import b2a_hex
from io import StringIO
from pdfminer3.converter import TextConverter
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfpage import PDFPage
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.layout import LAParams
from pdfminer3.pdfparser import PDFParser
from pdfminer3.pdfdocument import PDFDocument
from pdfminer3.layout import LTImage, LTFigure, LTTextBoxHorizontal
import io
import PIL.Image

fp = open('/home/jan/Documents/test/Еты-Пуровское/260по/ОПИСАНИЕ+ФОТО/Рис._2.2.7-2.2.10_Еты-Пуровское_260.pdf', 'rb')
parser = PDFParser(fp)
document = PDFDocument(parser)
rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)

'''Top and bottom captions for all images, 
except that one that haven't the top one '''


def find_captions_for_img(outer_layout, items):
    for in_thing in outer_layout:
        if isinstance(in_thing, LTImage):
            top_img_caption = [item.get_text() for item in items if
                               (item.y1 > (in_thing.y1 + in_thing.y0) / 2 and item.x0 < (
                                       (in_thing.x1 + in_thing.x0) / 2) < item.x1 and isinstance(item,
                                                                                                 LTTextBoxHorizontal))]

            bot_img_caption = [item.get_text() for item in items if
                               (item.y1 < (in_thing.y1 + in_thing.y0) / 2 and item.x0 < (
                                       (in_thing.x1 + in_thing.x0) / 2) < item.x1 and isinstance(item,
                                                                                                 LTTextBoxHorizontal))]

            try:
                if top_img_caption:
                    return ((top_img_caption[0], bot_img_caption[0]))
                # print(top_img_caption[0], bot_img_caption[0])
            except IndexError:
                pass
    # return captions

    # PIL.Image.frombytes('RGBA', (600,600), thing.stream)
    # save_image(thing)


for page in PDFPage.create_pages(document):
    interpreter.process_page(page)
    pdf_item = device.get_result()
    for thing in pdf_item:
        if isinstance(thing, LTImage):
            print('img')
            # save_image(thing)
        if isinstance(thing, LTFigure):
            # print('figure')

            captions = find_captions_for_img(thing, pdf_item)
            if captions:
                print(captions)
