import argparse
import os

from PIL import Image

def modify_image(directory, image):
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
        # новое имя файла в директории для результатов = изначальное-имя_rotated_угол-вращения.изначальное-расширение
        im_rotate_name =  output_directory + os.sep +image[:image.rindex('.')]+"_rotated_"+k.__str__()+image[image.rindex('.'):]    # ".jpg"
        # transparency = im_rotate.info['transparency']
        im_rotate.save(im_rotate_name) #, transparency = transparency)

# входная точка приложения
if __name__ == "__main__":
    # задаются параметры приложения
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", required=True, help="Директория поиска изображений")
    args = vars(ap.parse_args())

    # получение значения параметра "Директория поиска изображений"
    directory = args["dir"]
    #Получаем список файлов в переменную files
    files = os.listdir(directory)
    #Фильтруем список
    images = filter(lambda x: x.endswith('.jpg' or '.gif'), files)

    # запуск обработки каждого из изображений
    for image in images:
        print(image)
        modify_image(directory, image)
