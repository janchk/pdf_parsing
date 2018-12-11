import PIL
from PIL import Image, ImageDraw
import sys, os
from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import copy

import pypdf_implem
import pdfminer_ver2

from pdf2image import convert_from_bytes

# from pdfminer_ver import pdfminer_ver
'''Doing image extraction the hard way'''


def main():
    # quite bad decision to pass path instead bytes of already opened file
    pdffile_path = "/home/jan/Documents/test/Еты-Пуровское/260по/ОПИСАНИЕ+ФОТО/Рис._2.2.7-2.2.10_Еты-Пуровское_260.pdf"
    captions = pdfminer_ver2.captinons_handling(pdffile_path)
    imnames = [cap.get('image_name') for cap in captions]
    imgs = pypdf_implem.img_extract(pdffile_path, 1)
    filtred_imgs = [img for img in imgs if list(img)[0] in imnames]

    print(captions)

    bboxes = []

    return 0


if __name__ == "__main__":
    # extract_img()
    main()
