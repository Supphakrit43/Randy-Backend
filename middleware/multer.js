const multer = require('multer');
const { CloudinaryStorage } = require('multer-storage-cloudinary');
const cloudinary = require('cloudinary').v2;

// ตั้งค่า Cloudinary โดยดึงค่ามาจากไฟล์ .env
cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
});

// กำหนดค่า Storage ให้ไปที่ Cloudinary
const storage = new CloudinaryStorage({
  cloudinary: cloudinary,
  params: {
    folder: 'randy-app-uploads', // ชื่อโฟลเดอร์ใน Cloudinary ที่จะเก็บไฟล์
    allowed_formats: ['jpeg', 'png', 'jpg'], // อนุญาตเฉพาะไฟล์รูปภาพ
  },
});

// สร้าง upload middleware
const upload = multer({
  storage: storage,
  limits: { fileSize: 1024 * 1024 * 5 }, // จำกัดขนาดไฟล์ไม่เกิน 5MB
});

module.exports = upload;