from flask import Flask, render_template, request, redirect, url_for,jsonify
import os
app = Flask(__name__)


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
                pass
                try:
                    pass
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
@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy", "memory_mb": get_memory_usage()})

def get_memory_usage():
    """Get current memory usage in MB"""
    try:
        import psutil
        process = psutil.Process(os.getpid())
        return round(process.memory_info().rss / 1024 / 1024, 2)
    except:
        return "N/A"

if __name__ == '__main__':
    try:
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    except (KeyboardInterrupt, SystemExit):
        pass