const { MulterError } = require('multer');

const errorHandler = (err, req, res, next) => {
  console.error("ERROR:", err.stack); // แสดง error ทั้งหมดเพื่อการดีบัก

  if (err instanceof MulterError) {
    return res.status(400).json({
      message: `File upload error: ${err.message}`,
    });
  }

  // จัดการ Error อื่นๆ
  return res.status(500).json({
    message: err.message || 'An internal server error occurred.',
  });
};

module.exports = errorHandler;