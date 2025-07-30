from flask import Blueprint, jsonify
from flask_cors import cross_origin

products_bp = Blueprint('products', __name__)

# ข้อมูลผลิตภัณฑ์ Randy Thailand
PRODUCT_DATA = {
    "categories": [
        {
            "id": "spotlight_solar",
            "name": "ไฟสปอตไลท์โซล่าเซลล์",
            "icon": "spotlight",
            "products": [
                {
                    "id": "diamond",
                    "name": "Diamond",
                    "models": []  # จะเพิ่มข้อมูลเมื่อมีรายละเอียด
                },
                {
                    "id": "street_m_series",
                    "name": "ไฟถนน220V M Series",
                    "models": []
                },
                {
                    "id": "street_p_series", 
                    "name": "ไฟถนน220V P Series",
                    "models": []
                },
                {
                    "id": "street_r_series",
                    "name": "ไฟถนน220V R Series", 
                    "models": []
                },
                {
                    "id": "galaxy",
                    "name": "Galaxy",
                    "models": []
                },
                {
                    "id": "space_light",
                    "name": "Space Light",
                    "models": [
                        {
                            "id": "dw_ssth800",
                            "name": "DW-SSTH800",
                            "wattage": 800,
                            "lumens": 2550,
                            "description": "Starship III 800W"
                        },
                        {
                            "id": "dw_ssth1200", 
                            "name": "DW-SSTH1200",
                            "wattage": 1200,
                            "lumens": 3840,
                            "description": "Starship III 1200W"
                        }
                    ]
                },
                {
                    "id": "spectrum",
                    "name": "Spectrum",
                    "models": []
                },
                {
                    "id": "sport_d",
                    "name": "Sport D", 
                    "models": []
                },
                {
                    "id": "sport_x",
                    "name": "Sport X",
                    "models": []
                },
                {
                    "id": "sport_x_camera",
                    "name": "Sport X Camera",
                    "models": []
                },
                {
                    "id": "super_lumens",
                    "name": "Super Lumens",
                    "models": []
                },
                {
                    "id": "super_lumens_cctv",
                    "name": "Super Lumens CCTV",
                    "models": []
                },
                {
                    "id": "ufo",
                    "name": "UFO",
                    "models": [
                        {
                            "id": "dw_ew800",
                            "name": "DW-EW800",
                            "wattage": 800,
                            "lumens": 2029,
                            "description": "Explorer Warrior 800W"
                        },
                        {
                            "id": "dw_ew1200",
                            "name": "DW-EW1200", 
                            "wattage": 1200,
                            "lumens": 2679,
                            "description": "Explorer Warrior 1200W"
                        }
                    ]
                },
                {
                    "id": "ultra",
                    "name": "Ultra",
                    "models": [
                        {
                            "id": "dw_xj_801",
                            "name": "DW-XJ-801",
                            "wattage": 100,
                            "lumens": 1485,
                            "description": "Interstellar Warrior 100W"
                        },
                        {
                            "id": "dw_xj_802",
                            "name": "DW-XJ-802",
                            "wattage": 200,
                            "lumens": 2000,
                            "description": "Interstellar Warrior 200W"
                        },
                        {
                            "id": "dw_xj_803",
                            "name": "DW-XJ-803",
                            "wattage": 300,
                            "lumens": 2552,
                            "description": "Interstellar Warrior 300W"
                        },
                        {
                            "id": "dw_xj_804",
                            "name": "DW-XJ-804",
                            "wattage": 400,
                            "lumens": 3168,
                            "description": "Interstellar Warrior 400W"
                        },
                        {
                            "id": "dw_xj_1200",
                            "name": "DW-XJ-1200",
                            "wattage": 1200,
                            "lumens": 5500,
                            "description": "Interstellar Warrior 1200W"
                        }
                    ]
                },
                {
                    "id": "ultra_pro",
                    "name": "Ultra Pro",
                    "models": [
                        {
                            "id": "dw_xj902",
                            "name": "DW-XJ902",
                            "wattage": 200,
                            "lumens": 1800,
                            "description": "Interstellar Warrior II"
                        },
                        {
                            "id": "dw_xj903",
                            "name": "DW-XJ903",
                            "wattage": 300,
                            "lumens": 2650,
                            "description": "Interstellar Warrior II"
                        },
                        {
                            "id": "dw_xj904",
                            "name": "DW-XJ904",
                            "wattage": 400,
                            "lumens": 3358,
                            "description": "Interstellar Warrior II"
                        },
                        {
                            "id": "dw_xj905",
                            "name": "DW-XJ905",
                            "wattage": 500,
                            "lumens": 3512,
                            "description": "Interstellar Warrior II"
                        },
                        {
                            "id": "dw_xj906",
                            "name": "DW-XJ906",
                            "wattage": 600,
                            "lumens": 3840,
                            "description": "Interstellar Warrior II"
                        }
                    ]
                },
                {
                    "id": "electrum_220v",
                    "name": "Electrum 220V",
                    "models": []
                }
            ]
        },
        {
            "id": "home_lights",
            "name": "ไฟบ้าน",
            "icon": "home",
            "products": [
                {
                    "id": "newblack",
                    "name": "NewBlack",
                    "models": [
                        {
                            "id": "dw_lh9090",
                            "name": "DW-LH9090",
                            "wattage": 90,
                            "lumens": 994,
                            "description": "Intrepid Pioneer II 90W"
                        },
                        {
                            "id": "dw_lh9150",
                            "name": "DW-LH9150",
                            "wattage": 150,
                            "lumens": 1476,
                            "description": "Intrepid Pioneer II 150W"
                        },
                        {
                            "id": "dw_lh9250",
                            "name": "DW-LH9250",
                            "wattage": 250,
                            "lumens": 1970,
                            "description": "Intrepid Pioneer II 250W"
                        },
                        {
                            "id": "dw_lh9350",
                            "name": "DW-LH9350",
                            "wattage": 350,
                            "lumens": 2488,
                            "description": "Intrepid Pioneer II 350W"
                        }
                    ]
                }
            ]
        }
    ]
}

