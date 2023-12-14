from PIL import Image
import argparse
import os
import re

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--img", help="path to the input image")
ap.add_argument("-d", "--dir", help="path to the image files")
ap.add_argument("-r", "--res", default=300, type=int, help="resolution of thumb, default = 300")
ap.add_argument("-b", "--bak", help="path to backup original alpha-chanel jpg")
args = vars(ap.parse_args())

def file_proc(dir,filename,res,bak):
    im = Image.open(dir+filename).convert('RGBA')
    im.getbbox()
    im_c = im.crop(im.getbbox())
    im_c.save(dir+filename.rsplit(".", 1)[0]+"_crop.png")
    im_c.thumbnail((res,res))
    im_c.save(dir+filename.rsplit(".", 1)[0]+"_thumb.png")
    im_c.load() # required for png.split()
    im_c_j = Image.new("RGB", im_c.size, (255, 255, 255))
    im_c_j.paste(im_c, mask=im_c.split()[3]) # 3 is the alpha channel
    im_c_j.save(dir+filename.rsplit(".", 1)[0]+"_thumb.jpg")
    os.replace(dir+filename, bak+filename)



if args["img"]:
    dir = args["img"].rsplit("\\", 1)[0]+"\\"
    res = args["res"]
    if args["bak"]:
        bak = args["bak"]
    else:
        bak = dir
    if os.path.exists(bak):
        if os.path.isdir(bak):
            print("Папка уже существует")
    else:
        os.mkdir(bak)
    filename = args["img"].split("\\", )[-1]
    file_proc(dir, filename, res, bak)


if args["dir"]:
    dir = args["dir"]
    if dir[-1] != "\\":
        dir=dir+"\\"
    res = args["res"]
    if args["bak"]:
        bak = args["bak"]
    else:
        bak = dir
    if os.path.exists(bak):
        if os.path.isdir(bak):
            print("Папка , бекапа уже существует")
    else:
        os.mkdir(bak)
    tpl = '^\d{1,}.jpg$'
    files = os.listdir(dir)
    print(dir)
    for f in files:
        if os.path.isfile(os.path.join(dir,f)):
            if re.match(tpl, f) is not None:
                print("Файл " + f + " подходит. Обрабатываем:")
                filename = f
                file_proc(dir, filename, res, bak)
            else:
                print("Файл " + f + " не подходит. Пропускаем")
