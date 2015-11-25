import os
from PIL import Image

def convert_to_jpg(infile):
    f, e = os.path.splitext(infile)
    outfile = f + ".jpg"
    if infile != outfile:
        try:
            x = Image.open(infile).save(outfile)
        except IOError:
        	pass
            #print("cannot convert", infile)
    return outfile


def main():
    dirname = 'tiles' # a directory of .gif files
    pictdb = os.listdir(dirname)
    L = []
    for item in pictdb:
        im = (convert_to_jpg(item))
        L.append(im)

    print (L)		
    return L

if __name__ == '__main__':
	main()