@products_bp.route('/categories', methods=['GET'])
@cross_origin()
def get_categories():
    """ดึงรายการหมวดหมู่ผลิตภัณฑ์"""
    try:
        categories = []
        for category in PRODUCT_DATA['categories']:
            categories.append({
                'id': category['id'],
                'name': category['name'],
                'icon': category['icon'],
                'product_count': len(category['products'])
            })
        
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/category/<category_id>/products', methods=['GET'])
@cross_origin()
def get_products_by_category(category_id):
    """ดึงรายการผลิตภัณฑ์ตามหมวดหมู่"""
    try:
        category = None
        for cat in PRODUCT_DATA['categories']:
            if cat['id'] == category_id:
                category = cat
                break
        
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        products = []
        for product in category['products']:
            products.append({
                'id': product['id'],
                'name': product['name'],
                'model_count': len(product['models'])
            })
        
        return jsonify({
            'success': True,
            'category': {
                'id': category['id'],
                'name': category['name']
            },
            'products': products
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/product/<product_id>/models', methods=['GET'])
@cross_origin()
def get_product_models(product_id):
    """ดึงรายการรุ่นของผลิตภัณฑ์"""
    try:
        product = None
        category_name = None
        
        for category in PRODUCT_DATA['categories']:
            for prod in category['products']:
                if prod['id'] == product_id:
                    product = prod
                    category_name = category['name']
                    break
            if product:
                break
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({
            'success': True,
            'product': {
                'id': product['id'],
                'name': product['name'],
                'category': category_name
            },
            'models': product['models']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/model/<model_id>', methods=['GET'])
@cross_origin()
def get_model_details(model_id):
    """ดึงรายละเอียดของรุ่นผลิตภัณฑ์"""
    try:
        model = None
        product_name = None
        category_name = None
        
        for category in PRODUCT_DATA['categories']:
            for product in category['products']:
                for mod in product['models']:
                    if mod['id'] == model_id:
                        model = mod
                        product_name = product['name']
                        category_name = category['name']
                        break
                if model:
                    break
            if model:
                break
        
        if not model:
            return jsonify({'error': 'Model not found'}), 404
        
        return jsonify({
            'success': True,
            'model': model,
            'product_name': product_name,
            'category_name': category_name
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/search', methods=['GET'])
@cross_origin()
def search_products():
    """ค้นหาผลิตภัณฑ์"""
    try:
        from flask import request
        query = request.args.get('q', '').lower()
        
        if not query:
            return jsonify({'error': 'Search query required'}), 400
        
        results = []
        
        for category in PRODUCT_DATA['categories']:
            for product in category['products']:
                # ค้นหาในชื่อผลิตภัณฑ์
                if query in product['name'].lower():
                    results.append({
                        'type': 'product',
                        'id': product['id'],
                        'name': product['name'],
                        'category': category['name'],
                        'model_count': len(product['models'])
                    })
                
                # ค้นหาในรุ่นผลิตภัณฑ์
                for model in product['models']:
                    if (query in model['name'].lower() or 
                        query in model['description'].lower()):
                        results.append({
                            'type': 'model',
                            'id': model['id'],
                            'name': model['name'],
                            'product_name': product['name'],
                            'category': category['name'],
                            'wattage': model['wattage'],
                            'lumens': model['lumens'],
                            'description': model['description']
                        })
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

