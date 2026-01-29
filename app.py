import streamlit as st
import cv2
import face_recognition
import pickle
import numpy as np
from datetime import datetime
import json
from pathlib import Path
import pandas as pd

# --- SYSTEM LOGIC ---
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
    
    def save_user(self, name, user_id, encoding):
        self.known_face_encodings.append(encoding)
        self.known_face_names.append(user_id)
        self.users[user_id] = {'name': name, 'user_id': user_id, 'registered_at': datetime.now().isoformat()}
        
        with open(self.encodings_file, 'wb') as f:
            pickle.dump({'encodings': self.known_face_encodings, 'names': self.known_face_names}, f)
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)

    def log_attendance(self, user_id, confidence, action):
        now = datetime.now()
        record = {
            'user_id': user_id,
            'name': self.users[user_id]['name'],
            'action': action,
            'confidence': round(float(confidence), 2),
            'date': now.strftime('%Y-%m-%d'),
            'time': now.strftime('%H:%M:%S')
        }
        self.attendance_records.append(record)
        with open(self.attendance_file, 'w') as f:
            json.dump(self.attendance_records, f, indent=2)
        return record

# --- STREAMLIT UI ---
st.set_page_config(page_title="AI Face Attendance", layout="wide")
system = FaceAttendanceSystem()

st.title("AI Face Attendance System")
st.markdown("---")

menu = ["Log Attendance", "User Registration", "View Reports"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "User Registration":
    st.subheader("New User Registration")
    col1, col2 = st.columns(2)
    
    with col1:
        u_name = st.text_input("Enter Full Name")
        u_id = st.text_input("Enter Unique ID")
        register_btn = st.button("Start Camera & Register")

    if register_btn and u_name and u_id:
        cap = cv2.VideoCapture(0)
        samples = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        while len(samples) < 5:
            ret, frame = cap.read()
            if not ret: break
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locs = face_recognition.face_locations(rgb_frame)
            
            if len(face_locs) == 1:
                enc = face_recognition.face_encodings(rgb_frame, face_locs)[0]
                samples.append(enc)
                progress_bar.progress(len(samples) * 20)
                status_text.text(f"Captured {len(samples)}/5 samples...")
        
        cap.release()
        if len(samples) == 5:
            system.save_user(u_name, u_id, np.mean(samples, axis=0))
            st.success(f"User {u_name} registered successfully!")

elif choice == "Log Attendance":
    st.subheader("Punch In/Out System")
    action = st.radio("Select Action", ["Punch In", "Punch Out"], horizontal=True)
    run_scanner = st.checkbox("Turn On Scanner")
    
    FRAME_WINDOW = st.image([]) # Placeholder for video
    
    if run_scanner:
        cap = cv2.VideoCapture(0)
        consecutive_count = 0
        last_user = None
        
        while True:
            ret, frame = cap.read()
            if not ret: break
            
            # Optimization
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            face_locs = face_recognition.face_locations(rgb_small)
            face_encs = face_recognition.face_encodings(rgb_small, face_locs)
            
            current_user = None
            conf = 0
            
            for (top, right, bottom, left), enc in zip(face_locs, face_encs):
                matches = face_recognition.compare_faces(system.known_face_encodings, enc, tolerance=0.5)
                dist = face_recognition.face_distance(system.known_face_encodings, enc)
                
                if True in matches:
                    idx = np.argmin(dist)
                    current_user = system.known_face_names[idx]
                    conf = 1 - dist[idx]
                    
                    # Draw UI on frame
                    top*=4; right*=4; bottom*=4; left*=4
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, system.users[current_user]['name'], (left, top-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Verification Logic
            if current_user and current_user == last_user:
                consecutive_count += 1
            else:
                consecutive_count = 0
                last_user = current_user
            
            # Display frame in Streamlit
            FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            if consecutive_count >= 3:
                rec = system.log_attendance(current_user, conf, action.lower().replace(" ", "_"))
                st.balloons()
                st.success(f"Verified: {rec['name']} logged at {rec['time']}")
                break
                
        cap.release()

elif choice == "View Reports":
    st.subheader("Attendance Records")
    if system.attendance_records:
        df = pd.DataFrame(system.attendance_records)
        # Reverse to show newest at top
        st.dataframe(df.iloc[::-1], use_container_width=True)
        st.download_button("Download CSV", df.to_csv(index=False), "attendance.csv", "text/csv")
    else:
        st.info("No records found yet.")