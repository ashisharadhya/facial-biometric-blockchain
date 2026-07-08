"""
Production Demo Script for Facial Biometric Key Generation System
Demonstrates single-shot recognition and key generation capabilities
"""

import cv2
import time
from facial_keygen_system import ProductionKeygenSystem


def demo_system():
    """Run interactive demo of the biometric key system"""
    
    print("🎯 FACIAL BIOMETRIC KEY GENERATION DEMO")
    print("=" * 50)
    print("🔐 Advanced Dynamic LFSR Cryptographic Key Generation")
    print("🎯 Single-Shot Face Recognition & User Management")
    print("=" * 50)
    
    system = ProductionKeygenSystem()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Camera not available")
        return
    
    print("📷 Camera initialized successfully!")
    print("\n🎬 DEMO INSTRUCTIONS:")
    print("   • Position your face clearly in the camera frame")
    print("   • Press SPACE to process your biometric data")
    print("   • First time: System will register you as new user")
    print("   • Subsequent times: System will recognize and retrieve your keys")
    print("   • Press T to add more templates (improves recognition accuracy)")
    print("   • Press ESC to exit demo")
    print("\n💡 PRO TIP: Add 2-3 templates per user for best recognition!")
    
    user_count = 0
    demo_sessions = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Add demo overlay
        height, width = frame.shape[:2]
        cv2.putText(frame, "Facial Biometric Key System - DEMO", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Users Registered: {user_count}", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, f"Demo Sessions: {demo_sessions}", 
                   (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "SPACE = Process | T = Add Template | ESC = Exit", 
                   (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        cv2.imshow('Biometric Demo', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):  # Process biometric
            print(f"\n{'='*60}")
            print(f"🔄 DEMO SESSION #{demo_sessions + 1}")
            print("=" * 60)
            
            start_time = time.time()
            result = system.process_user(frame)
            process_time = time.time() - start_time
            
            demo_sessions += 1
            
            if result['status'] == 'new_user_registered':
                user_count += 1
                print(f"🆕 NEW USER REGISTERED")
                print(f"   👤 User ID: {result['user_id']}")
                print(f"   ⏱️  Processing Time: {process_time:.2f}s")
                
            elif result['status'] == 'existing_user':
                print(f"✅ USER RECOGNIZED")
                print(f"   👤 User ID: {result['user_id']}")
                print(f"   ⏱️  Recognition Time: {process_time:.2f}s")
                if result.get('can_add_template'):
                    print(f"   💡 TIP: Press 'T' to add another template for better recognition")
                
            else:
                print(f"❌ PROCESSING FAILED")
                print(f"   Error: {result['message']}")
                continue
            
            # Display key information
            if 'keys' in result:
                keys = result['keys']
                print(f"\n🔑 CRYPTOGRAPHIC KEYS GENERATED:")
                print(f"   Primary:  {keys['primary_key'][:16]}...{keys['primary_key'][-8:]}")
                print(f"   Backup:   {keys['backup_key'][:16]}...{keys['backup_key'][-8:]}")
                print(f"   Hash:     {keys['hash_key'][:16]}...{keys['hash_key'][-8:]}")
                print(f"   Compact:  {keys['compact_key']}")
                
                if 'metadata' in keys:
                    meta = keys['metadata']
                    print(f"\n📊 ALGORITHM PERFORMANCE:")
                    print(f"   LFSR Rounds: {meta['rounds_processed']}")
                    print(f"   Unique Values: {meta['unique_values']:,}")
                    print(f"   Entropy Ratio: {meta['entropy_ratio']:.4f}")
                    print(f"   Generation Time: {meta.get('timestamp', 'N/A')}")
            
            print(f"\n💡 TIP: Try again to test recognition accuracy!")
            print("=" * 60)
            
        elif key == ord('t') or key == ord('T'):  # T - add template
            print(f"\n{'='*60}")
            print(f"📝 ADDING TEMPLATE FOR BETTER RECOGNITION")
            print(f"{'='*60}")
            
            result = system.process_user(frame, add_template=True)
            
            if result['status'] == 'existing_user':
                print(f"✅ Template added for {result['user_id']}")
                print(f"   Recognition will be more accurate now!")
            else:
                print(f"❌ Must recognize existing user first")
                print(f"   Use SPACE to process first")
            
            print(f"{'='*60}\n")
            
        elif key == 27:  # ESC to exit
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n🎯 DEMO COMPLETE")
    print("=" * 50)
    print(f"📈 DEMO STATISTICS:")
    print(f"   Total Sessions: {demo_sessions}")
    print(f"   Users Registered: {user_count}")
    print(f"   Recognition Tests: {demo_sessions - user_count}")
    print("=" * 50)
    print("✨ Thank you for trying the Facial Biometric Key Generation System!")


if __name__ == "__main__":
    try:
        demo_system()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
    finally:
        cv2.destroyAllWindows()
        print("🔒 System shutdown complete")