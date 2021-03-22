from django.shortcuts import render
from django.http import JsonResponse
import os
from keras.models import load_model
import numpy as np
from tqdm import tqdm
from annoy import AnnoyIndex
from api_user import response, deepmodel
import logging
from api_user.models import Location
logger = logging.getLogger(__name__)

# cafe similarity measure with InceptionV3 and Annoy Index
def cafe_similarity_measure(request, upload_img_name):
    save_img_path = "C:/cafe-img/dump/"
    upload_img_path = "C:/cafe-img/upload/"
    images = os.listdir(save_img_path)

    files = os.listdir("C:/cafe-img/")
    print(files[0].split("_")[0])

    valid_images = list()
    valid_image_names = list()

    # upload img
    img = deepmodel.fetch_image(upload_img_path, upload_img_name)
    if img:
        valid_images.append(img)
        valid_image_names.append(upload_img_name)

    # save img
    for save_img_name in tqdm(images):
        img = deepmodel.fetch_image(save_img_path, save_img_name)
        if img:
            valid_images.append(img)
            valid_image_names.append(save_img_name)

    # InceptionV3
    model = load_model("C:/deep-learning-cookbook/spotify/test_model.h5")

    # batch size
    chunks = [deepmodel.get_vector(model, valid_images[i:i + 30]) for i in range(0, len(valid_images), 30)]
    vectors = np.concatenate(chunks)
    print(vectors.shape)

    # Annoy Index
    vector_size = 2048
    index = AnnoyIndex(vector_size, 'dot')
    data = list()
    for idx in range(len(vectors)):
        data.append({'idx': idx, 'img': valid_images[idx], 'name': valid_image_names[idx], 'vector': vectors[idx]})
        if idx <= 80:
            index.add_item(idx, vectors[idx])

    index.build(50)
    index.save('C:/rest_api/api_user/cafemodel/cafe_similarity_analysis.annoy')

    # evaluation
    load_index = AnnoyIndex(vector_size, 'dot')
    load_index.load('C:/rest_api/api_user/cafemodel/cafe_similarity_analysis.annoy')

    # nearest vector index list
    result = load_index.get_nns_by_vector(data[0]['vector'], 20)

    locationList = list()
    # for idx, value in enumerate(result):
    #     locationList.append(Location.objects.filter(name=data[result[idx]]['name']).values()[0])

    # test
    locationList.append(Location.objects.filter(name=data[result[1]]['name']).values()[0])

    success = response.success
    success['data'] = locationList
    return JsonResponse(success)

# spring - django request and response test
def testRequest(request):
    # update query
    # data = Location.objects.get(id=1)
    # data.lat = '37.56652'
    # data.long = '126.97796'
    # data.save()
    return JsonResponse(response.success)