from PIL import Image
import numpy as np
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing import image

def center_crop_resize(img, new_size):
    w, h = img.size
    s = min(w, h)
    y = (h - s) // 2
    x = (w - s) // 2
    img = img.crop((x, y, s, s))
    return img.resize((new_size, new_size))

def fetch_image(img_path, img_name):
    try:
        img = Image.open(img_path + img_name)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        return center_crop_resize(img, 299)
    except IOError:
        pass
    return None

def get_vector(model, img):
    if not type(img) == list:
        images = [img]
    else:
        images = img
    target_size = int(max(model.input.shape[1:]))
    images = [img.resize((target_size, target_size), Image.ANTIALIAS) for img in images]
    np_imgs = [image.img_to_array(img) for img in images]
    pre_processed = preprocess_input(np.asarray(np_imgs))
    print(pre_processed.shape)
    return model.predict(pre_processed)