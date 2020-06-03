from PIL import Image, ImageDraw, ImageFont
import argparse
import math
from random import randint
import random


class ImageProperties:
    def __intit__(self, args):
        # sets a size variable from the size argument
        self.image_size = args.size
        # creates square background from inputs
        self.image = Image.new("RGBA", (self.image_size, self.image_size), (args.background[0], args.background[1], \
                                                                            args.background[2], args.background[3]))
        # sets up drawing
        self.painter = ImageDraw.Draw(self.image, "RGBA")


# draw small circles
def draw_circle(x, y, size, imgProp):
    imgProp.painter.ellipse(((x-size, y-size), (x+size, y+size)), fill=None, outline=(0, 0, 0), width=int(size*0.1))


# places an individual letter
def draw_letter(x, y, letter, font, imgProp):
    imgProp.painter.text((x, y), letter, font=font, fill=(0,0,0,255))


def circle_center(img_prop):
    # loop to draw circles in a circle
    circleRadius = int(img_prop.image_size * 0.2)
    circleCount = randint(2, 12)
    for i in range(circleCount):
        circleX = int(img_prop.image_size / 2) + circleRadius * math.cos(2 * math.pi * i / circleCount)
        circleY = int(img_prop.image_size / 2) + circleRadius * math.sin(2 * math.pi * i / circleCount)
        draw_circle(circleX, circleY, int(circleRadius * 0.50), img_prop)
    # center circle for style
    draw_circle(img_prop.image_size / 2, img_prop.image_size / 2, img_prop.image_size / 10, img_prop)


def text_circle_center(img_prop):
    # loop to draw circles in a circle
    circle_count = randint(2, 5)
    circle_radius = int(img_prop.image_size * 0.15) + circle_count * 6
    for i in range(circle_count):
        circle_x = int(img_prop.image_size / 2) + circle_radius * math.cos(2 * math.pi * i / circle_count)
        circle_y = int(img_prop.image_size / 2) + circle_radius * math.sin(2 * math.pi * i / circle_count)
        # draw outer then inner circle
        draw_circle(circle_x, circle_y, int(circle_radius * 1) - circle_count * 14, img_prop)
        draw_circle(circle_x, circle_y, int(((circle_radius * 1) - circle_count * 14) * 0.6), img_prop)

        # add text to inner circles
        inner_circle_radius = int(((circle_radius * 1) - circle_count * 14) * 0.8)
        inner_text = generate_text(6, 10)
        fnt = ImageFont.truetype('dejavuserif.ttf', int((img_prop.image_size * .04) - (len(inner_text) / 2)))
        inner_text_circle_count = len(inner_text)
        for i in range(len(inner_text)):
            inner_text_circle_x = int(circle_x) + inner_circle_radius * math.cos(2 * math.pi * i / inner_text_circle_count)
            inner_text_circle_y = int(circle_y) + inner_circle_radius * math.sin(2 * math.pi * i / inner_text_circle_count)
            draw_letter(inner_text_circle_x - inner_circle_radius * 0.1, inner_text_circle_y - inner_circle_radius * 0.2, inner_text[i], fnt, img_prop)


def star_center(img_prop):
    # sets number of points to generate
    points = randint(3, 13)
    # sets random offset for the points to start
    offset = random.random()
    # creates starting of first line
    old_x = int(img_prop.image_size / 2) + int(img_prop.image_size * 0.3) * math.sin(2 * math.pi * offset)
    old_y = int(img_prop.image_size / 2) + int(img_prop.image_size * 0.3) * math.cos(2 * math.pi * offset)
    # sets the sequence number at max to start to equal 1 on later calculations with division
    current_sequence = points
    # creates iterator so it makes satisfying star shapes relative to number of points
    iterator = math.ceil(points / 2) - 1

    # loops through each point
    for i in range(points):
        # sets which point in the sequence it will do and sets it back down if it goes above the max
        current_sequence = current_sequence + iterator
        if current_sequence > points:
            current_sequence -= points
        # sets the rotation relative to the center for graphing in range 0-1, sets it back down if it goes out of range
        rotation = current_sequence / points + offset
        if rotation > 1:
            rotation -= 1
        # sets the destination of the line
        new_x = int(img_prop.image_size / 2) + int(img_prop.image_size * 0.3) * math.sin(2 * math.pi * rotation)
        new_y = int(img_prop.image_size / 2) + int(img_prop.image_size * 0.3) * math.cos(2 * math.pi * rotation)
        # writes the line from starting to end point
        img_prop.painter.line((old_x, old_y, (new_x, new_y)), fill=(0, 0, 0), width=int(img_prop.image_size / 80))
        # sets the next starting point to the current end of the line
        old_x = new_x
        old_y = new_y


