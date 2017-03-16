import random

import argparse
import os
import numpy as np


from PIL import Image

def get_noise_image(width, height):
    imarray = np.random.rand(height, width, 3) * 255
    im = Image.fromarray(imarray.astype('uint8')).convert('RGBA')
    return im

def modify_image(directory, image, isNoiseFill):
    filled = ""
    img_path = directory+os.sep+image;
    # Директория для результатов
    output_directory = directory + os.sep + "out"
    # Если такой директории нет - создание
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    # Чтение изображения
    im = Image.open(img_path).convert("RGBA")

    # Вращение изображения от 2 до 358 градусов с шагом 2(50)
    for k in range(2, 358, 50):
        im_rotate = im.rotate(k, expand = True)
        # Если необходимо добавить шум
        if(isNoiseFill):
            # Генерация фона (шума) под размер изображения
            img_noise = get_noise_image(im_rotate.width, im_rotate.height)
            # Слияние изображений
            im_rotate = Image.composite(im_rotate, img_noise, im_rotate)
            filled = "_filled"
        # новое имя файла в директории для результатов = изначальное-имя_rotated_угол-вращения.изначальное-расширение
        im_rotate_name =  output_directory + os.sep +image[:image.rindex('.')]+"_rotated_"+k.__str__()+filled+image[image.rindex('.'):]
        # transparency = im_rotate.info['transparency']
        im_rotate.save(im_rotate_name) #, transparency = transparency)
        # print("++"+im_rotate.width.__str__()+":"+im_rotate.height.__str__())

# входная точка приложения
if __name__ == "__main__":
    # задаются параметры приложения
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", required=True, help="Директория поиска изображений")
    ap.add_argument("-n", "--noise", required=False, help="Добавление шума: 1 - добавлять шум к изображению при вращении; пустая строка "" - не добавлять")
    args = vars(ap.parse_args())

    # получение значения параметра "Директория поиска изображений"
    directory = args["dir"]
    # получение значения параметра "Добавление шума"
    noise = args["noise"]
    if noise == None: noise = ""
    #Получаем список файлов в переменную files
    files = os.listdir(directory)
    #Фильтруем список
    images = filter(lambda x: x.endswith('.jpg' or '.gif'), files)

    print("Начало обработки в директории: "+ directory + ", генерация шума: " + noise)
    # запуск обработки каждого из изображений
    for image in images:
        print(image)
        modify_image(directory, image, noise)

    # get_noise_image(100, 100).show()
