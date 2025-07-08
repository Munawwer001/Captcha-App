from flask import Flask, render_template, request, jsonify, send_from_directory
from captcha_generator import generate_captcha, random_string
import os

app = Flask(__name__)
captcha_solution = ""
CAPTCHA_IMAGE_FILENAME = 'captcha_image.png' # Define a constant for the filename

@app.route('/')
def home():
    global captcha_solution
    captcha_text = random_string()
    captcha_solution = generate_captcha(captcha_text, app.root_path) # Pass app.root_path
    return render_template('index.html')

@app.route('/captcha_image')
def get_captcha_image():
    # This route serves the generated CAPTCHA image
    return send_from_directory('static', CAPTCHA_IMAGE_FILENAME)

@app.route('/validate', methods=['POST'])
def validate():
    global captcha_solution
    user_input = request.json.get('captcha_input', '').strip().upper()
    result = user_input == captcha_solution
    return jsonify({'success': result})

if __name__ == '__main__':
    app.run(debug=True)