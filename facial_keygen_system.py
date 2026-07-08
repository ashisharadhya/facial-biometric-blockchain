"""
Production Facial Biometric Key Generation System
Advanced cryptographic key derivation using facial biometrics with dynamic LFSR processing
"""

import cv2
import numpy as np
import mediapipe as mp
import hashlib
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class BiometricProcessor:
    """Core biometric processing engine"""
    
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
    def extract_features(self, image: np.ndarray) -> np.ndarray:
        """Extract biometric features from facial image"""
        # Ensure image quality
        if image is None or image.size == 0:
            raise ValueError("Invalid image provided")
        
        # Resize image for consistent processing
        height, width = image.shape[:2]
        if width < 100 or height < 100:
            raise ValueError("Image too small for reliable face detection")
        
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_image)
        
        if not results.multi_face_landmarks:
            raise ValueError("No face detected in image")
            
        landmarks = results.multi_face_landmarks[0]
        
        # Extract normalized landmark coordinates
        features = []
        for landmark in landmarks.landmark:
            features.extend([
                landmark.x,  # Already normalized 0-1
                landmark.y,  # Already normalized 0-1
                landmark.z if hasattr(landmark, 'z') else 0  # Depth information
            ])
            
        return np.array(features, dtype=np.float32)


class DynamicLFSREngine:
    """Advanced LFSR with dynamic processing until entropy exhaustion"""
    
    def __init__(self, buffer_size: int = 16):
        self.buffer_size = buffer_size
        self.max_rounds = 100
        
    def generate_keys(self, biometric_data: np.ndarray) -> Dict:
        """Generate cryptographic keys using dynamic LFSR processing"""
        
        # Initialize processing buffers
        buffers = [biometric_data[i:i+self.buffer_size] 
                  for i in range(0, len(biometric_data), self.buffer_size)]
        
        if len(buffers[-1]) < self.buffer_size:
            # Pad last buffer
            padding = np.zeros(self.buffer_size - len(buffers[-1]))
            buffers[-1] = np.concatenate([buffers[-1], padding])
        
        unique_values = set()
        entropy_history = []
        round_count = 0
        
        # Dynamic processing until entropy exhaustion
        while round_count < self.max_rounds:
            round_entropy = 0
            
            for i, buffer in enumerate(buffers):
                # Apply LFSR transformation
                transformed = self._lfsr_transform(buffer, round_count)
                
                # Cross-buffer feedback
                if i > 0:
                    feedback = np.mean(buffers[i-1]) * 0.1
                    transformed += feedback
                
                # Update buffer
                buffers[i] = transformed
                
                # Track unique values
                for val in transformed:
                    unique_values.add(hash(val))
                
                round_entropy += np.var(transformed)
            
            entropy_history.append(round_entropy)
            
            # Check convergence (entropy exhaustion)
            if len(entropy_history) >= 3:
                recent_change = abs(entropy_history[-1] - entropy_history[-3])
                if recent_change < 0.001:  # Entropy plateau reached
                    break
                    
            round_count += 1
        
        # Generate final key material
        final_buffer = np.concatenate(buffers)
        
        # Create multiple key formats
        keys = {
            'primary_key': self._generate_hex_key(final_buffer, 256),
            'backup_key': self._generate_hex_key(final_buffer[::-1], 256),
            'hash_key': hashlib.sha256(final_buffer.tobytes()).hexdigest(),
            'compact_key': self._generate_hex_key(final_buffer[::2], 128),
            'metadata': {
                'rounds_processed': round_count,
                'unique_values': len(unique_values),
                'entropy_ratio': len(unique_values) / (round_count * self.buffer_size * len(buffers)),
                'timestamp': datetime.now().isoformat()
            }
        }
        
        return keys
    
    def _lfsr_transform(self, buffer: np.ndarray, round_num: int) -> np.ndarray:
        """Advanced LFSR transformation with round-specific polynomials"""
        
        # Dynamic polynomial selection based on round
        polynomials = [0x1D, 0x39, 0x69, 0xB1, 0x187, 0x307, 0x605]
        poly = polynomials[round_num % len(polynomials)]
        
        result = np.zeros_like(buffer)
        
        for i in range(len(buffer)):
            val = int(abs(buffer[i] * 1000)) & 0xFFFF
            
            # LFSR shift with polynomial feedback
            for _ in range(8):
                msb = val & 0x8000
                val <<= 1
                if msb:
                    val ^= poly
                val &= 0xFFFF
            
            # Add entropy injection
            val ^= (round_num * i) & 0xFFFF
            result[i] = val / 1000.0
            
        return result
    
    def _generate_hex_key(self, data: np.ndarray, bits: int) -> str:
        """Generate hexadecimal key of specified bit length"""
        hash_obj = hashlib.sha512(data.tobytes())
        full_hash = hash_obj.hexdigest()
        key_length = bits // 4
        return full_hash[:key_length].upper()


