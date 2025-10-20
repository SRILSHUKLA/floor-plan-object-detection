from flask import Flask, request, jsonify, render_template
import os
from detection import detect_doors
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        image = Image.open(filepath)
        doors = detect_doors(image)
        # Scale to 3D plane: assume image is 1000x1000, plane 10x10 units
        img_width, img_height = image.size
        plane_size = 10.0
        scale_x = plane_size / img_width
        scale_y = plane_size / img_height
        doors_3d = []
        for door in doors:
            doors_3d.append({
                'x': door['x'] * scale_x - plane_size/2,
                'y': 0,  # On the plane
                'z': door['y'] * scale_y - plane_size/2,
                'w': door['w'] * scale_x,
                'h': door['h'] * scale_y
            })
        return jsonify({'doors': doors_3d})

if __name__ == '__main__':
    app.run(debug=True)
