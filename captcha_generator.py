# captcha_generator.py
from PIL import Image, ImageDraw, ImageFont
import random, string
import os

def random_string(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_captcha(text, base_path_for_font): 
    width, height = 200, 60
    image = Image.new('RGB', (width, height), (0, 200, 200))
    draw = ImageDraw.Draw(image)

    try:
        font_path = os.path.join(base_path_for_font, 'arial.ttf')
        font = ImageFont.truetype(font_path, 40) 
    except IOError:
        print("Font not found or could not be loaded, using default font.")
        font = ImageFont.load_default()
    except Exception as e:
        print(f"An unexpected error occurred loading font: {e}, using default font.")
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_position = ((width - text_bbox[2]) // 2, (height - text_bbox[3]) // 2)
    draw.text(text_position, text, font=font, fill=(0, 0, 0))

    for _ in range(5):
        draw.line([random.randint(0, width), random.randint(0, height),
                   random.randint(0, width), random.randint(0, height)], fill=(0, 0, 0), width=2)
    for _ in range(100):
        draw.point((random.randint(0, width), random.randint(0, height)), fill=(0, 0, 0))

    temp_dir = '/tmp'
    os.makedirs(temp_dir, exist_ok=True)
    filepath = os.path.join(temp_dir, 'captcha_image.png')
    image.save(filepath)
    return text