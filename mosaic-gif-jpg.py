# Python version = 2.7.10
# Platform = win32

from __future__ import print_function

from PIL import Image
import math
import operator
import os
import time

from collections import deque

import test


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


def compare(img, x):
    """Inactive Function"""
    image2 = Image.open(x)
    h1 = img.histogram()
    h2 = image2.histogram()
    rms = math.sqrt(reduce(operator.add,
                           map(lambda a, b: (a - b)**2, h1, h2)) / len(h1))
    return rms


def compare_color(img):
    """Innactive Function"""
    dirname = 'tiles'
    pictdb = os.listdir(dirname)
    counter = 0
    for i in pictdb:
        x = os.path.join('dali', i)
        td = compare(img, x)
        counter += 1
        if counter == 1:
            place_holder = td
        if td < place_holder:
            place_holder = td
            pdb = i


def copy_picture():
    pass


def resize_picture(resize_pic, resize_pic_width, resize_pic_height):
    """Resizes the picture database picture to the size of the
    cropped quadrant picture, and returns as value 'out'"""
    out = resize_pic.resize((resize_pic_width, resize_pic_height))
    return out


def find_match(img, d):
    dirname = 'tiles'
    pictdb = os.listdir(dirname)
    color_value = img_getdata(img)
    closest_match = 1000000
    red_match = 10000000
    green_match = 10000000
    blue_match = 10000000
    for key, value in d.items():
        ismatch_red = abs(value[0] - color_value[0])
        if ismatch_red < red_match:
            red_match = ismatch_red
            match_key_red = key
        ismatch_green = abs(value[1] - color_value[1])
        if ismatch_green < green_match:
            green_match = ismatch_green
            match_key_green = key
        ismatch_blue = abs(value[2] - color_value[2])
        if ismatch_blue < blue_match:
            blue_match = ismatch_blue
            match_key_blue = key
    if red_match <= green_match and red_match <= blue_match:
        return pictdb[match_key_red - 1]
    elif green_match <= red_match and green_match <= blue_match:
        return pictdb[match_key_green - 1]
    elif blue_match <= red_match and blue_match <= green_match:
        return pictdb[match_key_blue - 1]
    else:
        pass


def img_getdata(img):
    """Returns a 3-length tuple of the average Red, Green and Blue
    color values"""
    img = img.getdata()
    red_counter = 0
    green_counter = 0
    blue_counter = 0
    for rgb in img:
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]
        red_counter += red
        green_counter += green
        blue_counter += blue
    red_average = red_counter / len(img)
    green_average = green_counter / len(img)
    blue_average = blue_counter / len(img)
    color_value = (red_average, green_average, blue_average)
    return color_value


def pictdb_getdata(pictdb, dirname):
    """Creates a dictionary entry for each picture in the picture database.
    The key will be the counter, the value will be the Red, Green, and Blue
    averages as a 3-length tuple. Returns the dictionary 'd'"""
    d = {}
    counter = 0
    for i in pictdb:
        dbpic = os.path.join(dirname, i)
        dbpic = Image.open(dbpic)
        dbpic = dbpic.getdata()
        counter += 1
        red_counter = 0
        green_counter = 0
        blue_counter = 0
        for rgb in dbpic:
            convert_jpg(rgb)
            print ("rgb = ", rgb)
            red = rgb[0]
            green = rgb[1]
            blue = rgb[2]
            red_counter += red
            green_counter += green
            blue_counter += blue
        red_average = red_counter / len(dbpic)
        green_average = green_counter / len(dbpic)
        blue_average = blue_counter / len(dbpic)
        color_value = (red_average, green_average, blue_average)
        d[counter] = color_value
    return d

#########################################################################################

def convert_jpg(infile):
    str(infile)
    #for infile in sys.argv[1:]:
    f, e = os.path.splitext(infile)
    outfile = f + ".jpg"
    if infile != outfile:
        try:
            Image.open(infile).save(outfile)
        except IOError:
            print("cannot convert", infile)
    return outfile

#########################################################################################

def create_mosaic(filename, min_size):
    """Creates the mosaic"""
    dirname = 'tiles'
    pictdb = os.listdir(dirname)
    counter = 0
    imc = Image.open(filename)
    im = imc.copy()
    im_width, im_height = im.size
    start_x = 0
    start_y = 0
    d = pictdb_getdata(pictdb, dirname)
    Q = []
    switch = 1
    xy = quads(im_width, im_height, start_x, start_y)
    for i in range(0, 4):
        Q.append(xy[i])
    while switch == 1:
        Q = deque(Q)
        qn = Q.popleft()
        im_width = qn[2] - qn[0]
        im_height = qn[3] - qn[1]
        start_x = qn[0]
        start_y = qn[1]
        a = start_x + im_width
        b = start_y + im_height
        xy = quads(im_width, im_height, start_x, start_y)
        if (xy[0][2] - xy[0][0]) < min_size or (xy[0][3] - xy[0][1]) < min_size:
            for i in range(0, 4):
                #print xy[i]
                img = im.crop((xy[i][0], xy[i][1], xy[i][2], xy[i][3]))
                match = find_match(img, d)
                resize_pic = os.path.join(dirname, match)
                resize_pic = Image.open(resize_pic)
                resize_pic_width = xy[i][2] - xy[i][0]
                resize_pic_height = xy[i][3] - xy[i][1]
                paste_pic = resize_picture(resize_pic, resize_pic_width,
                                           resize_pic_height)
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
    im.save(outdir + 'test.jpg', quality=100)


def main():
    """Main Program"""
    start_time = time.clock()
    outdir = 'output-photos/'
    filename = "input-photos/karan.jpg"
    min_size = 10
    im = create_mosaic(filename, min_size)
    save_as(im, outdir)
    run_time = time.clock() - start_time
    print ("Run time = ", run_time)


if __name__ == '__main__':
    main()
