from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Check if the post request has the file part
    if 'image' not in request.files or 'text' not in request.files or 'video' not in request.files:
        return 'No file part'

    image = request.files['image']
    text = request.files['text']
    video = request.files['video']

    # You can handle each file as needed (save to disk, process, etc.)
    # For simplicity, we'll just print the file names here
    print("Image File Name:", image.filename)
    print("Text File Name:", text.filename)
    print("Video File Name:", video.filename)

    return 'Files uploaded successfully!'

if __name__ == '__main__':
    app.run(debug=True)
