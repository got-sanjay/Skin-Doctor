
const fileInput = document.getElementById('file-input');
const cameraInput = document.getElementById('camera-input');
const preview = document.getElementById('preview');
const imagePreview = document.getElementById('image-preview');
const uploadBox = document.getElementById('upload-box');
const uploadContainer = document.getElementById('upload-container');

function previewFile(file) {
    const reader = new FileReader();
    reader.onload = () => {
        preview.src = reader.result;
        imagePreview.style.display = 'block';
        uploadContainer.style.display = 'none'; 
    };
    reader.readAsDataURL(file);
}

fileInput.addEventListener('change', () => {
    if (fileInput.files[0]) {
        previewFile(fileInput.files[0])};
});

cameraInput.addEventListener('change', () => {
    if (cameraInput.files[0]) {
        previewFile(cameraInput.files[0]);
        }
});

uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        fileInput.files = e.dataTransfer.files;
        previewFile(file);
    }
});

