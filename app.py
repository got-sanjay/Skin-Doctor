# app.py
from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from test import model_predict

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploaded_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def clear_upload_folder():
    folder = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    error = None
    uploaded_image = 'static/img/1.png'
    post_button = False
    
    if request.method == 'POST':
        if 'image' not in request.files:
            error = "No image part"
        else:
            file = request.files['image']
            if file.filename == '':
                error = "No selected file"
            elif file:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                clear_upload_folder()
                file.save(filepath)
                uploaded_image = f"{UPLOAD_FOLDER}/{filename}"
                post_button = True
                try:
                    prediction = model_predict(filepath)
                except Exception as e:
                    error = f"Prediction error: {e}"

    return render_template(
        'index.html',
        prediction=prediction,
        error=error,
        uploaded_image=uploaded_image,
        show_post_buttons=post_button
    )

if __name__ == '__main__':
    app.run(debug=True)
