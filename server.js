require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const connectDB = require('./config/db'); // สมมติว่าคุณสร้างไฟล์ db.js ไว้
const errorHandler = require('./middleware/errorHandler'); // สมมติว่าคุณสร้างไฟล์ errorHandler.js ไว้

// เชื่อมต่อ Database
connectDB();

const app = express();

// ตั้งค่า CORS
app.use(cors({
  origin: ['http://localhost:3000', 'https://randy-frontend.onrender.com'],
}));

// Middleware
app.use(express.json());

// Error Handling Middleware (ต้องอยู่ล่างสุด)
app.use(errorHandler);

// ตั้งค่า Port และ Host
const PORT = process.env.PORT || 5000;
app.listen(PORT, '0.0.0.0', () => console.log(`Server running on port ${PORT}`));

// ส่วนที่ 1: เพิ่มด้านบนของไฟล์เพื่อ import เข้ามา
const uploadRoutes = require('./routes/upload');

// ... โค้ดอื่นๆ ของคุณ ...

// ส่วนที่ 2: เพิ่มก่อนบรรทัด app.listen เพื่อใช้งาน
// เป็นการบอกว่าถ้ามี request มาที่ /api/… ให้ส่งไปที่ uploadRoutes
app.use('/api', uploadRoutes);

// ... app.listen(...) ...
