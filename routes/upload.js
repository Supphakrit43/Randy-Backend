const express = require('express');
const router = express.Router();
const upload = require('../middleware/multer'); // เรียกใช้ multer ที่เราสร้างไว้
const Image = require('../models/image');     // เรียกใช้ Model Schema

// Endpoint สำหรับ POST /api/upload
router.post('/', (req, res, next) => {
  upload.single('file')(req, res, (err) => {
    if (err) {
      return next(err); // ถ้ามี error ให้ส่งไปที่ errorHandler
    }
    if (!req.file) {
      return res.status(400).json({ message: 'No file uploaded.' });
    }

    const newImage = new Image({
      imageUrl: req.file.path,
      publicId: req.file.filename
    });

    newImage.save()
      .then(savedImage => {
        res.status(201).json({
          message: 'File uploaded successfully!',
          imageUrl: savedImage.imageUrl
        });
      })
      .catch(dbError => next(dbError));
  });
});

module.exports = router;