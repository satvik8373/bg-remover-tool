import os
from flask import Flask, request, render_template_string, url_for, jsonify
from rembg import remove

# Initialize Flask app
app = Flask(__name__)

# Directory paths for input and output images
output_dir = './static/output/'  # Ensure this is under the static folder

# Ensure that the static output folder exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Middleware to fix any proxy-related issues (e.g., when deploying to Heroku)
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

# Route for the index page with the form
@app.route('/')
def index():
    return render_template_string("""
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Background Remover</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f7fc;
                text-align: center;
                padding: 50px;
            }
            h1 {
                color: #4A90E2;
                font-size: 36px;
                margin-bottom: 20px;
            }
            .form-container {
                background-color: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                display: inline-block;
                width: 100%;
                max-width: 500px;
            }
            input[type="file"] {
                margin-bottom: 20px;
                padding: 10px;
                font-size: 16px;
            }
            button {
                background-color: #4A90E2;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 18px;
            }
            button:hover {
                background-color: #357ab7;
            }
        </style>
    </head>
    <body>
        <h1>Upload an Image to Remove Background</h1>
        <div class="form-container">
            <form action="/remove_bg" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*" required>
                <button type="submit">Upload Image</button>
            </form>
        </div>
    </body>
    </html>
    """)

# Function to remove the background
def remove_bg(input_data):
    return remove(input_data)

# Route to handle the background removal and show download link
@app.route('/remove_bg', methods=['POST'])
def remove_bg_api():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Process the image to remove the background
    input_data = file.read()
    output_data = remove_bg(input_data)

    # Save the output image in the static folder (output)
    output_path = os.path.join(output_dir, file.filename)
    with open(output_path, 'wb') as output_file:
        output_file.write(output_data)

    # Ensure the URL path to the output image is correct
    output_file_url = url_for('static', filename=f'output/{file.filename}')

    # Display a simple download link for the processed image
    return render_template_string("""
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image Background Removed</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f7fc;
                text-align: center;
                padding: 50px;
            }
            h1 {
                color: #4A90E2;
                font-size: 36px;
            }
            p {
                color: #7a7a7a;
                font-size: 18px;
            }
            a {
                display: inline-block;
                background-color: #4A90E2;
                color: white;
                padding: 15px 30px;
                font-size: 18px;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
                transition: background-color 0.3s ease;
            }
            a:hover {
                background-color: #357ab7;
            }
        </style>
    </head>
    <body>
        <h1>Background Removed Successfully!</h1>
        <p>You can download the processed image below:</p>
        <a href="{{ output_file_url }}" download>Download Image</a>
        <img src="{{ output_file_url }}" alt="Processed Image" style="margin-top: 20px; width: 50%;"/>
    </body>
    </html>
    """, output_file_url=output_file_url)

# Run the Flask app on the correct port (from environment variable)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to port 5000 if not set
    app.run(debug=True, host='0.0.0.0', port=port)
