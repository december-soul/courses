from random import randrange
from PIL import Image, ImageDraw, ImageFont
import json
import os


def coordinateToPixel(x, y, im_x, im_y):
    # scale coordinate to imagesize
    scale_x =  10000 / im_x
    scale_y =  -12000 / im_y
    offset_x = 2640
    offset_y = 5284

    z_x = x / scale_x + offset_x
    z_y = y / scale_y + offset_y
    #print("y={} im_y={} scale_y={} offset_y={} z_y={} ".format(y, im_y, scale_y, offset_y, z_y) )
    #print("x={} im_x={} scale_x={} offset_x={} z_x={} ".format(x, im_x, scale_x, offset_x, z_x) )
    return z_x, z_y


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
                        (x, y) = coordinateToPixel(p["X"], p["Y"], im.size[0], im.size[1])
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
