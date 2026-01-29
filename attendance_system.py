import cv2
import face_recognition
import pickle
import numpy as np
from datetime import datetime
import json
from pathlib import Path

class FaceAttendanceSystem:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.encodings_file = self.data_dir / "face_encodings.pkl"
        self.attendance_file = self.data_dir / "attendance.json"
        self.users_file = self.data_dir / "users.json"
        
        self.known_face_encodings = []
        self.known_face_names = []
        self.users = {}
        self.attendance_records = []
        
        self._load_data()
        
    def _load_data(self):
        if self.encodings_file.exists():
            with open(self.encodings_file, 'rb') as f:
                data = pickle.load(f)
                self.known_face_encodings = data['encodings']
                self.known_face_names = data['names']
        if self.users_file.exists():
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        if self.attendance_file.exists():
            with open(self.attendance_file, 'r') as f:
                self.attendance_records = json.load(f)
    
    def _save_encodings(self):
        with open(self.encodings_file, 'wb') as f:
            pickle.dump({'encodings': self.known_face_encodings, 'names': self.known_face_names}, f)
    
    def _save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def _save_attendance(self):
        with open(self.attendance_file, 'w') as f:
            json.dump(self.attendance_records, f, indent=2)

    def register_user(self, name, user_id):
        video_capture = cv2.VideoCapture(0)
        # SPEED FIX: Lower Capture Resolution
        video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        samples = []
        print(f"Registering {name}. Look at the camera...")

        while len(samples) < 5:
            ret, frame = video_capture.read()
            if not ret: break

            cv2.putText(frame, f"Capturing Sample: {len(samples)}/5", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow('Registration', frame)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            
            if len(face_locations) == 1:
                encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                samples.append(encoding)
            
            if cv2.waitKey(1) & 0xFF == ord('q'): break

        video_capture.release()
        cv2.destroyAllWindows()

        if len(samples) >= 5:
            self.known_face_encodings.append(np.mean(samples, axis=0))
            self.known_face_names.append(user_id)
            self.users[user_id] = {'name': name, 'user_id': user_id, 'registered_at': datetime.now().isoformat()}
            self._save_encodings(); self._save_users()
            print(f"✓ Registered {name}")
            return True
        return False

    def identify_face_realtime(self, tolerance=0.5, required_frames=3):
        """
        ULTRA-FAST VERSION:
        - Forced 640x480 resolution
        - Frame skipping (process every 2nd frame)
        - Reduced required_frames to 3
        """
        video_capture = cv2.VideoCapture(0)
        video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        consecutive_count = 0
        last_user_id = None
        final_confidence = 0
        process_this_frame = True # For frame skipping

        print("System Active: Scanning...")

        while True:
            ret, frame = video_capture.read()
            if not ret: break

            # SPEED FIX: Only process every other frame
            if process_this_frame:
                # Resize to 1/4 for processing speed
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                current_frame_user = None

                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=tolerance)
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    
                    if True in matches:
                        best_match_index = np.argmin(face_distances)
                        current_frame_user = self.known_face_names[best_match_index]
                        final_confidence = 1 - face_distances[best_match_index]
                        
                        # Draw label on original frame
                        top *= 4; right *= 4; bottom *= 4; left *= 4
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.putText(frame, self.users[current_frame_user]['name'], (left, top - 10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # Auto-confirm logic
                if current_frame_user and current_frame_user == last_user_id:
                    consecutive_count += 1
                else:
                    consecutive_count = 0
                    last_user_id = current_frame_user

            process_this_frame = not process_this_frame

            # Visual progress bar
            progress = (consecutive_count / required_frames)
            cv2.rectangle(frame, (150, 440), (490, 455), (50, 50, 50), -1)
            cv2.rectangle(frame, (150, 440), (150 + int(340 * progress), 455), (0, 255, 0), -1)
            
            cv2.imshow('Fast Scanner - Q to Cancel', frame)

            if consecutive_count >= required_frames:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                last_user_id = None
                break

        video_capture.release()
        cv2.destroyAllWindows()
        return last_user_id, final_confidence

    def mark_attendance(self, action='punch_in'):
        user_id, confidence = self.identify_face_realtime()
        if not user_id: return False

        now = datetime.now()
        record = {
            'user_id': user_id, 'name': self.users[user_id]['name'],
            'action': action, 'timestamp': now.isoformat(),
            'confidence': float(confidence), 'date': now.strftime('%Y-%m-%d'),
            'time': now.strftime('%H:%M:%S')
        }
        self.attendance_records.append(record)
        self._save_attendance()
        print(f"\n✓ {action.upper()} SUCCESS: {record['name']} @ {record['time']}")
        return True

    def display_report(self):
        date = datetime.now().strftime('%Y-%m-%d')
        records = [r for r in self.attendance_records if r['date'] == date]
        print(f"\n--- TODAY'S ATTENDANCE ({date}) ---")
        for r in records:
            print(f"{r['time']} - {r['name']} ({r['action']})")

def main():
    sys = FaceAttendanceSystem()
    while True:
        print("\n1. Register | 2. Punch In | 3. Punch Out | 4. Report | 5. Exit")
        c = input("Choice: ")
        if c == '1': sys.register_user(input("Name: "), input("ID: "))
        elif c == '2': sys.mark_attendance('punch_in')
        elif c == '3': sys.mark_attendance('punch_out')
        elif c == '4': sys.display_report()
        elif c == '5': break

if __name__ == "__main__":
    main()