from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfpage import PDFPage
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.layout import LAParams
from pdfminer3.pdfparser import PDFParser
from pdfminer3.pdfdocument import PDFDocument
from pdfminer3.layout import LTImage, LTFigure, LTTextBoxHorizontal


def captinons_handling(pdf_path):
    fp = open(pdf_path, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    caps = []
    desc_p = None

    for i, page in enumerate(PDFPage.create_pages(document)):
        # This is aux variable for detecting repeating core captions.
        # Assuming the uv images will be annotated exactly same as rgb images.
        aux_annot = []
        uv = False
        interpreter.process_page(page)
        pdf_item = device.get_result()
        for item in pdf_item:
            if isinstance(item, LTTextBoxHorizontal):
                p_descr = item.get_text().find('отбора керна до привязки:')
                if p_descr != -1:
                    desc_p = item.get_text()[p_descr + 26: p_descr + 33]  # another type of hardcoding
                    # print(desc_p)
            if isinstance(item, LTTextBoxHorizontal):
                if item.get_text().find('в ультрафиолетовом свете') != -1:
                    uv = True
                else:
                    uv = False
            if isinstance(item, LTImage):
                print('img')
                # save_image(thing)
            if isinstance(item, LTFigure):
                # print('figure')

                captions = find_captions_for_img(item, pdf_item)
                if captions:
                    im_name, top_cap, bot_cap, sz, src_sz, pred = captions
                    if top_cap not in aux_annot:
                        aux_annot.append(top_cap)
                    else:
                        uv = True
                    caps.append({"page": i, "image_name": im_name, "top_caption": top_cap, "bottom_caption": bot_cap,
                                 "in_pdf_size": sz, "src_size": src_sz, "is_ruler": pred, "is_uv": uv})
    # caps.append({'kern_start': desc_p})
    if not desc_p:
        desc_p = [cap for cap in caps if cap['is_ruler'] == False][0]['top_caption'][0]
    return caps, desc_p
    # print(i, captions)


'''Top and bottom captions for all images, 
except that one that haven't the top one '''


def find_captions_for_img(outer_layout, items):
    for in_thing in outer_layout:
        if isinstance(in_thing, LTImage):
            h = int(in_thing.y1 - in_thing.y0)
            w = int(in_thing.x1 - in_thing.x0)
            top_img_caption = [item.get_text() for item in items if
                               (item.y1 > (in_thing.y1 + in_thing.y0) / 2 and item.x0 < (
                                       (in_thing.x1 + in_thing.x0) / 2) < item.x1 and isinstance(item,
                                                                                                 LTTextBoxHorizontal))]

            bot_img_caption = [item.get_text() for item in items if
                               (item.y1 < (in_thing.y1 + in_thing.y0) / 2 and item.x0 < (
                                       (in_thing.x1 + in_thing.x0) / 2) < item.x1 and isinstance(item,
                                                                                                 LTTextBoxHorizontal))]
            try:
                # Not ruler images
                if top_img_caption:
                    # some kind of hardcoding
                    return in_thing.name, top_img_caption[0].split('\n')[:2], bot_img_caption[0].split('\n')[:2], (
                        w, h), in_thing.srcsize, False
                # The ruler image
                else:
                    return in_thing.name, None, None, (w, h), in_thing.srcsize, True
                # print(top_img_caption[0], bot_img_caption[0])
            # The ruler image
            except IndexError:
                return in_thing.name, None, None, (w, h), in_thing.srcsize, True


if __name__ == '__main__':
    path = '/home/jan/Documents/test/Еты-Пуровское/260по/ОПИСАНИЕ+ФОТО/Рис._2.2.7-2.2.10_Еты-Пуровское_260.pdf'
    print(captinons_handling(path))
