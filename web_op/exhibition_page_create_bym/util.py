from PIL import Image


def merge_dict(dict1, dict2):
    return dict1.update(dict2)


def resize_img(img_path, img_size_tpl=(700, 700)):
    img = Image.open(img_path)

    img_resize = img.resize(img_size_tpl)
    img_resize.save(img_path)


def convert_rgb(img_path):
    Image.open(img_path).convert('RGB').save(img_path)