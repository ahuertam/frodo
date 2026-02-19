from flask import Flask, render_template, request, jsonify
import os
from bardo import Bardo

app = Flask(__name__, template_folder='templates', static_folder='static')
bardo = Bardo()

@app.route('/')
def index():
    images = []
    images_dir = "Bardo/static/images"
    if os.path.exists(images_dir):
        images = [f for f in os.listdir(images_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        images.sort(reverse=True)
    return render_template('index.html', images=images)

@app.route('/listen', methods=['POST'])
def listen():
    text = request.json.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    bardo.listen(text)
    
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
