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
def drawLetter(x, y, letter, font):
    d.text((x, y), letter, font=font, fill=(0,0,0,255))

def circleCenter():
    # loop to draw circles in a circle
    circleRadius = int(imageSize * 0.2)
    circleCount = randint(2, 12)
    for i in range(circleCount):
        circleX = int(imageSize / 2) + circleRadius * math.cos(2 * math.pi * i / circleCount)
        circleY = int(imageSize / 2) + circleRadius * math.sin(2 * math.pi * i / circleCount)
        drawCircle(circleX, circleY, int(circleRadius * 0.50))
    # center circle for style
    drawCircle(imageSize / 2, imageSize / 2, imageSize / 10)

def textCircleCenter():
    # loop to draw circles in a circle
    circleCount = randint(2, 5)
    circleRadius = int(imageSize * 0.15) + circleCount * 6
    for i in range(circleCount):
        circleX = int(imageSize / 2) + circleRadius * math.cos(2 * math.pi * i / circleCount)
        circleY = int(imageSize / 2) + circleRadius * math.sin(2 * math.pi * i / circleCount)
        #draw outer then inner circle
        drawCircle(circleX, circleY, int(circleRadius * 1) - circleCount * 14)
        drawCircle(circleX, circleY, int(((circleRadius * 1) - circleCount * 14) * 0.6))

        #add text to inner circles
        innerCircleRadius = int(((circleRadius * 1) - circleCount * 14) * 0.8)
        innerText = generateText(6, 10)
        fnt = ImageFont.truetype('dejavuserif.ttf', int((imageSize * .04) - (len(innerText) / 2)))
        innerTextCircleCount = len(innerText)
        for i in range(len(innerText)):
            innerTextCircleX = int(circleX) + innerCircleRadius * math.cos(2 * math.pi * i / innerTextCircleCount)
            innerTextCircleY = int(circleY) + innerCircleRadius * math.sin(2 * math.pi * i / innerTextCircleCount)
            drawLetter(innerTextCircleX - innerCircleRadius * 0.1, innerTextCircleY - innerCircleRadius * 0.2, innerText[i], fnt)



def generateText(minLetter, maxLetter):
    get_char = chr
    unicode_range = (0x0021, 0x038C)
    alphabet = [
        get_char(char_point) for char_point in range(unicode_range[0], unicode_range[1])
    ]
    return''.join([random.choice(alphabet) for n in range(randint(minLetter, maxLetter))])


def getArgs():
    #gets command line arguments to set background and circle size
    parser = argparse.ArgumentParser(description="enter image size(in pixels) and RGBA color code tuple for the background")
    parser.add_argument('size', type=int, nargs=1, default=100, help='Size of the image')
    parser.add_argument('background', type=int, nargs=4, default=(255, 255, 255, 255), help='background color of the circle in RGBA')
    return parser.parse_args()

#gets command line args
args = getArgs()
#sets a size variable from the size argument
imageSize = args.size[0]

#creates square background from inputs
im = Image.new("RGBA", (imageSize, imageSize), (args.background[0], args.background[1], args.background[2], args.background[3]))

#sets up drawing
d = ImageDraw.Draw(im, "RGBA")

#draws inner and outer circle based on image size
d.ellipse(((imageSize * 0.10, imageSize * 0.10), (imageSize * 0.90, imageSize * 0.90)), fill=None, outline=(0, 0, 0), width=int(imageSize / 80))
d.ellipse(((imageSize * 0.2, imageSize * 0.2), (imageSize * 0.8, imageSize * 0.8)), fill=None, outline=(0, 0, 0), width=int(imageSize / 80))

#sets random circle text
text = generateText(10, 40)
#intialize font
fnt = ImageFont.truetype('dejavuserif.ttf', int((imageSize * .08) - (len(text) / 2)))
#places text in the middle of the 2 base circles
circleRadius = int(imageSize * 0.35)
textCircleCount = len(text)
for i in range(len(text)):
    textCircleX = int(imageSize / 2) + circleRadius * math.cos(2 * math.pi * i / textCircleCount)
    textCircleY = int(imageSize / 2) + circleRadius * math.sin(2 * math.pi * i / textCircleCount)
    #some adjustments to x and y so they fit into the circle better
    drawLetter(textCircleX - (imageSize * .02), textCircleY - (imageSize * .04), text[i], fnt)

#choses what the inner circle type will be out of a list and runs it
switcher = {
    1:circleCenter,
    2:textCircleCenter
}
innerStyleFunction = switcher.get(randint(1, 2))
innerStyleFunction()

#saves the image
im.save("test.png")