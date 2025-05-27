# app.py
from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from test import model_predict,API_KEY
from openai import OpenAI


app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploaded_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
client = OpenAI(api_key=API_KEY)
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
            
def generate_suggestion(diagnosis):
    prompt = f"What advice would you give to a patient diagnosed with {diagnosis}? Provide medical suggestions, treatment advice, or when to see a doctor."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a medical assistant providing safe and responsible advice for skin conditions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.5
        )
        suggestion = response.choices[0].message.content.strip()
        return suggestion
    except Exception as e:
        return f"Error generating suggestion: {e}"


@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    error = None
    uploaded_image = ''
    post_button = False
    suggestion = ''
    confidence= -1
    
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
                    prediction,confidence = model_predict(filepath)
                    suggestion = generate_suggestion(prediction)
                except Exception as e:
                    error = f"Prediction error: {e}"

    return render_template(
        'index.html',
        prediction=prediction,
        confidence=confidence,
        error=error,
        uploaded_image=uploaded_image,
        show_post_buttons=post_button,
        suggestion=suggestion
    )


if __name__ == '__main__':
    app.run(debug=True)
