from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import base64
import io

minimal_image_bp = Blueprint('minimal_image', __name__)

@minimal_image_bp.route('/upload', methods=['POST'])
@cross_origin()
def upload_image():
    """อัพโหลดรูปภาพและสร้าง mock depth map"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # อ่านรูปภาพเป็น bytes
        image_bytes = file.read()
        
        # สร้าง base64 ของรูปต้นฉบับ
        original_b64 = base64.b64encode(image_bytes).decode('utf-8')
        original_b64 = f"data:image/{file.filename.split('.')[-1]};base64,{original_b64}"
        
        # สร้าง mock depth map และ normal map (ใช้รูปเดิม)
        depth_b64 = original_b64
        normal_b64 = original_b64
        
        return jsonify({
            'success': True,
            'original_image': original_b64,
            'depth_map': depth_b64,
            'normal_map': normal_b64,
            'image_dimensions': {
                'width': 800,  # mock dimensions
                'height': 600
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@minimal_image_bp.route('/lighting/calculate', methods=['POST'])
@cross_origin()
def calculate_lighting():
    """คำนวณการกระจายแสงตามตำแหน่งและข้อมูลไฟ"""
    try:
        data = request.get_json()
        
        # ข้อมูลไฟ
        light_type = data.get('light_type', 'unknown')
        wattage = data.get('wattage', 100)
        lumens = data.get('lumens', 2000)
        
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
    
    # สร้าง simple intensity grid (ลดขนาดเพื่อประสิทธิภาพ)
    grid_width = min(50, width // 10)  # ลดความละเอียด
    grid_height = min(50, height // 10)
    
    intensity_grid = []
    max_distance = ((grid_width/2)**2 + (grid_height/2)**2)**0.5
    
    for y in range(grid_height):
        row = []
        for x in range(grid_width):
            # คำนวณระยะทาง
            actual_x = x * width / grid_width
            actual_y = y * height / grid_height
            distance_2d = ((actual_x - light_x)**2 + (actual_y - light_y)**2)**0.5
            distance_3d = (distance_2d**2 + (light_z * max_distance * 10)**2)**0.5
            
            # คำนวณความเข้มแสง
            if distance_3d == 0:
                intensity = 1.0
            else:
                intensity = min(1.0, (lumens or 2000) / (distance_3d**2 + 1000))
            
            row.append(round(intensity, 3))  # ปัดเศษเพื่อลดขนาดข้อมูล
        intensity_grid.append(row)
    
    return {
        'intensity_grid': intensity_grid,
        'light_position': {'x': light_x, 'y': light_y, 'z': light_z},
        'max_intensity': 1.0,
        'cone_angle': 60,
        'grid_dimensions': {'width': grid_width, 'height': grid_height}
    }

