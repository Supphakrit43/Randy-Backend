const express = require('express');
const aws = require('aws-sdk');
const multer = require('multer');
const multerS3 = require('multer-s3');
const router = express.Router();

// 1. สร้าง S3 Client โดยดึงค่าจาก Environment Variables ที่คุณตั้งบน Render
const s3 = new aws.S3({
    endpoint: process.env.R2_ENDPOINT, // <-- ดึงค่าจากตัวแปร R2_ENDPOINT
    accessKeyId: process.env.R2_ACCESS_KEY_ID, // <-- ดึงค่าจากตัวแปร R2_ACCESS_KEY_ID
    secretAccessKey: process.env.R2_SECRET_ACCESS_KEY, // <-- ดึงค่าจากตัวแปร R2_SECRET_ACCESS_KEY
    signatureVersion: 'v4',
});

// 2. ตั้งค่า Multer ให้ใช้ S3 Client นี้
const upload = multer({
    storage: multerS3({
        s3: s3,
        bucket: process.env.R2_BUCKET_NAME, // <-- ดึงค่าจากตัวแปร R2_BUCKET_NAME
        acl: 'public-read',
        key: function (req, file, cb) {
            cb(null, Date.now().toString() + '-' + file.originalname);
        }
    })
});

// 3. สร้าง Route สำหรับการอัปโหลด
const uploadRoutes = require('./routes/upload');
app.use('/api', uploadRoutes);
    if (!req.file) {
        return res.status(400).json({ error: 'No file uploaded.' });
    }
    res.status(200).json({ 
        message: 'File uploaded successfully',
        imageUrl: req.file.location 
    });
}, (error, req, res, next) => {
    res.status(400).json({error: error.message});
});

module.exports = router;
