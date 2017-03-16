import argparse
import os

from PIL import Image

def modify_image(image):
    #Read image
    im = Image.open(image).convert("RGBA")
    #Display image
    # im.show()

    for k in range(2, 358, 50):
        im_rotate = im.rotate(k, expand = True)
        im_rotate_name = "out"+os.sep+image[:image.rindex('.')]+"_rotated_"+k.__str__()+".gif"
        # transparency = im_rotate.info['transparency']
        im_rotate.save(im_rotate_name) #, transparency = transparency)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", required=True, help="Директория поиска изображений")
    args = vars(ap.parse_args())

    directory = args["dir"]
    #Получаем список файлов в переменную files
    files = os.listdir(directory)
    #Фильтруем список
    images = filter(lambda x: x.endswith('.jpg' or '.gif'), files)

    for i in images:
        print(i)
        modify_image(directory+os.sep+i)
