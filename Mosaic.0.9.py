# Python version = 2.7.6
# Platform = win32

from PIL import Image
import ImageChops
import math
import operator
import os
import time

from collections import deque


class Mosaic:
    def __init__(self, path):
        self.path = path


class photomosaic(Mosaic):
    def create_mosaic(self, filename, min_size):
        self.filename = filename
        self.min_size = min_size
        self.pictdb = os.listdir(self.path)
        counter = 0
        imc = Image.open(self.filename)
        im = imc.copy()
        self.im = im
        im_width, im_height = im.size
        start_x = 0
        start_y = 0
        self.start_x = start_x
        self.start_y = start_y
        self.im_width = im_width
        self.im_height = im_height
        d = self.pictdb_getdata(self.pictdb, self.path)
        Q = []
        switch = 1
        self.xy = self.quads(self.im_width, self.im_height, self.start_x,
                             self.start_y)
        for i in range(0, 4):
            Q.append(self.xy[i])
        while switch == 1:
            Q = deque(Q)
            qn = Q.popleft()
            self.im_width = qn[2] - qn[0]
            self.im_height = qn[3] - qn[1]
            self.start_x = qn[0]
            self.start_y = qn[1]
            xy = self.quads(self.im_width, self.im_height, self.start_x,
                            self.start_y)
            if (xy[0][2] - xy[0][0]) < self.min_size or (
                    xy[0][3] - xy[0][1]) < self.min_size:
                for i in range(0, 4):
                    img = im.crop((xy[i][0], xy[i][1], xy[i][2], xy[i][3]))
                    match = self.find_match(img, d)
                    resize_pic = os.path.join(self.path, match)
                    resize_pic = Image.open(resize_pic)
                    resize_pic_width = xy[i][2] - xy[i][0]
                    resize_pic_height = xy[i][3] - xy[i][1]
                    paste_pic = self.resize_picture(
                        resize_pic, resize_pic_width, resize_pic_height)
                    im.paste(paste_pic, (xy[i][0], xy[i][1]))
                    counter += 1
                    if counter == 5:
                        pass
            else:
                for i in range(0, 4):
                    Q.append(xy[i])
            if len(Q) == 0:
                switch = 0
        return self.im

    def quads(self, im_width, im_height, start_x, start_y):
        """Divides the original picture into quadrants"""
        self.quad_1 = (self.start_x, self.start_y, self.start_x + self.im_width / 2, \
                           self.start_y + self.im_height / 2)
        self.quad_2 = (self.start_x + self.im_width / 2, self.start_y, \
                           self.start_x + self.im_width, self.start_y + self.im_height / 2)
        self.quad_3 = (self.start_x, self.start_y + self.im_height / 2, \
                           self.start_x + self.im_width / 2, self.start_y + self.im_height)
        self.quad_4 = (self.start_x + self.im_width / 2, self.start_y + self.im_height / 2, \
                           self.start_x + self.im_width, self.start_y + self.im_height)
        return self.quad_1, self.quad_2, self.quad_3, self.quad_4

    def pictdb_getdata(self, pictdb, dirname):
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

    def find_match(self, img, d):

        pictdb = os.listdir(self.path)
        color_value = self.img_getdata(img)
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
            print "Error Message"

    def img_getdata(self, img):
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

    def rmsdiff(im1, im2):
        "Calculate the root-mean-square difference between two images"

        h = ImageChops.difference(im1, im2).histogram()

        # calculate rms
        return math.sqrt(reduce(operator.add,
                                map(lambda h, i: h * (i**2), h, range(256))) /
                         (float(im1.size[0]) * im1.size[1]))

    def resize_picture(self, resize_pic, resize_pic_width, resize_pic_height):
        """Resizes the picture database picture to the size of the
        cropped quadrant picture, and returns as value 'out'"""
        out = resize_pic.resize((resize_pic_width, resize_pic_height))
        return out

    def save_as(self):
        self.im.save("C:\\Users\\GREG\\Desktop\\Sandbox\\photomosaic\\" +
                     'im_Greg1.jpg',
                     quality=100)


start_time = time.clock()
p1 = photomosaic('C:\\Users\\GREG\\Desktop\\Sandbox\\photomosaic\\Flowers')
p1.create_mosaic("C:\\Users\GREG\Desktop\Sandbox\photomosaic\IMG_0929.jpg", 10)
p1.save_as()
run_time = time.clock() - start_time
print "Run time = ", run_time
