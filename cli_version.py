"""
Command Line Interface Version
Alternative to GUI for terminal users
"""

import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
import csv
import pickle
import sys

class FaceRecognitionCLI:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.attendance_marked = set()
        
        self.create_directories()
        self.load_encodings()
        
    def create_directories(self):
        """Create necessary directories"""
        directories = ['students_images', 'attendance_records', 'encodings']
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                
    def load_encodings(self):
        """Load face encodings"""
        encoding_file = 'encodings/face_encodings.pkl'
        if os.path.exists(encoding_file):
            try:
                with open(encoding_file, 'rb') as f:
                    data = pickle.load(f)
                    self.known_face_encodings = data['encodings']
                    self.known_face_names = data['names']
                print(f"✓ Loaded {len(self.known_face_names)} student(s)")
            except Exception as e:
                print(f"✗ Error loading encodings: {e}")
                
    def save_encodings(self):
        """Save face encodings"""
        encoding_file = 'encodings/face_encodings.pkl'
        data = {
            'encodings': self.known_face_encodings,
            'names': self.known_face_names
        }
        with open(encoding_file, 'wb') as f:
            pickle.dump(data, f)
        print("✓ Encodings saved")
        
    def add_new_student(self, name, num_images=5):
        """Add new student"""
        student_dir = f'students_images/{name}'
        if not os.path.exists(student_dir):
            os.makedirs(student_dir)
            
        cap = cv2.VideoCapture(0)
        count = 0
        encodings_list = []
        
        print(f"\n📸 Capturing {num_images} images for {name}")
        print("   Press SPACE to capture, ESC to cancel\n")
        
        while count < num_images:
            ret, frame = cap.read()
            if not ret:
                break
                
            cv2.putText(frame, f"Captured: {count}/{num_images}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Press SPACE to capture", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow('Add Student', frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord(' '):
                image_path = f'{student_dir}/image_{count}.jpg'
                cv2.imwrite(image_path, frame)
                
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                
                if face_locations:
                    face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                    encodings_list.append(face_encoding)
                    count += 1
                    print(f"   ✓ Image {count}/{num_images} captured")
                else:
                    print("   ✗ No face detected, try again")
                    
            elif key == 27:
                print("\n✗ Cancelled")
                cap.release()
                cv2.destroyAllWindows()
                return False
                
        cap.release()
        cv2.destroyAllWindows()
        
        if encodings_list:
            avg_encoding = np.mean(encodings_list, axis=0)
            self.known_face_encodings.append(avg_encoding)
            self.known_face_names.append(name)
            self.save_encodings()
            print(f"\n✓ {name} added successfully!\n")
            return True
        return False
        
    def mark_attendance(self, name):
        """Mark attendance"""
        now = datetime.now()
        date_string = now.strftime('%Y-%m-%d')
        time_string = now.strftime('%H:%M:%S')
        
        filename = f'attendance_records/attendance_{date_string}.csv'
        
        if name in self.attendance_marked:
            return False
            
        file_exists = os.path.exists(filename)
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Name', 'Date', 'Time'])
            writer.writerow([name, date_string, time_string])
            
        self.attendance_marked.add(name)
        return True
        
    def recognize_faces(self):
        """Start face recognition"""
        cap = cv2.VideoCapture(0)
        self.attendance_marked.clear()
        
        print("\n📹 Starting face recognition...")
        print("   Press 'q' to quit\n")
        
        frame_count = 0
        process_every_n_frames = 2
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            
            if frame_count % process_every_n_frames == 0:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                
                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.6)
                    name = "Unknown"
                    
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    if len(face_distances) > 0:
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = self.known_face_names[best_match_index]
                            
                            if self.mark_attendance(name):
                                print(f"   ✓ Attendance marked for {name}")
                                
                    face_names.append(name)
                    
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6),
                           cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
                           
            cv2.putText(frame, f"Marked: {len(self.attendance_marked)}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow('Attendance System', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"\n✓ Attendance complete! Marked: {len(self.attendance_marked)} student(s)\n")
        return len(self.attendance_marked)
        
    def view_attendance(self):
        """View today's attendance"""
        date_string = datetime.now().strftime('%Y-%m-%d')
        filename = f'attendance_records/attendance_{date_string}.csv'
        
        if not os.path.exists(filename):
            print("\n⚠ No attendance records for today\n")
            return
            
        print(f"\n📋 Attendance for {date_string}")
        print("=" * 60)
        
        with open(filename, 'r') as f:
            content = f.read()
            print(content)
        print("=" * 60 + "\n")
        
    def list_students(self):
        """List all registered students"""
        if not self.known_face_names:
            print("\n⚠ No students registered\n")
            return
            
        print(f"\n👥 Registered Students ({len(self.known_face_names)})")
        print("=" * 40)
        for i, name in enumerate(self.known_face_names, 1):
            print(f"{i}. {name}")
        print("=" * 40 + "\n")

def print_menu():
    """Print main menu"""
    print("\n" + "="*60)
    print("   FACE RECOGNITION ATTENDANCE SYSTEM - CLI")
    print("="*60)
    print("\n1. Add New Student")
    print("2. Start Attendance Recognition")
    print("3. View Today's Attendance")
    print("4. List All Students")
    print("5. Exit")
    print("\n" + "="*60)

def main():
    system = FaceRecognitionCLI()
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            name = input("\nEnter student name: ").strip()
            if name:
                print(f"\nℹ Camera will open. Press SPACE to capture images.")
                system.add_new_student(name)
            else:
                print("\n✗ Invalid name\n")
                
        elif choice == '2':
            if len(system.known_face_names) == 0:
                print("\n⚠ No students registered! Add students first.\n")
            else:
                print(f"\nℹ {len(system.known_face_names)} student(s) registered")
                input("Press ENTER to start camera...")
                system.recognize_faces()
                
        elif choice == '3':
            system.view_attendance()
            
        elif choice == '4':
            system.list_students()
            
        elif choice == '5':
            print("\n👋 Goodbye!\n")
            break
            
        else:
            print("\n✗ Invalid choice. Please try again.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)
