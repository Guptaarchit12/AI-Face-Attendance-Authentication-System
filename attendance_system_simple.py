"""
Simplified Attendance System for Python 3.14
Works without face recognition (no dlib needed)
Uses OpenCV for camera verification and manual ID entry
"""

import cv2
import json
import os
from datetime import datetime, timedelta


class SimpleAttendanceSystem:
    """
    Attendance system without face recognition
    Users enter ID, system verifies they're present via camera
    """
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        self.users_file = os.path.join(data_dir, "users.json")
        self.attendance_file = os.path.join(data_dir, "attendance.json")
        
        self.users = self.load_users()
        self.attendance_records = self.load_attendance()
    
    def load_users(self):
        """Load registered users"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_users(self):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def load_attendance(self):
        """Load attendance records"""
        if os.path.exists(self.attendance_file):
            with open(self.attendance_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_attendance(self):
        """Save attendance records"""
        with open(self.attendance_file, 'w') as f:
            json.dump(self.attendance_records, f, indent=2)
    
    def register_user(self, user_id, name, department=""):
        """Register a new user"""
        if user_id in self.users:
            print(f"✗ User {user_id} already exists!")
            return False
        
        self.users[user_id] = {
            'name': name,
            'user_id': user_id,
            'department': department,
            'registered_at': datetime.now().isoformat()
        }
        
        self.save_users()
        print(f"✓ Registered: {name} (ID: {user_id})")
        return True
    
    def verify_presence(self, user_name):
        """Verify person is present using camera"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("⚠ Camera not available - marking attendance anyway")
            return True
        
        print(f"\nVerifying presence of {user_name}...")
        print("Please look at the camera and press SPACE to confirm")
        
        verified = False
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Add text overlay
            cv2.putText(frame, f"User: {user_name}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Press SPACE to confirm presence", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press Q to cancel", 
                       (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Presence Verification', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):  # Space to confirm
                verified = True
                break
            elif key == ord('q'):  # Q to cancel
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        return verified
    
    def mark_attendance(self, user_id, action='punch_in'):
        """Mark attendance for a user"""
        if user_id not in self.users:
            print(f"✗ User {user_id} not found!")
            print("Please register first.")
            return False
        
        user = self.users[user_id]
        
        # Check for recent duplicate
        now = datetime.now()
        recent_cutoff = now - timedelta(seconds=60)
        
        for record in reversed(self.attendance_records[-10:]):
            record_time = datetime.fromisoformat(record['timestamp'])
            if (record['user_id'] == user_id and 
                record['action'] == action and 
                record_time > recent_cutoff):
                print(f"⚠ You already {action.replace('_', ' ')} less than a minute ago!")
                return False
        
        # Verify presence
        print(f"\n{'='*60}")
        print(f"  {action.upper().replace('_', ' ')}")
        print(f"{'='*60}")
        print(f"User: {user['name']}")
        print(f"ID: {user_id}")
        
        if self.verify_presence(user['name']):
            record = {
                'user_id': user_id,
                'name': user['name'],
                'action': action,
                'timestamp': now.isoformat(),
                'date': now.strftime('%Y-%m-%d'),
                'time': now.strftime('%H:%M:%S')
            }
            
            self.attendance_records.append(record)
            self.save_attendance()
            
            print(f"\n✓ {action.upper().replace('_', ' ')} successful!")
            print(f"  Name: {user['name']}")
            print(f"  Time: {record['time']}")
            return True
        else:
            print("\n✗ Attendance not marked - verification failed")
            return False
    
    def view_attendance(self, date=None, user_id=None):
        """View attendance records"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        records = [r for r in self.attendance_records if r['date'] == date]
        
        if user_id:
            records = [r for r in records if r['user_id'] == user_id]
        
        print(f"\n{'='*70}")
        print(f"  ATTENDANCE REPORT - {date}")
        print(f"{'='*70}\n")
        
        if not records:
            print("No records found.")
            return
        
        print(f"{'Name':<20} {'ID':<12} {'Action':<12} {'Time':<12}")
        print("-"*70)
        
        for record in records:
            print(f"{record['name']:<20} {record['user_id']:<12} "
                  f"{record['action'].upper():<12} {record['time']:<12}")
        
        print(f"\nTotal records: {len(records)}")
    
    def list_users(self):
        """List all registered users"""
        print(f"\n{'='*60}")
        print("  REGISTERED USERS")
        print(f"{'='*60}\n")
        
        if not self.users:
            print("No users registered yet.")
            return
        
        print(f"{'ID':<12} {'Name':<20} {'Department':<15}")
        print("-"*60)
        
        for user_id, user in self.users.items():
            dept = user.get('department', '')
            print(f"{user_id:<12} {user['name']:<20} {dept:<15}")
        
        print(f"\nTotal users: {len(self.users)}")


def main():
    """Main function"""
    system = SimpleAttendanceSystem()
    
    print("\n" + "="*60)
    print("  SIMPLIFIED ATTENDANCE SYSTEM")
    print("  (Compatible with Python 3.14)")
    print("="*60)
    print("\nNote: This version uses manual ID entry with camera")
    print("verification instead of face recognition.\n")
    
    while True:
        print("\n" + "="*60)
        print("  MENU")
        print("="*60)
        print("\n1. Register New User")
        print("2. Punch In")
        print("3. Punch Out")
        print("4. View Today's Attendance")
        print("5. View Attendance by Date")
        print("6. List All Users")
        print("7. Exit")
        
        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == '1':
            print("\n--- Register New User ---")
            user_id = input("Enter User ID: ").strip()
            name = input("Enter Name: ").strip()
            department = input("Enter Department (optional): ").strip()
            
            if user_id and name:
                system.register_user(user_id, name, department)
            else:
                print("✗ User ID and Name are required!")
        
        elif choice == '2':
            print("\n--- Punch In ---")
            user_id = input("Enter Your User ID: ").strip()
            if user_id:
                system.mark_attendance(user_id, action='punch_in')
        
        elif choice == '3':
            print("\n--- Punch Out ---")
            user_id = input("Enter Your User ID: ").strip()
            if user_id:
                system.mark_attendance(user_id, action='punch_out')
        
        elif choice == '4':
            system.view_attendance()
        
        elif choice == '5':
            date = input("Enter date (YYYY-MM-DD): ").strip()
            if date:
                system.view_attendance(date=date)
        
        elif choice == '6':
            system.list_users()
        
        elif choice == '7':
            print("\nThank you for using the Attendance System!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n\nError: {e}")
        print("Please report this issue.")
