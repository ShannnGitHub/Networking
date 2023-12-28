from flask import Flask, render_template, request
import os

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'txt', 'mp4'}  # Add or modify allowed file extensions

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Check if at least one file is present in the request
    if 'image' not in request.files and 'text' not in request.files and 'video' not in request.files:
        return 'No file part'

    # Check each file individually and handle it if present
    for file_type in ['image', 'text', 'video']:
        if file_type in request.files:
            file = request.files[file_type]

            # Validate file type
            if not allowed_file(file.filename):
                return f'Invalid {file_type} file type'

            # Validate file size (adjust the limit as needed)
            if len(file.read()) > 5 * 1024 * 1024:  # 5 MB limit
                return f'{file_type} file size exceeds the limit'

            # Save the file to a secure location (modify the path as needed)
            file.save(os.path.join('/path/to/uploaded/files/', file.filename))
            print(f'{file_type.capitalize()} File Name:', file.filename)

    return 'Files uploaded successfully!'

if __name__ == '__main__':
    app.run(debug=True)
