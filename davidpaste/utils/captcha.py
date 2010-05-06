#-*-coding:utf-8-*-
import Image, ImageDraw, ImageFont, cStringIO, random

def getCaptcha():
    """
    Generate a captcha image
    """
    im = Image.new("RGB", (52, 20))
    draw = ImageDraw.Draw(im)
    for x in range(0, 100):
        for y in range(0, 60):
            draw.point((x, y), (255, 255, 255))
    font = ImageFont.truetype('FreeMono.ttf', 18)
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    word = ''
    for i in range(4):
        word = word + alphabet[random.randint(0, len(alphabet) -1)]
    draw.text((4, 0), word, font=font, fill=(226, 33, 33))
    f = cStringIO.StringIO()
    im.save(f, "GIF")
    f.seek(0)
    return word, f

