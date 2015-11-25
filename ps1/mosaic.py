# mosaic.py
# 
# Version 1.0
# UVA CS 1120
# Problem Set 1
from graphics import * 
import glob

def make_color(red, green, blue):
        # In this problem set, a color is just a list of three integers
        # corresponding to its red, green and blue light components. 
        return [red, green, blue]

def get_red(color):
        return color[0]

def get_green(color):
        return color[1]

def get_blue(color):
        return color[2] 

def add_color(color1, color2):
        # Returns a new color that is equal to the sum of color1 and
        # color2.
        return make_color(get_red(color1) + get_red(color2),
                get_green(color1) + get_green(color2),
                get_blue(color1) + get_blue(color2))

def sum_colors(color_list): 
        # Sums all of the colors in a list of colors. 
        if color_list is []: 
                # If there are no colors to sum, return black. 
                return make_color(0,0,0)
        else:
                # Otherwise, add the first color in the list to the
                # sum of the rest of the colors in the list.
                return add_color(color_list[0], sum_colors(color_list[1:]))

def sum_colors_alterate(color_list): 
        # The following definition of sum_colors() computes exactly the
        # same thing as the previous one. We'll cover "reduce" (also known
        # as "fold") later in this course. 
        return reduce(add_color, color_list, make_color(0,0,0))
                                
def show_color(color): 
        # Displays a friendly window containing an exmaple of the given
        # color. 
        win = GraphWin("Showing The Colors", 640, 480)
        c = Circle(Point(320,240), 200)
        rgb = color_rgb(get_red(color), get_green(color), get_blue(color))
        c.setFill(rgb) 
        c.draw(win)
        t1 = Text(Point(320,20), "Click to close this window.")
        t1.draw(win) 
        t2 = Text(Point(320,460), str(color))
        t2.draw(win) 
        win.getMouse() # Pause to view result
        win.close()    # Close window when done

def show_image(filename): 
        # Displays a friendly window containing an image stored on disk.
        img = Image(Point(0,0), filename) 
        w = img.getWidth() 
        h = img.getHeight()  
        win = GraphWin("Showing " + filename, w, h)
        img.move(w/2,h/2) # center the image 
        img.draw(win) 
        win.getMouse() # Pause to view result
        win.close()    # Close window when done

def find_best_match(sample_color, tiles, tile_colors, closer_color):
        # Given a sample color, find the tile image that is closest to 
        # that sample color according to closer_color. 
        if tiles is []:
                print "Error: no tiles to match?" 
                return None
        elif len(tiles) is 1: 
                return [tiles[0], tile_colors[0]]
        else:
                [a_tile, a_color] = [tiles[0], tile_colors[0]]
                [b_tile, b_color] = find_best_match(sample_color, tiles[1:], tile_colors[1:], closer_color) 
                if closer_color(sample_color, a_color, b_color): 
                        return [a_tile, a_color]
                else:
                        return [b_tile, b_color]


def make_photomosaic(original_filename, tile_directory, color_comparator): 
        # Creates a photomosaic that looks like the image in
        # original_filename but is made up of tiles from the GIF images in
        # tile_directory. Displays the result on the screen and stores the
        # result in output_filename. 

        # First, we load the original image.
        original = Image(Point(0,0), original_filename) 
        ow = original.getWidth()
        oh = original.getHeight() 

        # Next, we find all of the tiles files.
        tile_files = glob.glob(tile_directory + "/*.gif") 
        if tile_files is []:
                print "No .gif files found in " + tile_directory
                return 

        # Now we load all of the tile images. 
        tile_images = [Image(Point(0,0), fname) for fname in tile_files]

        tw = tile_images[0].getWidth() 
        th = tile_images[0].getHeight() 

        if ow < tw or oh < th:
                print "Original image is smaller than the tiles!" 
                return 

        def image_average_region_color(image, x, y, dx, dy):
                # Find the average color of a rectangular sub-region of an
                # image. We compute the average color for all pixels
                # between [x,y] and [x+dx, y+dy]. 
                result = [0,0,0] 
                for i in range(dx):
                        for j in range(dy): 
                                pixel = image.getPixel(x+i, y+j) 
                                result = add_color(result, pixel) 
                result[0] = result[0] / (dx * dy) 
                result[1] = result[1] / (dx * dy) 
                result[2] = result[2] / (dx * dy) 
                return result 

        def image_average_color(image):
                # For simplicity, we'll often want to find the average
                # color of an entire image. 
                return image_average_region_color(image, 0, 0, image.getWidth(), image.getHeight())

        tile_colors = [image_average_color(tile) for tile in tile_images] 

        win = GraphWin("Photomosaic", ow, oh)

        for x in range(ow/tw):
                for y in range(oh/th):
                        sample_color = image_average_region_color(original, x*tw, y*th, tw, th) 
                        [best_image, best_color] = find_best_match(sample_color, tile_images, tile_colors, color_comparator) 

                        pasted_image = best_image.clone() 
                        pasted_image.move(x*tw + (tw/2), y*th + (th/2))
                        pasted_image.draw(win) 

        win.getMouse() # Pause to view result
        win.close()    # Close window when done

        return 

        



