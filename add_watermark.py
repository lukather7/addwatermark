#!/usr/local/bin/python3
from PIL import Image

import glob
import os

### get the home directory of the user on the system
home = os.path.expanduser("~")

### concatinate home directory with the path of sign.png
watermarkfname = home + "/watermark.png"

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

### watermarkfname is filename of merge with alpha channel to tranparent
def merge_with_sign(originalfname, watermarkfname, placerightflag):
    originalimg = Image.open(originalfname).convert('RGBA')
    watermarkimg = Image.open(watermarkfname).convert('RGBA')
    ### get height and width of originalimg
    ow, oh = originalimg.size
    sw, sh = watermarkimg.size

    margin = 50

    #### check the rightflag is true or not
    if (placerightflag == False):
        #### add margin to watermarkimg of top and right to place watermark on left bottom
        marginimg = add_margin(watermarkimg, oh-sh-margin, ow-sw-margin, margin, margin, (0,0,0)).convert('RGBA')
    else:
        #### if you want watermark on right bottom then change as below
        marginimg = add_margin(watermarkimg, oh-sh-margin, margin, margin, ow-sw-margin, (0,0,0)).convert('RGBA')

    #### make black pixel into transparent
    pixdata = marginimg.load()

    width, height = marginimg.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (0, 0, 0, 255):
                pixdata[x, y] = (0, 0, 0, 0)

    return Image.alpha_composite(originalimg, marginimg)

### check the ./src directory exist or not
if not os.path.exists('./src'):
    print('No ./src directory')
    print('Usage: python3 add_watermark.py [-r]')
    print(' place "watermark.png" saved with tranparent background on your home directory')
    exit()
#### check the watermarkfname exist or not
if not os.path.exists(watermarkfname):
    print('No watermark.png on your home directory')
    exit()

### check the ./dst directory exist or not
dstdir = './dst'
if not os.path.exists(dstdir):
    os.mkdir(dstdir)
### get all file name of jpg and png in the directory
fnames = glob.glob('./src/*.jpg') + glob.glob('./src/*.png') \
        + glob.glob('./src/*.JPG') + glob.glob('./src/*.PNG')

placerightflag = False
### check command line argument has "-r" or not
if len(sys.argv) == 2 and sys.argv[1] == '-r':
    placerightflag = True

#### get each file name from fnames
for fname in fnames:
    ### call merge_with_sign function with 
    ### originalfname and watermarkfname
    mergeimg = merge_with_sign(fname, watermarkfname, placerightflag)
    ### save mergeimg to dstdir with file name as fname with extension png
    mergeimg.convert("RGB").save(os.path.join(dstdir, os.path.basename(fname)))