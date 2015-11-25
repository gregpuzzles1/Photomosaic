import os
from PIL import Image

def convert_jpg(infile):
    f, e = os.path.splitext(infile)
    outfile = f + ".jpg"
    if infile != outfile:
        try:
            Image.open(infile).save(outfile)
        except IOError:
        	pass
            #print("cannot convert", infile)
    return outfile

#infile = "tiles/P1030208.gif"

#print convert_jpg(infile)
def main():
	L = []
	dirname = 'tiles'
	pictdb = os.listdir(dirname)
	print (pictdb)
	for item in pictdb:
		L.append(convert_jpg(item))

	print (L)		
	return L

if __name__ == '__main__':
	main()