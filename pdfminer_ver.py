from binascii import b2a_hex
from io import StringIO
from pdfminer3.converter import TextConverter
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfpage import PDFPage
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.layout import LAParams
# from pdfminer.layout import LTImage
import io

# def extract_img_coords(pdf_path):
#     with open(pdf_path, 'rb') as fh:
#         for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):


def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            resource_manager = PDFResourceManager()
            laparams =
            device = PDFPageAggregator(resource_manager)
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()

            yield text

            # close open handles

            converter.close()

            fake_file_handle.close()


def extract_text(pdf_path):
    for page in extract_text_by_page(pdf_path):
        print(page)

        print()


def pdfminer_ver(pdfdoc):
    print('pdfminer ver')

    # doc = PDFDocument(parser)

    # parser.set_document(doc)

    # _parse_pages(doc)


if __name__ == "__main__":
    print(extract_text(
        "/home/jan/Documents/test/Еты-Пуровское/260по/ОПИСАНИЕ+ФОТО/Рис._2.2.7-2.2.10_Еты-Пуровское_260.pdf"))
