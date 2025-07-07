# captcha_generator.py
from PIL import Image, ImageDraw, ImageFont
import random, string
import os

def random_string(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_captcha(text):
    width, height = 200, 60
    image = Image.new('RGB', (width, height), (0, 200, 200))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_position = ((width - text_bbox[2]) // 2, (height - text_bbox[3]) // 2)
    draw.text(text_position, text, font=font, fill=(0, 0, 0))

    for _ in range(5):
        draw.line([random.randint(0, width), random.randint(0, height),
                   random.randint(0, width), random.randint(0, height)], fill=(0, 0, 0), width=2)

    for _ in range(100):
        draw.point((random.randint(0, width), random.randint(0, height)), fill=(0, 0, 0))

    filepath = os.path.join('static', 'captcha_image.png')
    image.save(filepath)
    return text
