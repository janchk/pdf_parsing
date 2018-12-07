import PIL
from PIL import Image, ImageDraw
import sys, os
from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import copy
import minecart
from pdf2image import convert_from_bytes

# from pdfminer_ver import pdfminer_ver
'''Doing image extraction the hard way'''


def visualisation(pdfdoc, *bboxes):
    print(bboxes)
    pdfpage_img = convert_from_bytes(open(pdfdoc, 'rb').read())
    for i, img in enumerate(pdfpage_img):
        draw = ImageDraw.Draw(img)
        dr = lambda x: draw.rectangle(x, fill=(128, 128, 0),  width=1)
        for bbox in bboxes[0]:
            if bbox['page'] == i:
                dr(bbox['bbox'])
        img.show()
        # for box in bboxes:


    rect = patches.Rectangle
    pdfpage_img.show()



def get_img_coords(pdfdoc):
    pdfdoc = open(pdfdoc, 'rb')
    doc = minecart.Document(pdfdoc)
    pdfdoc.close()
    for i, page in enumerate(doc.iter_pages()):
        for image in page.images:
            yield {'page': i, 'bbox': tuple(_ for _ in image.coords)}


def main():
    # quite bad decision to pass path instead bytes of already opened file
    pdffile_path = "/home/jan/Documents/test/Еты-Пуровское/260по/ОПИСАНИЕ+ФОТО/Рис._2.2.7-2.2.10_Еты-Пуровское_260.pdf"
    bboxes = []
    for bb in get_img_coords(pdffile_path):
        bboxes.append(bb)
    visualisation(pdffile_path, bboxes)

    return 0


def extract_img():
    pdf = open("/home/jan/Documents/test/Еты-Пуровское/260по/ОПИСАНИЕ+ФОТО/Рис._2.2.7-2.2.10_Еты-Пуровское_260.pdf",
               'rb').read()

    startmark = "\xff\xd8"
    startfix = 0
    endmark = "\xff\xd9"
    endfix = 2
    i = 0

    njpg = 0
    while True:
        istream = pdf.find("stream", i)
        if istream < 0:
            break
        istart = pdf.find(startmark, istream, istream + 20)
        if istart < 0:
            i = istream + 20
            continue
        iend = pdf.find("endstream", istart)
        if iend < 0:
            raise Exception("Didn't find end of stream!")
        iend = pdf.find(endmark, iend - 20)
        if iend < 0:
            raise Exception("Didn't find end of JPG!")

        istart += startfix
        iend += endfix
        print("JPG %d from %d to %d" % (njpg, istart, iend))
        jpg = pdf[istart:iend]
        # jpgfile = file("jpg%d.jpg" % njpg, "wb")
        # jpgfile.write(jpg)
        # jpgfile.close()

        njpg += 1
        i = iend


if __name__ == "__main__":
    # extract_img()
    main()
