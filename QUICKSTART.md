# Quick Start Guide

## Getting Started in 5 Minutes

### Step 1: Install Dependencies
```bash
# Make setup script executable (Linux/Mac)
chmod +x setup.sh

# Run setup
./setup.sh

# Or install manually
pip install -r requirements.txt
```

### Step 2: Run the System
```bash
# Activate virtual environment (if created)
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Run the main program
python attendance_system.py
```

### Step 3: Register Your First User
1. Select option `1` (Register New User)
2. Enter name: `John Doe`
3. Enter user ID: `EMP001`
4. Look at camera and press `SPACE` to capture (5 times)
5. User registered!

### Step 4: Test Attendance
1. Select option `2` (Punch In)
2. Look at camera
3. System recognizes you
4. Press `SPACE` to confirm
5. Attendance marked!

## Demo Mode (No Camera Required)

Want to see how it works without a camera?

```bash
python demo.py
```

This will:
- Show system capabilities
- Simulate user registration
- Generate sample attendance records
- Display reports
- Explain technical details

## Common Commands

```bash
# Run main system
python attendance_system.py

# Run demo
python demo.py

# Check if camera works
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"

# View attendance data
cat data/attendance.json

# View registered users
cat data/users.json
```

## Quick Troubleshooting

**Camera not working?**
- Close other apps using camera
- Check camera permissions
- Try: `cv2.VideoCapture(1)` instead of `cv2.VideoCapture(0)`

**Installation fails?**
- Install system dependencies first
- Ubuntu: `sudo apt-get install build-essential cmake`
- Mac: `brew install cmake`

**Low accuracy?**
- Improve lighting
- Face camera directly
- Re-register user
- Adjust tolerance in code

## File Structure

```
face_attendance_system/
├── attendance_system.py  ← Main program
├── demo.py              ← Demo/testing
├── requirements.txt     ← Dependencies
├── README.md           ← Full documentation
├── QUICKSTART.md       ← This file
├── setup.sh            ← Setup script
└── data/               ← Auto-created
    ├── face_encodings.pkl
    ├── users.json
    └── attendance.json
```

## What's Next?

1. Read full [README.md](README.md) for detailed documentation
2. Test the demo to understand the system
3. Register your team members
4. Start tracking attendance!

## Key Features

✓ Real-time face recognition  
✓ Punch in/out tracking  
✓ Spoof prevention  
✓ Attendance reports  
✓ Easy to use  
✓ Works with webcam  

## Support

- Check [README.md](README.md) for detailed info
- Review troubleshooting section
- Test with demo.py first

That's it! You're ready to use the Face Attendance System.
