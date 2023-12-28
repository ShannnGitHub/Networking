const express = require('express');
const multer = require('multer');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;

const allowedExtensions = ['png', 'jpg', 'jpeg', 'txt', 'mp4'];

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, path.join(__dirname, 'uploads')); // Specify the destination folder
    },
    filename: function (req, file, cb) {
        // Generate a unique filename
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        const fileExtension = file.originalname.split('.').pop().toLowerCase();
        cb(null, file.fieldname + '-' + uniqueSuffix + '.' + fileExtension);
    },
});

const upload = multer({ storage: storage, limits: { fileSize: 5 * 1024 * 1024 } }); // 5 MB limit

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/upload', upload.fields([{ name: 'image' }, { name: 'text' }, { name: 'video' }]), (req, res) => {
    const files = req.files;

    // Check if at least one file is present in the request
    if (!files['image'] && !files['text'] && !files['video']) {
        return res.send('No file part');
    }

    // Check each file individually and handle it if present
    for (const fileType of ['image', 'text', 'video']) {
        const file = files[fileType];

        if (file) {
            // Validate file type
            const fileExtension = file.originalname.split('.').pop().toLowerCase();
            if (!allowedExtensions.includes(fileExtension)) {
                return res.send(`Invalid ${fileType} file type`);
            }

            // The file has already been saved to the specified destination folder

            console.log(`${fileType.capitalize()} File Name:`, file.filename);
        }
    }

    return res.send('Files uploaded successfully!');
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
