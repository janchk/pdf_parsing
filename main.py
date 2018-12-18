import pypdf_implem
import pdfminer_ver2
import description_handling
from concat_and_cut import concat_all, c_n_c


def main():
    # quite bad decision to pass path instead bytes of already opened file
    pdffile_path = "/home/jan/Documents/test/Еты-Пуровское/260по/ОПИСАНИЕ+ФОТО/Рис._2.2.7-2.2.10_Еты-Пуровское_260.pdf"
    captions, kernt_st = pdfminer_ver2.captinons_handling(pdffile_path)
    imnames = [cap.get('image_name') for cap in captions]  # (for debug)

    imgs = pypdf_implem.img_extract(pdffile_path, 1)

    # filtred_imgs = [img for img in imgs if list(img)[0] in imnames]

    rgb_img, uv_img = concat_all(imgs, captions)  # (for debug)

    cap_descipt = description_handling.find_cap_descr(kernt_st)
    cutted_imgs_rgb, cutted_imgs_uv = c_n_c(captions, imgs, cap_descipt)

    for i, img in enumerate(cutted_imgs_rgb):
        f = open('exported/descriptions/layer_%i.txt' % i, 'w+')
        f.write(cap_descipt[i]['layer description'])
        img.save('exported/images/layer_%i.png' % i)

    print(captions)

    return 0


if __name__ == "__main__":
    main()