def concenteric_circles(img_prop):
    # sets a starting radius for the circles
    concentric_circle_radius = img_prop.image_size * 0.3
    # sets up the center of the image for later use
    image_middle = img_prop.image_size / 2
    # loops until the radius of the circles gets too small to bother
    while concentric_circle_radius > img_prop.image_size * 0.01:
        # draws a circle starting from the middle outward the radius amount
        img_prop.painter.ellipse(((image_middle - concentric_circle_radius, image_middle - concentric_circle_radius), \
                                  (image_middle + concentric_circle_radius, image_middle + concentric_circle_radius)) \
                                 , fill=None, outline = (0 ,0 ,0), width=int(concentric_circle_radius * 0.05))
        # makes the radius smaller for the next circle
        concentric_circle_radius *= 0.9


def generate_text(min_letter, max_letter):
    # sets character variable and a unicode range to pull from
    get_char = chr
    unicode_range = (0x0021, 0x038C)
    # creates a list of chars to pull from based on all the chars in the unicode range
    alphabet = [
        get_char(char_point) for char_point in range(unicode_range[0], unicode_range[1])
    ]
    # returns a string with random choices from the alphabet list
    return''.join([random.choice(alphabet) for n in range(randint(min_letter, max_letter))])


def get_args():
    # gets command line arguments to set background and circle size
    parser = argparse.ArgumentParser(description="Enter image size(in pixels) and RGBA color code tuple for the background")
    parser.add_argument('size', type=int, nargs="?", default=1000, help='Size of the image')
    parser.add_argument('background', type=int, nargs=argparse.REMAINDER, default=(255, 255, 255, 255), help='Background color of the circle in RGBA')
    return parser.parse_args()


def main():
    # gets command line args
    args = get_args()
    # sets transparency to full if it wasn't specified
    if len(args.background) == 3:
        args.background.append(255)
    # deals with if there are no args for background and sets it to default white
    elif len(args.background) < 4:
        args.background = (255, 255, 255, 255)

    # Creates image properties object
    img_prop = ImageProperties()
    img_prop.__intit__(args)

    # draws outer circles based on image size
    img_prop.painter.ellipse(((img_prop.image_size * 0.10, img_prop.image_size * 0.10), (img_prop.image_size * 0.90, img_prop.image_size * 0.90)), \
                             fill=None, outline=(0, 0, 0), width=int(img_prop.image_size / 80))
    img_prop.painter.ellipse(((img_prop.image_size * 0.2, img_prop.image_size * 0.2), (img_prop.image_size * 0.8, img_prop.image_size * 0.8)), \
                             fill=None, outline=(0, 0, 0), width=int(img_prop.image_size / 80))

    # sets random circle text
    text = generate_text(10, 40)
    # initialize font
    fnt = ImageFont.truetype('dejavuserif.ttf', int((img_prop.image_size * .08) - (len(text) / 2)))
    # places text in the middle of the 2 base circles
    circle_radius = int(img_prop.image_size * 0.35)
    text_circle_count = len(text)
    for i in range(len(text)):
        text_circle_x = int(img_prop.image_size / 2) + circle_radius * math.cos(2 * math.pi * i / text_circle_count)
        text_circle_y = int(img_prop.image_size / 2) + circle_radius * math.sin(2 * math.pi * i / text_circle_count)
        # some adjustments to x and y so they fit into the circle better
        draw_letter(text_circle_x - (img_prop.image_size * .02), text_circle_y - (img_prop.image_size * .04), text[i], fnt, img_prop)

    # choses what the inner circle type will be out of a list and runs it
    switcher = {
        1: circle_center,
        2: text_circle_center,
        3: star_center,
        4: concenteric_circles,
        5: star_center,
        6: text_circle_center,
    }
    # gets and runs the function for the corresponding inner circle
    inner_style_function = switcher.get(randint(1, 6))
    inner_style_function(img_prop)

    # saves the image
    img_prop.image.save("MagicCircle.png")


if __name__ == "__main__":
    main()
