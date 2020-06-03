from PIL import Image, ImageDraw, ImageFont
import argparse
import math
from random import randint
import random


# draw small circles
def drawCircle(x, y, size):
    d.ellipse(((x-size, y-size), (x+size, y+size)), fill=None, outline = (0 ,0 ,0), width=int(size*0.1))


# places an individual letter
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
        # draw outer then inner circle
        drawCircle(circleX, circleY, int(circleRadius * 1) - circleCount * 14)
        drawCircle(circleX, circleY, int(((circleRadius * 1) - circleCount * 14) * 0.6))

        # add text to inner circles
        innerCircleRadius = int(((circleRadius * 1) - circleCount * 14) * 0.8)
        innerText = generateText(6, 10)
        fnt = ImageFont.truetype('dejavuserif.ttf', int((imageSize * .04) - (len(innerText) / 2)))
        innerTextCircleCount = len(innerText)
        for i in range(len(innerText)):
            innerTextCircleX = int(circleX) + innerCircleRadius * math.cos(2 * math.pi * i / innerTextCircleCount)
            innerTextCircleY = int(circleY) + innerCircleRadius * math.sin(2 * math.pi * i / innerTextCircleCount)
            drawLetter(innerTextCircleX - innerCircleRadius * 0.1, innerTextCircleY - innerCircleRadius * 0.2, innerText[i], fnt)


def starCenter():
    # sets number of points to generate
    points = randint(3, 13)
    # sets random offset for the points to start
    offset = random.random()
    # creates starting of first line
    oldx = int(imageSize/2) + int(imageSize * 0.3) * math.sin(2 * math.pi * offset)
    oldy = int(imageSize/2) + int(imageSize * 0.3) * math.cos(2 * math.pi * offset)
    # sets the sequence number at max to start to equal 1 on later calculations with division
    currentSequence = points
    # creates iterator so it makes staisfying star shapes relative to number of points
    iterator = math.ceil(points / 2) - 1

    # loops through each point
    for i in range(points):
        # sets which point in the sequence it will do and sets it back down if it goes above the max
        currentSequence = currentSequence + iterator
        if currentSequence > points:
            currentSequence -= points
        # sets the rotation relative to the center for graphing in range 0-1, sets it back down if it goes out of range
        rotation = currentSequence / points + offset
        if rotation > 1:
            rotation -= 1
        # sets the destination of the line
        newx = int(imageSize/2) + int(imageSize * 0.3) * math.sin(2 * math.pi * rotation)
        newy = int(imageSize/2) + int(imageSize * 0.3) * math.cos(2 * math.pi * rotation)
        # writes the line from starting to end point
        d.line((oldx, oldy, (newx, newy)), fill=(0, 0, 0), width=int(imageSize / 80))
        # sets the next starting point to the current end of the line
        oldx = newx
        oldy = newy

def concentericCircles():
    # sets a starting radius for the circles
    concentricCircleRadius = imageSize * 0.3
    # sets up the center of the image for later use
    imageMiddle = imageSize / 2
    # loops until the radius of the circles gets too small to bother
    while concentricCircleRadius > imageSize * 0.01:
        # draws a circle starting from the middle outward the radius amount
        d.ellipse(((imageMiddle - concentricCircleRadius, imageMiddle - concentricCircleRadius), (imageMiddle + concentricCircleRadius, imageMiddle + concentricCircleRadius))\
                  , fill=None, outline = (0 ,0 ,0), width=int(concentricCircleRadius * 0.05))
        # makes the radius smaller for the next circle
        concentricCircleRadius *= 0.9

def generateText(minLetter, maxLetter):
    # sets chracater variable and a unicode range to pull from
    get_char = chr
    unicode_range = (0x0021, 0x038C)
    # creates a list of chars to pull from based on all the chars in the unicode range
    alphabet = [
        get_char(char_point) for char_point in range(unicode_range[0], unicode_range[1])
    ]
    # returns a string with random choices from the alphabet list
    return''.join([random.choice(alphabet) for n in range(randint(minLetter, maxLetter))])


def getArgs():
    # gets command line arguments to set background and circle size
    parser = argparse.ArgumentParser(description="enter image size(in pixels) and RGBA color code tuple for the background")
    parser.add_argument('size', type=int, nargs="?", default=1000, help='Size of the image')
    parser.add_argument('background', type=int, nargs=argparse.REMAINDER, default=(255, 255, 255, 255), help='background color of the circle in RGBA')
    return parser.parse_args()


# gets command line args
args = getArgs()
# sets transparency to full if it wasn't specified
if len(args.background) == 3:
    args.background.append(255)
# deals with if there are no args for background and sets it to default white
elif len(args.background) < 4:
    args.background = (255, 255, 255, 255)

# sets a size variable from the size argument
imageSize = args.size

# creates square background from inputs
im = Image.new("RGBA", (imageSize, imageSize), (args.background[0], args.background[1], args.background[2], args.background[3]))

# sets up drawing
d = ImageDraw.Draw(im, "RGBA")

# draws outer circles based on image size
d.ellipse(((imageSize * 0.10, imageSize * 0.10), (imageSize * 0.90, imageSize * 0.90)), fill=None, outline=(0, 0, 0), width=int(imageSize / 80))
d.ellipse(((imageSize * 0.2, imageSize * 0.2), (imageSize * 0.8, imageSize * 0.8)), fill=None, outline=(0, 0, 0), width=int(imageSize / 80))

# sets random circle text
text = generateText(10, 40)
# intialize font
fnt = ImageFont.truetype('dejavuserif.ttf', int((imageSize * .08) - (len(text) / 2)))
# places text in the middle of the 2 base circles
circleRadius = int(imageSize * 0.35)
textCircleCount = len(text)
for i in range(len(text)):
    textCircleX = int(imageSize / 2) + circleRadius * math.cos(2 * math.pi * i / textCircleCount)
    textCircleY = int(imageSize / 2) + circleRadius * math.sin(2 * math.pi * i / textCircleCount)
    # some adjustments to x and y so they fit into the circle better
    drawLetter(textCircleX - (imageSize * .02), textCircleY - (imageSize * .04), text[i], fnt)

# choses what the inner circle type will be out of a list and runs it
switcher = {
    1:circleCenter,
    2:textCircleCenter,
    3:starCenter,
    4:concentericCircles,
    5:starCenter,
    6:textCircleCenter,
}
# gets and runs the function for the corresponding inner circle
innerStyleFunction = switcher.get(randint(1, 6))
innerStyleFunction()

# saves the image
im.save("magicCircle.png")