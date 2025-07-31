from flask import Blueprint, request, jsonify, send_file
from flask_cors import cross_origin
import cv2
import numpy as np
from PIL import Image
import io
import base64
import os
import tempfile

image_bp = Blueprint('image', __name__)

@image_bp.route('/upload', methods=['POST'])
@cross_origin()
def upload_image():
    """อัพโหลดรูปภาพและสร้าง depth map"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # อ่านรูปภาพ
        image_bytes = file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'error': 'Invalid image format'}), 400
        
        # สร้าง depth map
        depth_map = create_depth_map(image)
        
        # สร้าง normal map
        normal_map = create_normal_map(depth_map)
        
        # แปลงเป็น base64 สำหรับส่งกลับ
        original_b64 = image_to_base64(image)
        depth_b64 = image_to_base64(depth_map)
        normal_b64 = image_to_base64(normal_map)
        
        return jsonify({
            'success': True,
            'original_image': original_b64,
            'depth_map': depth_b64,
            'normal_map': normal_b64,
            'image_dimensions': {
                'width': image.shape[1],
                'height': image.shape[0]
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_depth_map(image):
    """สร้าง depth map จากรูปภาพ 2D"""
    # แปลงเป็น grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # ใช้ Gaussian blur เพื่อลด noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # ใช้ Sobel operator เพื่อหา edges
    sobel_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    
    # คำนวณ gradient magnitude
    gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    
    # Normalize เป็น 0-255
    gradient_magnitude = np.uint8(255 * gradient_magnitude / np.max(gradient_magnitude))
    
    # สร้าง depth map โดยใช้ inverse ของ gradient
    # พื้นที่ที่มี edge น้อย = ลึกมาก (สีเข้ม)
    # พื้นที่ที่มี edge เยอะ = ตื้น (สีอ่อน)
    depth_map = 255 - gradient_magnitude
    
    # ใช้ morphological operations เพื่อปรับปรุง
    kernel = np.ones((3,3), np.uint8)
    depth_map = cv2.morphologyEx(depth_map, cv2.MORPH_CLOSE, kernel)
    depth_map = cv2.morphologyEx(depth_map, cv2.MORPH_OPEN, kernel)
    
    # ใช้ bilateral filter เพื่อ smooth แต่รักษา edges
    depth_map = cv2.bilateralFilter(depth_map, 9, 75, 75)
    
    # แปลงเป็น 3 channels สำหรับ display
    depth_map_colored = cv2.applyColorMap(depth_map, cv2.COLORMAP_JET)
    
    return depth_map_colored

def create_normal_map(depth_map):
    """สร้าง normal map จาก depth map"""
    # แปลง depth map เป็น grayscale
    if len(depth_map.shape) == 3:
        depth_gray = cv2.cvtColor(depth_map, cv2.COLOR_BGR2GRAY)
    else:
        depth_gray = depth_map
    
    # คำนวณ gradients
    grad_x = cv2.Sobel(depth_gray, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(depth_gray, cv2.CV_32F, 0, 1, ksize=3)
    
    # สร้าง normal vectors
    # X component (red channel)
    normal_x = grad_x / 255.0
    
    # Y component (green channel) 
    normal_y = grad_y / 255.0
    
    # Z component (blue channel) - คำนวณจาก X และ Y
    normal_z = np.sqrt(np.maximum(0, 1 - normal_x**2 - normal_y**2))
    
    # แปลงเป็น 0-255 range
    normal_x = ((normal_x + 1) * 127.5).astype(np.uint8)
    normal_y = ((normal_y + 1) * 127.5).astype(np.uint8)
    normal_z = (normal_z * 255).astype(np.uint8)
    
    # รวม channels
    normal_map = cv2.merge([normal_z, normal_y, normal_x])  # BGR format
    
    return normal_map

def image_to_base64(image):
    """แปลงรูปภาพเป็น base64 string"""
    _, buffer = cv2.imencode('.png', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/png;base64,{image_base64}"

@image_bp.route('/lighting/calculate', methods=['POST'])
@cross_origin()
def calculate_lighting():
    """คำนวณการกระจายแสงตามตำแหน่งและข้อมูลไฟ"""
    try:
        data = request.get_json()
        
        # ข้อมูลไฟ
        light_type = data.get('light_type')
        wattage = data.get('wattage')
        lumens = data.get('lumens')
        
        # ตำแหน่งไฟ (normalized coordinates 0-1)
        position = data.get('position', {'x': 0.5, 'y': 0.5, 'z': 0.8})
        
        # ขนาดรูปภาพ
        image_width = data.get('image_width', 800)
        image_height = data.get('image_height', 600)
        
        # คำนวณการกระจายแสง
        lighting_data = calculate_light_distribution(
            position, lumens, image_width, image_height
        )
        
        return jsonify({
            'success': True,
            'lighting_data': lighting_data,
            'light_info': {
                'type': light_type,
                'wattage': wattage,
                'lumens': lumens,
                'position': position
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_light_distribution(position, lumens, width, height):
    """คำนวณการกระจายแสงในรูปแบบ cone"""
    # แปลง normalized position เป็น pixel coordinates
    light_x = int(position['x'] * width)
    light_y = int(position['y'] * height)
    light_z = position['z']  # ความสูง (0-1)
    
    # สร้าง grid สำหรับคำนวณ
    y_coords, x_coords = np.mgrid[0:height, 0:width]
    
    # คำนวณระยะทางจากแหล่งแสง
    distance_2d = np.sqrt((x_coords - light_x)**2 + (y_coords - light_y)**2)
    distance_3d = np.sqrt(distance_2d**2 + (light_z * max(width, height))**2)
    
    # คำนวณความเข้มแสงตาม inverse square law
    # I = I0 / (distance^2)
    max_distance = np.sqrt(width**2 + height**2)
    normalized_distance = distance_3d / max_distance
    
    # ป้องกันการหารด้วย 0
    normalized_distance = np.maximum(normalized_distance, 0.01)
    
    # คำนวณความเข้มแสง
    intensity = lumens / (normalized_distance**2)
    
    # Normalize เป็น 0-1
    intensity = intensity / np.max(intensity)
    
    # สร้าง cone effect
    cone_angle = 60  # องศา
    cone_radius = distance_2d / (light_z * max(width, height)) if light_z > 0 else distance_2d
    cone_factor = np.exp(-cone_radius**2 / (2 * (cone_angle/180)**2))
    
    # รวม intensity และ cone effect
    final_intensity = intensity * cone_factor
    
    # แปลงเป็น list สำหรับ JSON
    lighting_grid = final_intensity.tolist()
    
    return {
        'intensity_grid': lighting_grid,
        'light_position': {'x': light_x, 'y': light_y, 'z': light_z},
        'max_intensity': float(np.max(final_intensity)),
        'cone_angle': cone_angle
    }

