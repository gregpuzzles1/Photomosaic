# Python version = 2.7.2
# Platform = win32

from PIL import Image
from PIL import ImageChops
import math
import operator
import os
import time

from collections import deque

def quads(im_width, im_height, start_x, start_y):
    """Divides the original picture into quadrants"""    
    quad_1 = (start_x, start_y, start_x + im_width / 2, \
                       start_y + im_height / 2)
    quad_2 = (start_x + im_width / 2, start_y, \
                       start_x + im_width, start_y + im_height / 2)
    quad_3 = (start_x, start_y + im_height / 2, \
                       start_x + im_width / 2, start_y + im_height)
    quad_4 = (start_x + im_width / 2, start_y + im_height / 2, \
                       start_x + im_width, start_y + im_height)
    return quad_1, quad_2, quad_3, quad_4

def resize_picture(resize_pic, resize_pic_width, resize_pic_height):
    """Resizes the picture database - picture to the size of the
    cropped quadrant picture, and returns as value 'out'"""    
    out = resize_pic.resize((resize_pic_width, resize_pic_height))
    return out

def rmsdiff(im, dbpic):
    "Calculate the root-mean-square difference between two images"

    diff = ImageChops.difference(im, dbpic)
    h = diff.histogram()
    sq = (value*(idx**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares/float(im.size[0] * im.size[1]))

    return rms

def FindClosestMatch(im, d):

    dirname = 'C:\\photomosaic\\dali&Flowers'
    pictdb = os.listdir(dirname)

    placeholder = 1000
    for item, value in d.iteritems():
        x = rmsdiff(im, value)
        if x < placeholder:
            placeholder = x
            zzz = value
            xyz = item
        else: 
            continue
    return xyz

def createDBdictionary():
    dirname = 'C:\\photomosaic\\dali&Flowers'
    pictdb = os.listdir(dirname)
    d = {}
    counter = 0 
    for i in pictdb:
        dbpic = os.path.join(dirname, i)
        dbpic = Image.open(dbpic)
        d[counter] = dbpic
        counter += 1
    return d
        
def create_mosaic(filename, min_size):
    """Creates the mosaic"""    
    dirname = 'C:\\photomosaic\\dali&Flowers'
    pictdb = os.listdir(dirname)        
    counter = 0
    imc = Image.open(filename)
    im = imc.copy()
    im_width, im_height = im.size
    start_x = 0
    start_y = 0

    QL1 = []

    for i in pictdb:
        dbpic = os.path.join(dirname, i)
        QL1.append(dbpic)

    hth = createDBdictionary()

    Q = []
    switch = 1
    xy = quads(im_width, im_height, start_x, start_y)
    for i in range(0,4):
        Q.append(xy[i])
    while switch == 1:
        Q = deque(Q)
        qn = Q.popleft()
        im_width = qn[2] - qn[0]
        im_height = qn[3] - qn[1]
        start_x = qn[0]
        start_y = qn[1]
        xy = quads(im_width, im_height, start_x, start_y)
        if (xy[0][2] - xy[0][0]) < min_size or (xy[0][3] - xy[0][1]) < min_size:
             for i in range(0, 4):
                 img = im.crop((xy[i][0], xy[i][1], xy[i][2], xy[i][3]))
                 match = FindClosestMatch(img, hth)
                 ext = QL1[match]
                 resize_pic = os.path.join(dirname, ext)
                 resize_pic = Image.open(resize_pic)
                 resize_pic_width = xy[i][2] - xy[i][0]
                 resize_pic_height = xy[i][3] - xy[i][1]
                 paste_pic = resize_picture(resize_pic, resize_pic_width, resize_pic_height)
                 im.paste(paste_pic, (xy[i][0], xy[i][1]))
                 counter += 1
                 if counter == 5:
                     pass
        else:
             for i in range(0, 4):
                 Q.append(xy[i])
        if len(Q) == 0:
                switch = 0
    return im            

def save_as(im, outdir):
    """Save the mosaic as im.jpg in the outdir directory"""    
    im.save(outdir + 'TESTim.jpg', quality = 100)
    print "Created output photo in working directory."

def main():
    """Main Program"""    
    start_time = time.clock()

    outdir = 'C:\\photomosaic\\'
    filename = "C:\\photomosaic\karan.jpg"
    min_size = 20
    im = create_mosaic(filename, min_size)
    save_as(im, outdir)

    run_time = time.clock() - start_time
    print "Run time = ", run_time

if __name__ == '__main__':
    main()

    
