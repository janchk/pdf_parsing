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
import description_handling
from concat_and_cut import concat_all, c_n_c

from pdf2image import convert_from_bytes

# from pdfminer_ver import pdfminer_ver

'''Find coefficient of resize between original and pdf version of image'''


def rs_coeff(orig_sz, in_pdf_sz):
    coeff = lambda sz1, sz: (sz1[0] / sz[0], sz1[1] / sz[1])
    # res = [sz, sz1 for (sz, sz1) in orig_sz, in_pdf_sz]
    return [coeff(in_pdf_sz[i], orig_sz[i]) for i, _ in enumerate(orig_sz) if orig_sz[i]]
    # print(coeff)


def main():
    # quite bad decision to pass path instead bytes of already opened file
    pdffile_path = "/home/jan/Documents/test/Еты-Пуровское/260по/ОПИСАНИЕ+ФОТО/Рис._2.2.7-2.2.10_Еты-Пуровское_260.pdf"
    captions, kernt_st = pdfminer_ver2.captinons_handling(pdffile_path)
    # mesure_m(captions)
    imnames = [cap.get('image_name') for cap in captions]
    sz_inpdf = [cap.get('in_pdf_size') for cap in captions]
    sz_orig = [cap.get('src_size') for cap in captions]
    coefs = rs_coeff(sz_orig, sz_inpdf)  # x, y resize coeff
    imgs = pypdf_implem.img_extract(pdffile_path, 1)
    # filtred_imgs = [img for img in imgs if list(img)[0] in imnames]
    rgb_img, uv_img = concat_all(imgs, captions)
    # start_mark = [cap['kern_start'] for cap in captions if cap.get('kern_start')][0]  # hate this expression
    cap_descipt = description_handling.find_cap_descr(kernt_st)
    cutted_imgs = c_n_c(captions, imgs, cap_descipt)


    print(captions)

    bboxes = []

    return 0


if __name__ == "__main__":
    # extract_img()
    main()
