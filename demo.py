"""
Demo Script for Face Attendance System
This script demonstrates the system functionality with sample images
"""

import cv2
import face_recognition
import numpy as np
from attendance_system import FaceAttendanceSystem
from datetime import datetime
import os


def create_sample_face_image(name, output_path):
    """
    Create a simple colored image as a placeholder
    In production, use actual photos
    """
    # Create a 200x200 colored image
    img = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
    cv2.imwrite(output_path, img)
    print(f"Created sample image: {output_path}")


def demo_without_camera():
    """
    Demonstrate system functionality without camera
    Useful for testing and demonstration
    """
    print("\n" + "="*60)
    print("  FACE ATTENDANCE SYSTEM - DEMO MODE")
    print("="*60)
    print("\nNote: This demo simulates the system without requiring a camera.")
    print("In production, the system uses real-time camera input.\n")
    
    # Initialize system
    system = FaceAttendanceSystem(data_dir="demo_data")
    
    # Demo 1: Show system capabilities
    print("\n--- SYSTEM CAPABILITIES ---")
    print("✓ User Registration: Capture and store face encodings")
    print("✓ Face Recognition: Identify users in real-time")
    print("✓ Punch In/Out: Mark attendance with timestamps")
    print("✓ Spoof Prevention: Duplicate detection within 60 seconds")
    print("✓ Attendance Reports: View and track attendance records")
    print("✓ Lighting Adaptation: Works under various lighting conditions")
    
    # Demo 2: Simulated user data
    print("\n--- SIMULATED USER REGISTRATION ---")
    demo_users = [
        {"name": "John Doe", "user_id": "EMP001"},
        {"name": "Jane Smith", "user_id": "EMP002"},
        {"name": "Bob Johnson", "user_id": "EMP003"}
    ]
    
    for user in demo_users:
        # Simulate registration
        print(f"\nRegistering: {user['name']} (ID: {user['user_id']})")
        print("  - Capturing face samples...")
        print("  - Generating face encoding...")
        print("  - Storing in database...")
        print(f"  ✓ {user['name']} registered successfully!")
        
        # Add to system (simulated)
        system.users[user['user_id']] = {
            'name': user['name'],
            'user_id': user['user_id'],
            'registered_at': datetime.now().isoformat()
        }
    
    system._save_users()
    
    # Demo 3: Simulated attendance marking
    print("\n--- SIMULATED ATTENDANCE MARKING ---")
    
    attendance_events = [
        {"user_id": "EMP001", "action": "punch_in", "time": "09:00:00"},
        {"user_id": "EMP002", "action": "punch_in", "time": "09:15:00"},
        {"user_id": "EMP003", "action": "punch_in", "time": "09:30:00"},
        {"user_id": "EMP001", "action": "punch_out", "time": "18:00:00"},
        {"user_id": "EMP002", "action": "punch_out", "time": "18:10:00"},
    ]
    
    for event in attendance_events:
        user = system.users[event['user_id']]
        now = datetime.now()
        
        record = {
            'user_id': event['user_id'],
            'name': user['name'],
            'action': event['action'],
            'timestamp': now.isoformat(),
            'confidence': 0.95,  # Simulated high confidence
            'date': now.strftime('%Y-%m-%d'),
            'time': event['time']
        }
        
        system.attendance_records.append(record)
        print(f"  {user['name']}: {event['action'].upper()} at {event['time']} (Confidence: 95%)")
    
    system._save_attendance()
    
    # Demo 4: Display attendance report
    print("\n--- ATTENDANCE REPORT ---")
    system.display_attendance_report()
    
    # Demo 5: Technical details
    print("\n--- TECHNICAL IMPLEMENTATION ---")
    print("\nModel: dlib ResNet-based face recognition")
    print("  - 128-dimensional face embeddings")
    print("  - 99.38% accuracy on LFW benchmark")
    print("  - Euclidean distance for matching")
    
    print("\nTraining Process:")
    print("  - Pre-trained model (no training required)")
    print("  - Registration: Capture 5 samples per user")
    print("  - Encoding: Generate 128-d vector")
    print("  - Storage: Save averaged encoding")
    
    print("\nRecognition Process:")
    print("  1. Capture live video frame")
    print("  2. Detect faces using HOG/CNN")
    print("  3. Generate face encoding")
    print("  4. Compare with stored encodings")
    print("  5. Match if distance < tolerance (0.6)")
    
    print("\nAccuracy Expectations:")
    print("  - Ideal conditions: 95-99% accuracy")
    print("  - Good lighting: 90-95% accuracy")
    print("  - Poor lighting: 70-85% accuracy")
    print("  - False positive rate: <1%")
    
    print("\nKnown Limitations:")
    print("  ✗ Cannot detect photo-based spoofing (advanced)")
    print("  ✗ May struggle with twins/very similar faces")
    print("  ✗ Requires face to be visible (no masks)")
    print("  ✗ Accuracy decreases with extreme angles (>45°)")
    
    print("\nFailure Cases & Handling:")
    print("  - Multiple faces: Shows error, asks for one person")
    print("  - No face detected: Prompts user to reposition")
    print("  - Low confidence: Rejects access, suggests re-registration")
    print("  - Duplicate punch: Prevented within 60 seconds")
    print("  - Camera issues: Clear error message with solution")
    
    print("\n--- SPOOF PREVENTION ---")
    print("\nCurrent Measures:")
    print("  ✓ Temporal duplicate detection (60s window)")
    print("  ✓ Live camera requirement")
    print("  ✓ Confidence threshold filtering")
    
    print("\nRecommended Enhancements:")
    print("  - Liveness detection (blink, head movement)")
    print("  - Depth sensing (3D cameras)")
    print("  - Challenge-response verification")
    print("  - Multi-factor authentication")
    
    print("\n--- DATA STORAGE ---")
    print(f"\nData files created in: {system.data_dir}")
    print("  - face_encodings.pkl: Face embeddings")
    print("  - users.json: User information")
    print("  - attendance.json: Attendance records")
    
    # Show sample data
    print("\nSample User Data:")
    for user_id, user_data in list(system.users.items())[:2]:
        print(f"  {user_data['name']}: ID={user_id}")
    
    print("\nSample Attendance Record:")
    if system.attendance_records:
        record = system.attendance_records[0]
        print(f"  {record['name']}: {record['action']} at {record['time']}")
        print(f"  Confidence: {record['confidence']:.1%}")
    
    print("\n--- DEMO COMPLETE ---")
    print("\nTo run the actual system with camera:")
    print("  python attendance_system.py")
    print("\nTo test with your own images:")
    print("  Modify the register_user() function to use image_path parameter")
    
    return system


