import requests
from urllib.parse import urlparse, quote_plus
from urllib.request import urlopen
from selenium import webdriver
import sys
import io
from api_user.models import CafeV1

# latitude, y, col
def address_to_latitude(address):
    global lat
    url = 'http://dapi.kakao.com/v2/local/search/address.json?query='+address
    result = requests.get(urlparse(url).geturl(), headers={"Authorization": "KakaoAK ebce0523c9fd17c096d7ee242a4f3626"})
    json_obj = result.json()
    for document in json_obj['documents']:
        lat = document['y']
        print(lat)
    return lat

# longitude, x, row
def address_to_longtitude(address):
    global long
    url = 'http://dapi.kakao.com/v2/local/search/address.json?query='+address
    result = requests.get(urlparse(url).geturl(), headers={"Authorization": "KakaoAK ebce0523c9fd17c096d7ee242a4f3626"})
    json_obj = result.json()
    for document in json_obj['documents']:
        long = document['x']
        print(long)
    return long

# crawling 3 cafe images by chrome
def cafe_img_search_by_chrome():

    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding="utf-8")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome("C:/chromedriver_win32/chromedriver.exe", chrome_options=chrome_options)

    save_path = "C:/cafe-img/compare/"

    # keyword = cafe name from models
    cafe_list = CafeV1.objects.all()
    cafe_name_list = list()
    for cafe in cafe_list:
        if cafe is not None:
            print()
            print(cafe.name)
            print()
            cafe_name_list.append(cafe.name)

    # search
    for cafe_name in cafe_name_list:
        search_keyword = cafe_name + " 인테리어"
        print("search_keyword : {}".format(search_keyword))
        print()

        url = f"https://www.google.com/search?q={quote_plus(search_keyword)}&sxsrf=ALeKk01n9CbhJFSTR5dLoacGQlXGMfTBTg:1593337667405&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjY0rCtnaTqAhWUQN4KHcV3B5oQ_AUoAnoECA4QBA&biw=1920&bih=987"
        driver.implicitly_wait(4)
        driver.get(url)

        image_list = driver.find_elements_by_tag_name("img.rg_i.Q4LuWd")

        # save 3 images every keywords
        for index, image in enumerate(image_list):
            if index > 3:
                break

            # original image
            webdriver.ActionChains(driver).move_to_element(image).click(image).perform()
            html_objects = driver.find_element_by_tag_name('img.n3VNCb')
            image_src_value = html_objects.get_attribute('src')
            current_image = urlopen(image_src_value).read()

            # save image
            file_name = cafe_name + "_" + str(index + 1)
            print("file_name : {}".format(file_name))
            print()
            file = open(save_path + file_name + '.jpg', 'wb')
            file.write(current_image)