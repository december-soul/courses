from random import randrange
from PIL import Image, ImageDraw, ImageFont
import json
import os


# image has 8192*8192 pixel
def coordinateToPixel(x, y, im_x, im_y):
    # scale coordinate to imagesize
    # set 0,0 to the center of the image
    # set offset to fix image to coordinate
    # todo: this don't fix, find better parameters
    scale = 12500
    offset_x = -500
    offset_y = 2200
    z_x = im_x / 2 * scale / im_x + offset_x
    z_y = im_y / 2 * scale / im_y + offset_y
    return (z_x + x) * im_x / scale, (z_y - y) * im_y / scale


with Image.open("grand-theft-auto-v_karte-satellit_hq.jpg") as im:
    draw = ImageDraw.Draw(im)

    for file in os.listdir("courses/"):
        if file.endswith(".json"):
            print(os.path.join("courses/", file))
            try:
                with open("courses/" + file) as json_file:
                    data = json.load(json_file)
                    old_x = 0
                    old_y = 0
                    start_x = 0
                    start_y = 0
                    color = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
                    for p in data['WayPointList']:
                        (x, y) = coordinateToPixel(p["X"], p["Y"], im.size[0], im.size[0])
                        print("  x={} y={}".format(x, y))
                        draw.rectangle((x, y, x + 20, y + 20), fill=color, outline=(255, 0, 255))
                        if old_x != 0:
                            draw.line((old_x, old_y, x, y), fill=color, width=5)
                        else:
                            start_x = x
                            start_y = y
                        old_x = x
                        old_y = y
                    fill_color = (255, 0, 0)
                    stroke_color = color
                    draw.text((start_x, start_y), file[:-5], font=ImageFont.truetype("arial.ttf", 30), fill=fill_color,
                              stroke_width=3, stroke_fill=stroke_color)
            except:
                print("skip " + "courses/" + file)
                pass
    im.save("courses/all_courses.png")
