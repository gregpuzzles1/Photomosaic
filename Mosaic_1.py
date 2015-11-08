# Python version = 2.7.6
# Platform = win32
# Testing git

from PIL import Image
from PIL import ImageChops
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

        #target = 0
        target_1 = 0
        self.target_1 = target_1
        large_rms = 10000
        self.large_rms = large_rms
        resize_pic = "null"

        
        #d = self.pictdb_getdata(self.pictdb, self.path)
        Q = []
        switch = 1
        self.xy = self.quads(self.im_width, self.im_height, self.start_x, self.start_y)
        for i in range(0,4):
            Q.append(self.xy[i])
        while switch == 1:
            Q = deque(Q)
            qn = Q.popleft()
            self.im_width = qn[2] - qn[0]
            self.im_height = qn[3] - qn[1]
            self.start_x = qn[0]
            self.start_y = qn[1]
            xy = self.quads(self.im_width, self.im_height, self.start_x, self.start_y)
            if (xy[0][2] - xy[0][0]) < self.min_size or (xy[0][3] - xy[0][1]) < self.min_size:
                 for i in range(0, 4):
                     img = im.crop((xy[i][0], xy[i][1], xy[i][2], xy[i][3]))
                     #match = self.find_match(img, d)
                     #print "img = ", img

                     for self.ii in self.pictdb:

                        #print "i= ", self.ii
                        #print "img = ", img
                        
                        #dbpic = os.path.join(dirname, i)
                        dbpic = os.path.join('C:\\photomosaic\\dali', self.ii)

                        #print "dbpic = ", dbpic
                        dbpic = Image.open(dbpic)
                        #dbpic = dbpic.getdata()
                        #counter += 1

                        #self.target = target
                        #self.target_1 = target_1
                        
                        match = self.rmsdiff(img, dbpic)

                        print "Match = ", match[0], match[1]
                     #resize_pic = os.path.join(self.path, match)
                     self.resize_pic = Image.open('C:\\photomosaic\\dali\\', match[1])

                     print "M0 = ", match[0]
                     print "M1 = ", match[1]

                     #t1 = os.path.join('C:\\Users\\GREG\\Desktop\\Sandbox\\photomosaic\\dali\\', match[1])
                     #resize_pic = Image.open(t1)
                     #resize_pic = Image.open(resize_pic)
                     t1 = self.resize_pic.load(match[1])
                     self.resize_pic = t1

                     #print "RP = ", resize_pic

                     #print "RP = ", resize_pic

                     width_1 = resize_pic.size[0]
                     height_1 = resize_pic.size[1]

                     #print "W1 =", width_1
                     #print "H2 = ", height_1

                     #resize_pic.resize = ([width_1, height_1])

                     #new_pic = resize_pic((width_1, height_1))

                     #resize_pic = match[1]
                     resize_pic_width = xy[i][2] - xy[i][0]
                     resize_pic_height = xy[i][3] - xy[i][1]

                     #print "RPW = ", resize_pic_width
                     #print "RPH = ", resize_pic_height

                     resize_pic = resize_pic.resize([resize_pic_width, resize_pic_height])

                     #print "resize_pic = ", resize_pic.size

                     #new_pic = resize_pic((resize_pic_width, resize_pic_height))

                     #print "rpw = ", resize_pic_width
                     #print "rph = ", resize_pic_height
                     
                     #paste_pic = self.resize_picture(resize_pic, resize_pic_width, resize_pic_height)

                     im.paste(resize_pic, (xy[i][0], xy[i][1]))
                     #im.paste(paste_pic, (xy[i][0], xy[i][1]))
                     counter += 1
                     if counter == 5:
                         pass
            else:
                 for i in range(0, 4):
                     Q.append(xy[i])
            if len(Q) == 0:
                    switch = 0
        return self.im

    def resize_picture(self, resize_pic, resize_pic_width, resize_pic_height):
        """Resizes the picture database picture to the size of the
        cropped quadrant picture, and returns as value 'out'"""
        self.resize_pic_width = resize_pic_width
        self.resize_pic_height = resize_pic_height
        out = resize_pic.resize(self.resize_pic_width, self.resize_pic_height)
        return out

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

    #def rmsdiff(self, im1, im2):
    def rmsdiff(self, im1, dbpic):
        "Calculate the root-mean-square difference between two images"

        
        counter = 0
        #target = 0
        #print "pictdb = ", pictdb
        """for i in pictdb:
            
            #dbpic = os.path.join(dirname, i)
            dbpic = os.path.join('C:\\photomosaic\\dali', i)
            dbpic = Image.open(dbpic)
            dbpic = dbpic.getdata()
            counter += 1"""
            #print "im1 = ", im1
            #print "dbpic = ", dbpic

            #h = ImageChops.difference(im1, dbpic).histogram()

        diff = ImageChops.difference(im1, dbpic)
        h = diff.histogram()
        sq = (value*(idx**2) for idx, value in enumerate(h))
        sum_of_squares = sum(sq)
        rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
            #return rms

        """h1 = im1.histogram()
            h2 = dbpic.histogram()
     
            rms = math.sqrt(reduce(operator.add,
                map(lambda a,b: (a-b)**2, h1, h2))/len(h1))"""

        """h = ImageChops.difference(im1, dbpic)
            h = h.histogram()

            # calculate rms
            rms = math.sqrt(reduce(operator.add,
                map(lambda h, i: h*(i**2), h, range(256))
            ) / (float(im1.size[0]) * im1.size[1]))"""

        """h1 = im1.histogram()
            h2 = dbpic.histogram()

            #print "h1 = ", h1
            #print "h2 = ", h2
     
            rms = math.sqrt(reduce(operator.add,
            map(lambda a,b: (a-b)**2, h1, h2))/len(h1))"""

        #print "rms = ", rms

            #small_rms = 0

        placeholder = rms
        if placeholder < self.large_rms:

            self.large_rms = placeholder
            #small_rms = placeholder
            #large_rms = small_rms
            #target = pictdb[i]
            #self.target = self.large_rms
            #target1 = i

            #print "dbpic** = ", dbpic
            #target_1 = os.path.join('C:\\Users\\GREG\\Desktop\\Sandbox\\photomosaic\\dali\\', dbpic)
            self.target_1 = dbpic

            #return rms
        #return self.target, self.target_1
        return self.large_rms, self.target_1

    def save_as(self):
        self.im.save("C:\\photomosaic\\" + 'im.jpg', quality = 100)
    

start_time = time.clock()
p1 = photomosaic('C:\\photomosaic\\dali')
p1.create_mosaic("C:\\photomosaic\karan.jpg", 10)
p1.save_as()
run_time = time.clock() - start_time
print "Run time = ", run_time
