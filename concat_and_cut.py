import PIL
from PIL import Image
import numpy as np

'''Calc pixel/meter ratios for every image '''


# pixel per meter
def mesure_m(captions):
    coeff = lambda sz1, sz: (sz1[1] / sz[1])  # resize coeff for Y coordinate
    pdf_src_ratio = []
    ruler_cap = captions[0]
    for img_cap in captions:
        try:
            if img_cap['is_ruler']:
                ruler_cap = img_cap
                continue
            else:
                ratio = coeff(img_cap.get('src_size'), img_cap.get('in_pdf_size')) * ruler_cap.get('in_pdf_size')[1]
                pdf_src_ratio.append({img_cap.get('image_name'): ratio})
                img_cap.update({'ratio': ratio})
        except:  # bare except I know
            pass
    return pdf_src_ratio
    # print(pdf_src_ratio)


'''Concatenate all images based on their top an bottom description'''


def concat_all(imgs, captions):
    rgb_imgs = [cap.get('image_name') for cap in captions if
                (cap.get('is_ruler') is False and cap.get('is_uv') is False)]

    uv_imgs = [cap.get('image_name') for cap in captions if
               (cap.get('is_ruler') is False and cap.get('is_uv') is True)]

    # TODO remove lists
    concated_rgb = rs_concat([imgs[name] for name in rgb_imgs])

    concated_uv = rs_concat([imgs[name] for name in uv_imgs])

    return concated_rgb, concated_uv


'''Width! resize and concatenate images'''


def rs_concat(imgs):
    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
    imgs_comb = np.vstack((np.asarray(i.resize((min_shape[0], i.height))) for i in imgs))
    return Image.fromarray(imgs_comb)


'''Just cut this damn image'''


def cut_func(img, top_b, bot_b):
    return img.crop((0, top_b, img.width, bot_b))


'''Cut image according meters'''


def cut_all(captions, img, cuts, rgb=True):
    # For detecting when we go to new image. It's for changin ppm coefficient
    if rgb:
        heights = [cap['src_size'][1] for cap in captions if (not cap['is_ruler'] and not cap['is_uv'])]
        imgs_caps = [cap for cap in captions if (not cap['is_ruler'] and not cap['is_uv'])]

        i = 0
        start = 0
        for cap in captions:  # parts of image in in concated big image
            if not cap['is_ruler'] and not cap['is_uv']:
                cap.update({'boundaries': (start, start + heights[i])})
                start += heights[i]
                i += 1
    else:
        heights = [cap['src_size'][1] for cap in captions if (not cap['is_ruler'] and cap['is_uv'])]
        imgs_caps = [cap for cap in captions if (not cap['is_ruler'] and cap['is_uv'])]

        i = 0
        start = 0
        for cap in captions:  # parts of image in in concated big image
            if not cap['is_ruler'] and cap['is_uv']:
                cap.update({'boundaries': (start, start + heights[i])})
                start += heights[i]
                i += 1

    # the magic begins
    top_cut = 0
    img_cnt = 0
    imgs = []
    for cut in cuts:
        if top_cut + cut * imgs_caps[img_cnt]['ratio'] < imgs_caps[img_cnt]['boundaries'][1]:
            bot_cut = top_cut + cut * imgs_caps[img_cnt]['ratio']
            cutted_img = cut_func(img, top_cut, bot_cut)
            top_cut = bot_cut
            imgs.append(cutted_img)
        else:
            bot_cut = imgs_caps[img_cnt]['boundaries'][1]
            fst_cutted_img = cut_func(img, top_cut, bot_cut)
            snd_cut = cut - (bot_cut - top_cut) / imgs_caps[img_cnt]['ratio']  # must be in meters

            img_cnt += 1
            top_cut = imgs_caps[img_cnt]['boundaries'][0]
            bot_cut = top_cut + snd_cut * imgs_caps[img_cnt]['ratio']
            snd_cutted_img = cut_func(img, top_cut, bot_cut)

            cutted_img = rs_concat((fst_cutted_img, snd_cutted_img))
            imgs.append(cutted_img)

    return imgs

    ###

    # img_borders =
    # ratios = mesure_m(captions)
    # for cut in cuts:


def c_n_c(captions, imgs, capdescr):  # concatinate and cut then
    mesure_m(captions)
    cuts = [float(layer['layer length'].replace(',', '.')) for layer in capdescr]
    rgb_cnt, uv_cnt = concat_all(imgs, captions)  # concated images
    cutted_rgb_cnt = cut_all(captions, rgb_cnt, cuts, True)
    cutted_uv_cnt = cut_all(captions, uv_cnt, cuts, False)
    return cutted_rgb_cnt, cutted_uv_cnt
