from PIL import Image, ImageDraw, ImageFont
import random, string
import os

def random_string(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Modify generate_captcha to accept base_path (app.root_path)
def generate_captcha(text, base_path):
    width, height = 200, 60
    image = Image.new('RGB', (width, height), (0, 200, 200))
    draw = ImageDraw.Draw(image)

    try:
        # It's good practice to ensure 'arial.ttf' is accessible or provide a fallback
        font_path = os.path.join(base_path, "static", "arial.ttf") # Assuming arial.ttf is in static
        if not os.path.exists(font_path):
            font = ImageFont.load_default() # Fallback if font not found
        else:
            font = ImageFont.truetype(font_path, 40)
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

    # Ensure the static directory exists
    static_dir = os.path.join(base_path, 'static')
    os.makedirs(static_dir, exist_ok=True)

    filepath = os.path.join(static_dir, 'captcha_image.png')
    image.save(filepath)
    return text