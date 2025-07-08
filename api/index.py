# api/index.py
from flask import Flask, render_template, request, jsonify, send_from_directory
from captcha_generator import generate_captcha, random_string
import os

app = Flask(__name__)
captcha_solution = ""
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

CAPTCHA_IMAGE_FILENAME = 'captcha_image.png'

@app.route('/')
def home():
    global captcha_solution
    captcha_text = random_string()
    captcha_solution = generate_captcha(captcha_text, STATIC_DIR)
    return render_template('index.html')

@app.route('/captcha_image')
def get_captcha_image():
    temp_image_path = os.path.join('/tmp', CAPTCHA_IMAGE_FILENAME)
    if os.path.exists(temp_image_path):
        return send_from_directory('/tmp', CAPTCHA_IMAGE_FILENAME, mimetype='image/png')
    else:
        return "Image not found", 404


@app.route('/validate', methods=['POST'])
def validate():
    global captcha_solution
    user_input = request.json.get('captcha_input', '').strip().upper()
    result = user_input == captcha_solution
    return jsonify({'success': result})