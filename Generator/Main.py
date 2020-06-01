from PIL import Image, ImageDraw, ImageFont
import argparse
import math
from random import randint
import random
import string


#draw small circles
def drawCircle(x, y, size):
    d.ellipse(((x-size, y-size), (x+size, y+size)), fill=None, outline = (0 ,0 ,0), width=int(size*0.1))

#places an individual letter
def drawLetter(x, y, letter):
    d.text((x - (imageSize * .02), y - (imageSize * .04)), letter, font=fnt, fill=(0,0,0,255))



#gets command line arguments to set background and circle size
parser = argparse.ArgumentParser(description="enter image size(in pixels) and RGBA color code tuple for the background")
parser.add_argument('size', type=int, nargs=1, default=100, help='Size of the image')
parser.add_argument('background', type=int, nargs=4, default=(255, 255, 255, 255), help='background color of the circle in RGBA')
args = parser.parse_args()

#sets an easier variable from the size argument
imageSize = args.size[0]

#sets random circle text
text = ''.join([random.choice(string.printable) for n in range(randint(2, 32))])


#intialize font
fnt = ImageFont.truetype('c:/windows/fonts/arial.ttf', int((imageSize * .08) - (len(text) / 2)))

#creates square background from inputs
im = Image.new("RGBA", (imageSize, imageSize), (args.background[0], args.background[1], args.background[2], args.background[3]))

#sets up drawing
d = ImageDraw.Draw(im, "RGBA")

#draws inner and outer circle based on iamge size
d.ellipse(((imageSize * 0.10, imageSize * 0.10), (imageSize * 0.90, imageSize * 0.90)), fill=None, outline=(0, 0, 0), width=int(imageSize / 80))
d.ellipse(((imageSize * 0.2, imageSize * 0.2), (imageSize * 0.8, imageSize * 0.8)), fill=None, outline=(0, 0, 0), width=int(imageSize / 80))

#loop to draw circles in a circle
circleRadius = int(imageSize * 0.2)
circleCount = randint(2, 12)
for i in range(circleCount):
    circleX = int(imageSize / 2) + circleRadius * math.cos(2 * math.pi * i / circleCount)
    circleY = int(imageSize / 2) + circleRadius * math.sin(2 * math.pi * i / circleCount)
    drawCircle(circleX, circleY, int(circleRadius * 0.50))

# loop to draw test in a circle
#places text in the middle of the 2 base circles
circleRadius = int(imageSize * 0.35)
textCircleCount = len(text)
for i in range(len(text)):
    textCircleX = int(imageSize / 2) + circleRadius * math.cos(2 * math.pi * i / textCircleCount)
    textCircleY = int(imageSize / 2) + circleRadius * math.sin(2 * math.pi * i / textCircleCount)
    drawLetter(textCircleX, textCircleY, text[i])

#center circle for style
drawCircle(imageSize / 2, imageSize / 2, imageSize / 10)


#saves the image
im.save("test.png")