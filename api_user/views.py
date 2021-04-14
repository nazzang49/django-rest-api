from django.shortcuts import render
from django.http import JsonResponse
from tqdm import tqdm
from annoy import AnnoyIndex
from keras.models import load_model
from api_user import response, deepmodel, util, sql
from api_user.models import Location, CafeV1
from selenium import webdriver
import os
import numpy as np
import logging
import datetime
import time
import pandas as pd
logger = logging.getLogger(__name__)

# cafe similarity measure with InceptionV3 and Annoy Index
def cafe_similarity_measure(request, upload_img_name):

    print("학습 시작 : ", datetime.datetime.now())
    print("upload_img_name : {}".format(upload_img_name))
    print()

    saving_path = "C:/cafe-img/compare/"
    upload_path = "C:/cafe-img/upload/"
    image_list = os.listdir(saving_path)

    valid_image_list = list()
    valid_image_name_list = list()

    # upload
    img = deepmodel.fetch_image(upload_path, upload_img_name)
    if img:
        valid_image_list.append(img)
        valid_image_name_list.append(str(upload_img_name).split('_')[0])

    # saving
    for saving_img_name in tqdm(image_list):
        img = deepmodel.fetch_image(saving_path, saving_img_name)
        if img:
            valid_image_list.append(img)
            valid_image_name_list.append(str(saving_img_name).split('_')[0])

    # inception v3
    model = load_model("C:/deep-learning-cookbook/spotify/test_model.h5")

    # batch size
    chunks = [deepmodel.get_vector(model, valid_image_list[i:i + 10]) for i in range(0, len(valid_image_list), 10)]
    vectors = np.concatenate(chunks)
    print("vector shape : ")
    print(vectors.shape)
    print()

    # annoy
    vector_size = 2048
    index = AnnoyIndex(vector_size, 'dot')
    data = list()
    for idx in range(len(vectors)):
        data.append({'idx': idx, 'img': valid_image_list[idx], 'name': valid_image_name_list[idx], 'vector': vectors[idx]})
        if idx <= 80:
            index.add_item(idx, vectors[idx])

    # index result
    index.build(50)
    index.save('C:/rest_api/api_user/cafemodel/cafe_similarity_analysis.annoy')

    # evaluation
    load_index = AnnoyIndex(vector_size, 'dot')
    load_index.load('C:/rest_api/api_user/cafemodel/cafe_similarity_analysis.annoy')

    # 30-nearest vector list on 0-index vector
    result = load_index.get_nns_by_vector(data[0]['vector'], 30)

    cafe_list = list()
    for idx, value in enumerate(result):
        print("카페 검색 결과 : {}".format(data[result[idx]]['name']))
        cafe_list.append(CafeV1.objects.filter(name=data[result[idx]]['name']).values()[0])

    print("학습 종료 : ", datetime.datetime.now())

    success = response.success
    success['data'] = cafe_list
    return JsonResponse(success)

# crawling
def test_request(request):
    util.cafe_img_search_by_chrome()
    # update query
    # data = Location.objects.get(id=1)
    # data.lat = '37.56652'
    # data.long = '126.97796'
    # data.save()

    # select query with distinct
    # data = Location.objects.distinct('id')
    return JsonResponse(response.success)

def call_kakao_map(request):
    # chrome options => without opening chrome browser
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome("C:/chromedriver_win32/chromedriver.exe", chrome_options=chrome_options)

    # mobile map
    seoul_list = pd.read_table("C:/rest_api/api_user/etc/seoul.txt", sep="\t")
    print(seoul_list.info())
    print(seoul_list.describe())
    seoul_list = seoul_list.drop([0, 1])
    seoul_list = seoul_list.drop(seoul_list[seoul_list['동'] == '소계'].index)
    print(seoul_list['동'])

    # to list
    region_list = seoul_list['동'].tolist()
    print(region_list)

    results = []
    for idx, region in enumerate(region_list):
        if idx > 0:
            break
        # mobile map
        url = "https://m.map.naver.com/"
        driver.get(url)
        driver.implicitly_wait(5)

        # search by keyword
        driver.find_element_by_class_name('Nbox_input_text').clear()
        driver.find_element_by_class_name('Nbox_input_text').click()

        driver.find_element_by_class_name('Nbox_input_text._search_input').send_keys(region + "카페")
        driver.find_element_by_xpath('//*[@id="ct"]/div[1]/div[1]/form/div/div[2]/div/span[2]/button[2]').click()
        time.sleep(4)

        # result
        search_list = driver.find_elements_by_xpath('//*[@id="ct"]/div[2]/ul/li')
        print(len(search_list))

        for index, data in enumerate(search_list):
            # cafe name
            name = data.find_element_by_css_selector('div.item_tit').text
            # cafe address
            address = data.find_element_by_css_selector('div.wrap_item').text.split('\n')[1]

            print()
            print("============== ", region, " 카페 검색 결과 : ", index, " ==============")
            print(name)
            print(data.find_element_by_css_selector('div.wrap_item').text.split('\n')[0])
            print(data.find_element_by_css_selector('div.wrap_item').text.split('\n')[1])
            print()

            # cafe position through kakao map api
            latitude = util.address_to_latitude(address)
            print(", ")
            longitude = util.address_to_longtitude(address)
            results.append((name, address, latitude, longitude))

    # create objects of CafeV1 model
    for o in results:
        CafeV1.objects.create(name=o[0], address=o[1], lat=o[2], long=o[3])
    print(CafeV1.objects.all().count())

    success = response.success
    success['data'] = results
    # for korean
    false_flag = {'ensure_ascii': False}
    return JsonResponse(success, json_dumps_params=false_flag)