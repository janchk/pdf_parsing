import pypdf_implem
import pdfminer_ver2
import description_handling
import os
from concat_and_cut import concat_all, c_n_c


def main():
    for dir in os.listdir('/home/jan/Documents/test/Еты-Пуровское'):
        target_dir = '/home/jan/Documents/test/Еты-Пуровское/' + dir + '/ОПИСАНИЕ+ФОТО/'
        if os.path.isdir(target_dir):
            pdfs = [target_dir + f for f in os.listdir(target_dir) if f.find("Рис.") != -1 and f.endswith('.pdf')]
            desc_file = [target_dir + f for f in os.listdir(target_dir) if
                         f.find("Описание") != -1 and f.endswith('.pdf')]
            try:
                for pdf in pdfs:
                    files_proc(desc_file[0], pdf, dir)
            except IndexError:
                continue


def files_proc(descr_pdf, imgs_pdf, dir_n):
    # quite bad decision to pass path instead bytes of already opened file
    pdffile_path = imgs_pdf
    captions, kernt_st = pdfminer_ver2.captinons_handling(pdffile_path)
    imnames = [cap.get('image_name') for cap in captions]  # (for debug)

    imgs = pypdf_implem.img_extract(pdffile_path, 1)

    # filtred_imgs = [img for img in imgs if list(img)[0] in imnames]

    rgb_img, uv_img = concat_all(imgs, captions)  # (for debug)

    cap_descipt = description_handling.find_cap_descr(kernt_st, descr_pdf)
    cutted_imgs_rgb, cutted_imgs_uv = c_n_c(captions, imgs, cap_descipt)
    pdf_name = imgs_pdf.split('/')[-1:][0]
    try:
        os.mkdir('exported/%s/' % dir_n)
        os.mkdir('exported/%s/descriptions/' % dir_n)
        os.mkdir('exported/%s/images/' % dir_n)
    except FileExistsError:
        pass
    try:
        for i, img in enumerate(cutted_imgs_rgb):
            f = open('exported/%s/descriptions/%s_layer_%i.txt' % (dir_n, pdf_name, i), 'w+')
            f.write(cap_descipt[i]['layer description'])
            img.save('exported/%s/images/%s_layer_%i.png' % (dir_n, pdf_name, i))
    except AttributeError :
        print('bad save for %s' % pdf_name)

    print(captions)

    return 0


if __name__ == "__main__":
    main()