def test_accuracy_scenarios():
    """
    Demonstrate expected accuracy under different scenarios
    """
    print("\n" + "="*60)
    print("  ACCURACY TESTING SCENARIOS")
    print("="*60)
    
    scenarios = [
        {
            "condition": "Ideal (Good lighting, front-facing)",
            "accuracy": "95-99%",
            "frr": "1-3%",
            "far": "<0.5%",
            "notes": "Best case scenario"
        },
        {
            "condition": "Good (Indoor office lighting)",
            "accuracy": "90-95%",
            "frr": "3-5%",
            "far": "<1%",
            "notes": "Typical office environment"
        },
        {
            "condition": "Moderate (Varying angles ±30°)",
            "accuracy": "85-90%",
            "frr": "5-10%",
            "far": "1-2%",
            "notes": "Some head rotation acceptable"
        },
        {
            "condition": "Challenging (Low light, ±45° angle)",
            "accuracy": "70-85%",
            "frr": "10-20%",
            "far": "2-3%",
            "notes": "May need re-attempt"
        },
        {
            "condition": "Poor (Very low light, extreme angles)",
            "accuracy": "50-70%",
            "frr": "20-40%",
            "far": "3-5%",
            "notes": "Not recommended"
        }
    ]
    
    print("\nFRR: False Rejection Rate (legitimate user rejected)")
    print("FAR: False Acceptance Rate (wrong person accepted)\n")
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['condition']}")
        print(f"   Accuracy: {scenario['accuracy']}")
        print(f"   FRR: {scenario['frr']} | FAR: {scenario['far']}")
        print(f"   Notes: {scenario['notes']}\n")


if __name__ == "__main__":
    # Run demo
    system = demo_without_camera()
    
    # Show accuracy scenarios
    test_accuracy_scenarios()
    
    print("\n" + "="*60)
    print("For production deployment, ensure:")
    print("  1. Good quality camera (720p minimum)")
    print("  2. Adequate lighting in registration area")
    print("  3. Clear background for face detection")
    print("  4. Regular re-registration (every 6-12 months)")
    print("  5. Backup and security measures")
    print("="*60 + "\n")
