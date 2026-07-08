"""
API Interface for Facial Biometric Key Generation System
Provides REST endpoints for key generation and user management
"""

from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
from facial_keygen_system import ProductionKeygenSystem
import json
import os

app = Flask(__name__)
system = ProductionKeygenSystem()

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)


@app.route('/api/health', methods=['GET'])
def health_check():
    """System health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'system': 'Facial Biometric Key Generation System',
        'version': '1.0.0'
    })


@app.route('/api/process', methods=['POST'])
def process_biometric():
    """
    Process facial biometric data for key generation or retrieval
    
    Expected input:
    {
        "image": "base64_encoded_image",
        "user_id": "optional_user_id"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'Image data required'}), 400
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'])
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'error': 'Invalid image format'}), 400
        
        # Process user
        user_id = data.get('user_id')
        result = system.process_user(image, user_id)
        
        # Prepare response (excluding full key data for security)
        response = {
            'status': result['status'],
            'user_id': result.get('user_id'),
            'message': result['message']
        }
        
        if result['status'] in ['existing_user', 'new_user_registered']:
            keys = result['keys']
            response['keys'] = {
                'primary_key_hash': keys['hash_key'][:16],
                'key_length': len(keys['primary_key']),
                'generation_metadata': keys.get('metadata', {})
            }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500


@app.route('/api/users', methods=['GET'])
def list_users():
    """List all registered users"""
    try:
        templates_dir = config['system_config']['recognition_system']['templates_directory']
        
        if not os.path.exists(templates_dir):
            return jsonify({'users': []})
        
        users = []
        for filename in os.listdir(templates_dir):
            if filename.endswith('.json'):
                user_id = filename[:-5]  # Remove .json extension
                
                with open(os.path.join(templates_dir, filename), 'r') as f:
                    template_data = json.load(f)
                
                users.append({
                    'user_id': user_id,
                    'registered': template_data.get('timestamp'),
                    'templates_count': len(template_data.get('feature_sets', []))
                })
        
        return jsonify({'users': users})
        
    except Exception as e:
        return jsonify({'error': f'Failed to list users: {str(e)}'}), 500


@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a registered user"""
    try:
        templates_dir = config['system_config']['recognition_system']['templates_directory']
        keys_dir = config['system_config']['key_storage']['storage_directory']
        
        # Delete template file
        template_path = os.path.join(templates_dir, f"{user_id}.json")
        if os.path.exists(template_path):
            os.remove(template_path)
        
        # Delete key file
        key_path = os.path.join(keys_dir, f"{user_id}_keys.json")
        if os.path.exists(key_path):
            os.remove(key_path)
        
        return jsonify({
            'status': 'success',
            'message': f'User {user_id} deleted successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to delete user: {str(e)}'}), 500


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current system configuration"""
    return jsonify(config)


if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs(config['system_config']['recognition_system']['templates_directory'], exist_ok=True)
    os.makedirs(config['system_config']['key_storage']['storage_directory'], exist_ok=True)
    
    print("🚀 Starting Facial Biometric Key Generation API Server")
    print("📍 Available endpoints:")
    print("   GET  /api/health - System health check")
    print("   POST /api/process - Process biometric data")
    print("   GET  /api/users - List registered users")
    print("   DELETE /api/users/<user_id> - Delete user")
    print("   GET  /api/config - Get system configuration")
    
    app.run(host='0.0.0.0', port=5000, debug=False)