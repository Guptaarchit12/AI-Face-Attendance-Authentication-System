"""
Quick Verification Script
Copy this entire file and save as: verify_setup.py
Then run: python verify_setup.py
"""

import sys

print("="*60)
print("  Installation Verification")
print("="*60)
print()

# Check Python version
print(f"Python Version: {sys.version}")
print()

# Test NumPy
try:
    import numpy as np
    print(f"✓ NumPy {np.__version__} - INSTALLED")
except ImportError:
    print("✗ NumPy - NOT INSTALLED")
    print("  Run: pip install numpy")

# Test Pillow
try:
    from PIL import Image
    print("✓ Pillow - INSTALLED")
except ImportError:
    print("✗ Pillow - NOT INSTALLED")
    print("  Run: pip install pillow")

# Test OpenCV
try:
    import cv2
    print(f"✓ OpenCV {cv2.__version__} - INSTALLED")
    opencv_ok = True
except ImportError:
    print("✗ OpenCV - NOT INSTALLED")
    print("  Run: pip install opencv-python")
    opencv_ok = False

print()
print("="*60)

# Test camera if OpenCV is available
if opencv_ok:
    print("Testing camera access...")
    import cv2
    
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("✓ Camera is accessible!")
        ret, frame = cap.read()
        if ret:
            print(f"✓ Camera resolution: {frame.shape[1]}x{frame.shape[0]}")
            print()
            print("Displaying camera feed for 3 seconds...")
            cv2.imshow('Camera Test - This will close automatically', frame)
            cv2.waitKey(3000)
            cv2.destroyAllWindows()
        cap.release()
    else:
        print("⚠ Camera not accessible")
        print("  - Close other apps using camera")
        print("  - Check camera permissions in Windows Settings")

print()
print("="*60)
print("  NEXT STEPS")
print("="*60)
print()
print("Since you have Python 3.14, you have 2 options:")
print()
print("OPTION 1: Install Python 3.11 (RECOMMENDED)")
print("  - Download from: https://www.python.org/downloads/")
print("  - Install Python 3.11.9")
print("  - Create new venv: py -3.11 -m venv venv")
print("  - Install packages: pip install dlib face-recognition")
print("  - Get FULL face recognition system!")
print()
print("OPTION 2: Use simplified version with Python 3.14")
print("  - No face recognition (dlib not available)")
print("  - Use motion detection or manual ID entry")
print("  - Still tracks attendance with timestamps")
print()

input("Press Enter to exit...")
