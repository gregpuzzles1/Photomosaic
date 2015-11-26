import os
from PIL import Image

inputDir = "tiles/"
outputDir = "tiles-png/"

if not os.path.exists(outputDir):
    os.makedirs(outputDir)
	
for i in os.listdir(inputDir):
    if i.endswith(".gif"):
		Image.open(inputDir + i).convert('RGB').save(outputDir + os.path.splitext(i)[0] + ".png")
    else:
        continue