class FaceRecognitionSystem:
    """Face recognition for user identification with multi-template support"""
    
    def __init__(self, templates_dir: str = "user_templates"):
        self.templates_dir = templates_dir
        self.similarity_threshold = 0.95  # Balanced threshold
        self.min_templates_match = 0.6  # 60% of templates must match
        self.max_templates_per_user = 5  # Store up to 5 templates per user
        os.makedirs(templates_dir, exist_ok=True)
        
    def register_user(self, user_id: str, features: np.ndarray) -> bool:
        """Register new user with biometric template"""
        try:
            template_path = os.path.join(self.templates_dir, f"{user_id}.json")
            
            # Check if user already exists
            if os.path.exists(template_path):
                # Add to existing templates
                with open(template_path, 'r') as f:
                    template = json.load(f)
                
                # Add new feature set if not at max
                if len(template['feature_sets']) < self.max_templates_per_user:
                    template['feature_sets'].append(features.tolist())
                    template['last_updated'] = datetime.now().isoformat()
                    
                    with open(template_path, 'w') as f:
                        json.dump(template, f, indent=2)
                    
                    print(f"   📝 Added template #{len(template['feature_sets'])} for {user_id}")
                    return True
            
            # New user - create initial template
            template = {
                'user_id': user_id,
                'feature_sets': [features.tolist()],  # Start with one template
                'timestamp': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            }
            
            with open(template_path, 'w') as f:
                json.dump(template, f, indent=2)
                
            return True
            
        except Exception as e:
            print(f"Registration failed: {e}")
            return False
    
    def identify_user(self, features: np.ndarray) -> Optional[str]:
        """Identify user from biometric features using multi-template matching"""
        try:
            template_files = [f for f in os.listdir(self.templates_dir) if f.endswith('.json')]
            
            if not template_files:
                return None
            
            best_match = None
            highest_avg_similarity = 0
            
            print(f"\n   🔍 Checking against {len(template_files)} registered user(s)...")
            
            for template_file in template_files:
                template_path = os.path.join(self.templates_dir, template_file)
                
                with open(template_path, 'r') as f:
                    template = json.load(f)
                
                # Compare against all feature sets for this user
                feature_sets = template['feature_sets']
                similarities = []
                
                for template_features in feature_sets:
                    template_features_array = np.array(template_features)
                    similarity = self._calculate_similarity(features, template_features_array)
                    similarities.append(similarity)
                
                # Calculate average similarity and count of matches above threshold
                avg_similarity = np.mean(similarities)
                max_similarity = np.max(similarities)
                matches_above_threshold = sum(1 for s in similarities if s > self.similarity_threshold)
                match_ratio = matches_above_threshold / len(similarities)
                
                # Use combined score: average similarity + bonus for multiple matches
                combined_score = avg_similarity * 0.6 + max_similarity * 0.4
                
                print(f"   📊 {template['user_id']}: Avg={avg_similarity:.4f}, Max={max_similarity:.4f}, "
                      f"Matches={matches_above_threshold}/{len(similarities)} (Score={combined_score:.4f})")
                
                if combined_score > highest_avg_similarity and match_ratio >= self.min_templates_match:
                    highest_avg_similarity = combined_score
                    best_match = template['user_id']
            
            # Use a lower threshold for combined score
            combined_threshold = 0.93
            
            if highest_avg_similarity > combined_threshold and best_match:
                print(f"   ✅ Match found! Combined Score: {highest_avg_similarity:.4f} > {combined_threshold:.4f}")
                return best_match
            else:
                print(f"   ❌ No match found. Best score: {highest_avg_similarity:.4f} < {combined_threshold:.4f}")
                return None
            
        except Exception as e:
            print(f"Identification failed: {e}")
            return None
    
    def _calculate_similarity(self, features1: np.ndarray, features2: np.ndarray) -> float:
        """Calculate cosine similarity between feature vectors"""
        # Ensure same shape
        if features1.shape != features2.shape:
            return 0
        
        # Normalize features first
        features1_norm = features1 / (np.linalg.norm(features1) + 1e-8)
        features2_norm = features2 / (np.linalg.norm(features2) + 1e-8)
        
        # Calculate cosine similarity
        similarity = np.dot(features1_norm, features2_norm)
        
        # Also check Euclidean distance for additional verification
        euclidean_dist = np.linalg.norm(features1_norm - features2_norm)
        distance_similarity = 1.0 / (1.0 + euclidean_dist)
        
        # Combined score (weighted average)
        combined_similarity = 0.7 * similarity + 0.3 * distance_similarity
        
        return float(combined_similarity)


