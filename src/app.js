const express = require('express');
const multer = require('multer');
const documentController = require('./controllers/document.controller');

const app = express();
const port = 3000;

app.use(express.json());

const upload = multer({ dest: '../uploads' });

app.post('/generate', upload.single('template'), documentController.generateDocument);

app.listen(port, () => {
    console.log(`[Server] API running at http://localhost:${port}`);
});
