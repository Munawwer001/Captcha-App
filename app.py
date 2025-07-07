from flask import Flask, render_template, request, jsonify
from captcha_generator import generate_captcha, random_string

app = Flask(__name__)
captcha_solution = ""

@app.route('/')
def home():
    global captcha_solution
    captcha_text = random_string()
    captcha_solution = generate_captcha(captcha_text)
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    global captcha_solution
    user_input = request.json.get('captcha_input', '').strip().upper()
    result = user_input == captcha_solution
    return jsonify({'success': result})

# ✅ THIS IS CRUCIAL
if __name__ == '__main__':
    app.run(debug=True)