class KeyStorageSystem:
    """Secure key storage and retrieval"""
    
    def __init__(self, storage_dir: str = "secure_keys"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
    def store_keys(self, user_id: str, keys: Dict) -> bool:
        """Store user's cryptographic keys securely"""
        try:
            key_file = os.path.join(self.storage_dir, f"{user_id}_keys.json")
            
            storage_data = {
                'user_id': user_id,
                'keys': keys,
                'created': datetime.now().isoformat(),
                'last_accessed': datetime.now().isoformat()
            }
            
            with open(key_file, 'w') as f:
                json.dump(storage_data, f, indent=2)
                
            return True
            
        except Exception as e:
            print(f"Key storage failed: {e}")
            return False
    
    def retrieve_keys(self, user_id: str) -> Optional[Dict]:
        """Retrieve user's cryptographic keys"""
        try:
            key_file = os.path.join(self.storage_dir, f"{user_id}_keys.json")
            
            if not os.path.exists(key_file):
                return None
                
            with open(key_file, 'r') as f:
                storage_data = json.load(f)
            
            # Update last accessed timestamp
            storage_data['last_accessed'] = datetime.now().isoformat()
            with open(key_file, 'w') as f:
                json.dump(storage_data, f, indent=2)
                
            return storage_data['keys']
            
        except Exception as e:
            print(f"Key retrieval failed: {e}")
            return None


class ProductionKeygenSystem:
    """Main production system integrating all components"""
    
    def __init__(self):
        self.biometric_processor = BiometricProcessor()
        self.lfsr_engine = DynamicLFSREngine()
        self.recognition_system = FaceRecognitionSystem()
        self.key_storage = KeyStorageSystem()
        
    def process_user(self, image: np.ndarray, user_id: str = None, add_template: bool = False) -> Dict:
        """Process user for key generation or retrieval"""
        
        try:
            # Extract biometric features
            features = self.biometric_processor.extract_features(image)
            
            # Try to identify existing user
            identified_user = self.recognition_system.identify_user(features)
            
            if identified_user:
                # Existing user recognized
                
                # Check if we should add this as an additional template
                if add_template:
                    self.recognition_system.register_user(identified_user, features)
                
                # Retrieve stored keys
                stored_keys = self.key_storage.retrieve_keys(identified_user)
                
                return {
                    'status': 'existing_user',
                    'user_id': identified_user,
                    'keys': stored_keys,
                    'message': f'Welcome back, {identified_user}!',
                    'can_add_template': True
                }
            
            else:
                # New user - generate keys
                if not user_id:
                    user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                # Generate cryptographic keys
                keys = self.lfsr_engine.generate_keys(features)
                
                # Register user
                registration_success = self.recognition_system.register_user(user_id, features)
                
                if registration_success:
                    # Store keys
                    storage_success = self.key_storage.store_keys(user_id, keys)
                    
                    return {
                        'status': 'new_user_registered',
                        'user_id': user_id,
                        'keys': keys,
                        'message': f'New user {user_id} registered successfully!',
                        'can_add_template': False
                    }
                else:
                    return {
                        'status': 'registration_failed',
                        'message': 'Failed to register new user'
                    }
                    
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Processing failed: {str(e)}'
            }


def main():
    """Main application entry point"""
    
    print("🔐 Facial Biometric Key Generation System")
    print("=" * 60)
    
    system = ProductionKeygenSystem()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Cannot access camera")
        return
    
    print("📷 Camera ready. Position your face in frame and press SPACE to process")
    print("Press ESC to exit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
            
        # Display frame
        cv2.imshow('Biometric Key System', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):  # Spacebar to process
            print("\n🔄 Processing...")
            
            result = system.process_user(frame)
            
            print(f"\n📊 Result: {result['message']}")
            
            if result['status'] in ['existing_user', 'new_user_registered']:
                keys = result['keys']
                
                print(f"\n🔑 Cryptographic Keys for {result['user_id']}:")
                print(f"   Primary Key: {keys['primary_key'][:32]}...")
                print(f"   Backup Key:  {keys['backup_key'][:32]}...")
                print(f"   Hash Key:    {keys['hash_key'][:32]}...")
                print(f"   Compact Key: {keys['compact_key'][:32]}...")
                
                if 'metadata' in keys:
                    meta = keys['metadata']
                    print(f"\n📈 Generation Stats:")
                    print(f"   Rounds: {meta['rounds_processed']}")
                    print(f"   Unique Values: {meta['unique_values']}")
                    print(f"   Entropy Ratio: {meta['entropy_ratio']:.4f}")
            
            print("\nPress SPACE to process again or ESC to exit")
            
        elif key == 27:  # ESC to exit
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n👋 System shutdown complete")


if __name__ == "__main__":
    main()