# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import os
# from pathlib import Path
# from werkzeug.utils import secure_filename
# import google.generativeai as genai
# from dotenv import load_dotenv  # <-- add this
# from PIL import Image

# from kolam_processor2 import process_kolam, identify_pattern

# # ---- load .env ----
# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # <-- configure here


# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": ["*", "null"]}})

# # ---- folders ----
# BASE_DIR = Path(__file__).resolve().parent
# UPLOAD_FOLDER = BASE_DIR / 'uploads'
# PROCESSED_FOLDER = BASE_DIR / 'processed'

# UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
# PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

# app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
# app.config['PROCESSED_FOLDER'] = str(PROCESSED_FOLDER)

# ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'bmp', 'webp'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT



# @app.route('/process_kolam', methods=['POST'])
# def process_kolam_route():
#     try:
#         file = request.files['file']
#         filename = secure_filename(file.filename)
#         upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         output_filename = "processed_" + filename
#         output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
#         svg_filename = "processed_" + filename + ".svg"
#         svg_path = os.path.join(app.config['PROCESSED_FOLDER'], svg_filename)

#         file.save(upload_path)

#         # Run OpenCV-based processing
#         process_kolam(upload_path, output_path, svg_path)

#         # Identify simple pattern
#         pattern = identify_pattern(upload_path)

#         return jsonify({
#             "pattern": pattern,
#             "processed_image": f"http://127.0.0.1:5000/processed/{output_filename}",
#             "svg": f"http://127.0.0.1:5000/processed/{svg_filename}"
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 400


# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file uploaded'}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No file selected'}), 400

#     if not allowed_file(file.filename):
#         return jsonify({'error': 'File type not allowed (use png/jpg/jpeg/bmp/webp)'}), 400

#     filename = secure_filename(file.filename)
#     upload_folder = app.config['UPLOAD_FOLDER']

#     file_path = os.path.join(upload_folder, filename)
#     file.save(file_path)

#     debug_path = os.path.join(upload_folder, filename + "_debug.png")
#     svg_path = os.path.join(upload_folder, filename + ".svg")

#     try:
#         process_kolam(file_path, debug_path, svg_path)
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': str(e)}), 500

#     return jsonify({'message': 'File uploaded and processed successfully'})



# # serve processed images
# @app.route('/processed/<path:filename>')
# def processed_files(filename):
#     return send_from_directory(app.config['PROCESSED_FOLDER'], filename)


# @app.route('/generate_kolam', methods=['POST'])
# def generate_kolam():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file uploaded'}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No file selected'}), 400

#     if not allowed_file(file.filename):
#         return jsonify({'error': 'File type not allowed'}), 400

#     filename = secure_filename(file.filename)
#     upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     file.save(upload_path)

#     # ✅ Use a fixed prompt now
#     prompt = "Transform the given picture into a rangoli design, keeping its overall pattern but reimagined with traditional rangoli motifs, symmetry and style."

#     # ---- your Gemini / kolam generation logic here ----
#     # new_filename and new_path are created for demonstration
#     new_filename = 'generated_' + filename
#     new_path = os.path.join(app.config['PROCESSED_FOLDER'], new_filename)

#     # (dummy image generation for now)
#     from PIL import Image, ImageDraw
#     im = Image.open(upload_path).convert("RGB")
#     draw = ImageDraw.Draw(im)
#     draw.rectangle([10, 10, 120, 120], outline="purple", width=5)
#     im.save(new_path)



#     return jsonify({
        
#         "new_kolam_image": f"http://127.0.0.1:5000/processed/{new_filename}"
#     })


# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from pathlib import Path
from werkzeug.utils import secure_filename
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

from kolam_processor2 import process_kolam, identify_pattern

# ---- load .env ----
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["*", "null"]}})

# ---- folders ----
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / 'uploads'
PROCESSED_FOLDER = BASE_DIR / 'processed'

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['PROCESSED_FOLDER'] = str(PROCESSED_FOLDER)

ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


# -------------------------------
# Kolam (OpenCV + SVG) Route
# -------------------------------
@app.route('/uploadfile', methods=['POST'])
def uploadfile():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed (use png/jpg/jpeg/bmp/webp)'}), 400

    filename = secure_filename(file.filename)
    upload_folder = app.config['UPLOAD_FOLDER']

    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    # ✅ save outputs inside processed/
    debug_path = os.path.join(app.config['PROCESSED_FOLDER'], filename + "_debug.png")
    svg_path = os.path.join(app.config['PROCESSED_FOLDER'], filename + ".svg")

    try:
        process_kolam(file_path, debug_path, svg_path)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'message': 'File uploaded and processed successfully',
        'debug_image': f"http://127.0.0.1:5000/processed/{filename}_debug.png",
        'svg': f"http://127.0.0.1:5000/processed/{filename}.svg"
    })



# -------------------------------
# Gemini Reasoning Route
# -------------------------------
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file'}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Call Gemini
        prompt = request.form.get('prompt', 'Identify patterns')
        model = genai.GenerativeModel("gemini-1.5-flash")
        image = Image.open(file_path)
        response = model.generate_content([prompt, image])

        return jsonify({
            "response": response.text if response else "No response"
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# -------------------------------
# Serve processed files
# -------------------------------
@app.route('/processed/<path:filename>')
def processed_files(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)


# -------------------------------
# Dummy Kolam Generation (for test)
# -------------------------------
@app.route('/generate_kolam', methods=['POST'])
def generate_kolam():
    try:
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file'}), 400

        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        # Dummy generation
        new_filename = 'generated_' + filename
        new_path = os.path.join(app.config['PROCESSED_FOLDER'], new_filename)

        from PIL import ImageDraw
        im = Image.open(upload_path).convert("RGB")
        draw = ImageDraw.Draw(im)
        draw.rectangle([10, 10, 120, 120], outline="purple", width=5)
        im.save(new_path)

        return jsonify({
            "new_kolam_image": f"http://127.0.0.1:5000/processed/{new_filename}"
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
