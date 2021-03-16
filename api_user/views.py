from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os
from keras.models import load_model
import numpy as np
from tqdm import tqdm
from annoy import AnnoyIndex
from api_user import deepmodel
import logging
from api_user.models import Location
logger = logging.getLogger(__name__)

def test(request, upload_img_name):
    apiGetResult = Location.objects.filter(name=upload_img_name).values()

    # save_img_path = "C:/cafe-img/dump/"
    # upload_img_path = "C:/cafe-img/upload/"
    # images = os.listdir(save_img_path)
    #
    # files = os.listdir("C:/cafe-img/")
    # print(files[0].split("_")[0])
    #
    # valid_images = []
    # valid_image_names = []
    #
    # # upload img
    # img = deepmodel.fetch_image(upload_img_path, upload_img_name)
    # if img:
    #     valid_images.append(img)
    #     valid_image_names.append(upload_img_name)
    #
    # # save img
    # for save_img_name in tqdm(images):
    #     img = deepmodel.fetch_image(save_img_path, save_img_name)
    #     if img:
    #         valid_images.append(img)
    #         valid_image_names.append(save_img_name)
    #
    # model = load_model("C:/deep-learning-cookbook/spotify/test_model.h5")
    #
    # # batch size
    # chunks = [deepmodel.get_vector(model, valid_images[i:i + 30]) for i in range(0, len(valid_images), 30)]
    # vectors = np.concatenate(chunks)
    # print(vectors.shape)
    #
    # # annoy
    # vector_size = 2048
    # index = AnnoyIndex(vector_size, 'dot')
    # data = []
    # for idx in range(len(vectors)):
    #     data.append({'idx': idx, 'img': valid_images[idx], 'name': valid_image_names[idx], 'vector': vectors[idx]})
    #     if idx <= 80:
    #         index.add_item(idx, vectors[idx])
    #
    # index.build(50)
    # index.save('C:/rest_api/api_user/cafemodel/cafe_similarity_analysis.annoy')
    #
    # # evaluation
    # load_index = AnnoyIndex(vector_size, 'dot')
    # load_index.load('C:/rest_api/api_user/cafemodel/cafe_similarity_analysis.annoy')
    # result = load_index.get_nns_by_vector(data[0]['vector'], 20)
    #
    # for idx in result:
    #     print(data[idx]['name'])

    return JsonResponse({
        'data': apiGetResult[0]
    }, json_dumps_params={'ensure_ascii': True})