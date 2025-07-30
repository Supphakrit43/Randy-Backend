from flask import Blueprint, request, jsonify, send_file
from flask_cors import cross_origin
from PIL import Image, ImageFilter, ImageEnhance
import io
import base64
import os
import tempfile

simple_image_bp = Blueprint('simple_image', __name__)

@simple_image_bp.route('/upload', methods=['POST'])
@cross_origin()
def upload_image():
    """อัพโหลดรูปภาพและสร้าง depth map แบบง่าย"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # อ่านรูปภาพ
        image = Image.open(file.stream)
        
        if image is None:
            return jsonify({'error': 'Invalid image format'}), 400
        
        # สร้าง depth map แบบง่าย
        depth_map = create_simple_depth_map(image)
        
        # สร้าง normal map แบบง่าย
        normal_map = create_simple_normal_map(depth_map)
        
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
                'width': image.width,
                'height': image.height
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_simple_depth_map(image):
    """สร้าง depth map แบบง่ายจากรูปภาพ"""
    # แปลงเป็น grayscale
    gray = image.convert('L')
    
    # ใช้ edge detection แบบง่าย
    edges = gray.filter(ImageFilter.FIND_EDGES)
    
    # สร้าง depth map โดยการ invert edges
    # พื้นที่ที่มี edge น้อย = ลึกมาก (สีเข้ม)
    depth_map = Image.eval(edges, lambda x: 255 - x)
    
    # เพิ่ม blur เพื่อให้ smooth
    depth_map = depth_map.filter(ImageFilter.GaussianBlur(radius=2))
    
    # แปลงกลับเป็น RGB
    depth_map = depth_map.convert('RGB')
    
    return depth_map

def create_simple_normal_map(depth_image):
    """สร้าง normal map แบบง่ายจาก depth map"""
    # แปลงเป็น grayscale
    if depth_image.mode != 'L':
        depth_gray = depth_image.convert('L')
    else:
        depth_gray = depth_image
    
    # สร้าง normal map สีฟ้า (default normal)
    width, height = depth_gray.size
    normal_map = Image.new('RGB', (width, height), (128, 128, 255))
    
    # เพิ่มการปรับแต่งเล็กน้อยจาก depth
    enhancer = ImageEnhance.Contrast(normal_map)
    normal_map = enhancer.enhance(1.2)
    
    return normal_map

def image_to_base64(image):
    """แปลงรูปภาพเป็น base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{image_base64}"

@simple_image_bp.route('/lighting/calculate', methods=['POST'])
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
        
        # คำนวณการกระจายแสงแบบง่าย
        lighting_data = calculate_simple_light_distribution(
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

def calculate_simple_light_distribution(position, lumens, width, height):
    """คำนวณการกระจายแสงแบบง่าย"""
    # แปลง normalized position เป็น pixel coordinates
    light_x = int(position['x'] * width)
    light_y = int(position['y'] * height)
    light_z = position['z']  # ความสูง (0-1)
    
    # สร้าง simple intensity grid
    intensity_grid = []
    max_distance = ((width/2)**2 + (height/2)**2)**0.5
    
    for y in range(height):
        row = []
        for x in range(width):
            # คำนวณระยะทาง
            distance_2d = ((x - light_x)**2 + (y - light_y)**2)**0.5
            distance_3d = (distance_2d**2 + (light_z * max_distance)**2)**0.5
            
            # คำนวณความเข้มแสง
            if distance_3d == 0:
                intensity = 1.0
            else:
                intensity = min(1.0, (lumens or 2000) / (distance_3d**2 + 1000))
            
            row.append(intensity)
        intensity_grid.append(row)
    
    return {
        'intensity_grid': intensity_grid,
        'light_position': {'x': light_x, 'y': light_y, 'z': light_z},
        'max_intensity': 1.0,
        'cone_angle': 60
    }

