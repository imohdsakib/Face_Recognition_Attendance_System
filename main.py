import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
import csv
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import pickle

class FaceRecognitionAttendanceSystem:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.attendance_marked = set()
        
        # Create necessary directories
        self.create_directories()
        
        # Load existing face encodings
        self.load_encodings()
        
    def create_directories(self):
        """Create necessary directories for the system"""
        directories = ['students_images', 'attendance_records', 'encodings']
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                
    def load_encodings(self):
        """Load previously saved face encodings"""
        encoding_file = 'encodings/face_encodings.pkl'
        if os.path.exists(encoding_file):
            try:
                with open(encoding_file, 'rb') as f:
                    data = pickle.load(f)
                    self.known_face_encodings = data['encodings']
                    self.known_face_names = data['names']
                print(f"Loaded {len(self.known_face_names)} face encodings")
            except Exception as e:
                print(f"Error loading encodings: {e}")
                
    def save_encodings(self):
        """Save face encodings to file"""
        encoding_file = 'encodings/face_encodings.pkl'
        data = {
            'encodings': self.known_face_encodings,
            'names': self.known_face_names
        }
        with open(encoding_file, 'wb') as f:
            pickle.dump(data, f)
        print("Encodings saved successfully")
        
    def add_new_student(self, name, num_images=5):
        """Capture and encode new student faces"""
        student_dir = f'students_images/{name}'
        if not os.path.exists(student_dir):
            os.makedirs(student_dir)
            
        cap = cv2.VideoCapture(0)
        
        # Check if camera opened successfully
        if not cap.isOpened():
            print("Error: Could not open camera")
            return False
        
        count = 0
        encodings_list = []
        
        print(f"\nCapturing {num_images} images for {name}")
        print("Press SPACE to capture, ESC to cancel")
        
        while count < num_images:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Display frame
            cv2.putText(frame, f"Captured: {count}/{num_images}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Press SPACE to capture", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "Press ESC to cancel", (10, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow('Add New Student', frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord(' '):  # Space key
                # Save image
                image_path = f'{student_dir}/image_{count}.jpg'
                cv2.imwrite(image_path, frame)
                
                # Get face encoding
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                
                if face_locations:
                    face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                    encodings_list.append(face_encoding)
                    count += 1
                    print(f"Captured image {count}/{num_images}")
                else:
                    print("No face detected. Please try again.")
                    
            elif key == 27:  # ESC key
                print("Cancelled")
                cap.release()
                cv2.destroyAllWindows()
                return False
                
        cap.release()
        cv2.destroyAllWindows()
        
        # Average the encodings
        if encodings_list:
            avg_encoding = np.mean(encodings_list, axis=0)
            self.known_face_encodings.append(avg_encoding)
            self.known_face_names.append(name)
            self.save_encodings()
            print(f"\n{name} added successfully!")
            return True
        return False
        
    def mark_attendance(self, name):
        """Mark attendance in CSV file"""
        now = datetime.now()
        date_string = now.strftime('%Y-%m-%d')
        time_string = now.strftime('%H:%M:%S')
        
        # Create attendance file for today
        filename = f'attendance_records/attendance_{date_string}.csv'
        
        # Check if student already marked today
        if name in self.attendance_marked:
            return False
            
        # Write to CSV
        file_exists = os.path.exists(filename)
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Name', 'Date', 'Time'])
            writer.writerow([name, date_string, time_string])
            
        self.attendance_marked.add(name)
        return True
    
    def delete_student(self, name):
        """Delete a student from the system"""
        if name not in self.known_face_names:
            return False
        
        # Find index of the student
        index = self.known_face_names.index(name)
        
        # Remove from lists
        del self.known_face_names[index]
        del self.known_face_encodings[index]
        
        # Save updated encodings
        self.save_encodings()
        
        # Delete student images folder
        import shutil
        student_dir = f'students_images/{name}'
        if os.path.exists(student_dir):
            shutil.rmtree(student_dir)
        
        print(f"Student {name} deleted successfully")
        return True
    
    def get_all_students(self):
        """Get list of all registered students"""
        return self.known_face_names.copy()
        
    def recognize_faces(self):
        """Real-time face recognition and attendance marking"""
        cap = cv2.VideoCapture(0)
        
        # Check if camera opened successfully
        if not cap.isOpened():
            print("Error: Could not open camera")
            return 0
        
        # Reset attendance marked for new session
        self.attendance_marked.clear()
        
        print("\nStarting face recognition...")
        print("Press 'q' to quit")
        
        frame_count = 0
        process_every_n_frames = 2  # Process every 2nd frame for better performance
        face_locations = []
        face_names = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to read frame")
                break
                
            frame_count += 1
            
            # Process only every nth frame
            if frame_count % process_every_n_frames == 0:
                # Resize frame for faster processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                
                # Find faces in frame
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                
                face_names = []
                for face_encoding in face_encodings:
                    # Compare with known faces
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.6)
                    name = "Unknown"
                    
                    # Use the known face with smallest distance
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    if len(face_distances) > 0:
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = self.known_face_names[best_match_index]
                            
                            # Mark attendance
                            if self.mark_attendance(name):
                                print(f"Attendance marked for {name}")
                                
                    face_names.append(name)
                    
            # Display results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                # Draw rectangle around face
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                
                # Draw label
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6),
                           cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
                           
            # Display attendance status
            cv2.putText(frame, f"Attendance Marked: {len(self.attendance_marked)}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Display instructions
            cv2.putText(frame, "Press 'q' to Quit", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            cv2.imshow('Face Recognition Attendance System', frame)
            
            # Quit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        
        return len(self.attendance_marked)

class AttendanceSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Face Recognition Attendance System")
        self.root.configure(bg='#1a1a2e')
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set window to screen size
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Maximize window (Windows)
        try:
            self.root.state('zoomed')
        except:
            # For other OS, use fullscreen
            self.root.attributes('-fullscreen', False)
        
        self.root.resizable(True, True)
        
        self.system = FaceRecognitionAttendanceSystem()
        
        self.create_widgets()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg='#16213e', height=120)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title with icon
        title_icon = tk.Label(header_frame, text="🎓", 
                             font=('Arial', 40), bg='#16213e')
        title_icon.pack(pady=(15, 0))
        
        title = tk.Label(header_frame, text="Face Recognition Attendance System",
                        font=('Segoe UI', 18, 'bold'), bg='#16213e', fg='#00d4ff')
        title.pack(pady=(0, 5))
        
        subtitle = tk.Label(header_frame, text="AI-Powered Attendance Management",
                           font=('Segoe UI', 10), bg='#16213e', fg='#a0a0a0')
        subtitle.pack()
        
        # Main Content Frame
        content_frame = tk.Frame(self.root, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40)
        
        # Button style
        btn_style = {
            'font': ('Segoe UI', 12, 'bold'),
            'width': 30,
            'height': 2,
            'fg': 'white',
            'border': 0,
            'cursor': 'hand2',
            'relief': tk.FLAT
        }
        
        # Add Student Button
        add_btn = tk.Button(content_frame, text="➕  Add New Student",
                           command=self.add_student,
                           bg='#0f4c75', activebackground='#1b6ca8',
                           **btn_style)
        add_btn.pack(pady=8)
        self.add_hover_effect(add_btn, '#1b6ca8', '#0f4c75')
        
        # Start Attendance Button
        start_btn = tk.Button(content_frame, text="📹  Start Attendance Recognition",
                             command=self.start_recognition,
                             bg='#27ae60', activebackground='#2ecc71',
                             **btn_style)
        start_btn.pack(pady=8)
        self.add_hover_effect(start_btn, '#2ecc71', '#27ae60')
        
        # View Attendance Button
        view_btn = tk.Button(content_frame, text="📊  View Today's Attendance",
                            command=self.view_attendance,
                            bg='#8e44ad', activebackground='#9b59b6',
                            **btn_style)
        view_btn.pack(pady=8)
        self.add_hover_effect(view_btn, '#9b59b6', '#8e44ad')
        
        # Delete Student Button
        delete_btn = tk.Button(content_frame, text="🗑️  Delete Student",
                              command=self.delete_student,
                              bg='#d35400', activebackground='#e67e22',
                              **btn_style)
        delete_btn.pack(pady=8)
        self.add_hover_effect(delete_btn, '#e67e22', '#d35400')
        
        # Separator
        separator = tk.Frame(content_frame, height=2, bg='#3d3d5c')
        separator.pack(fill=tk.X, pady=20)
        
        # Exit Button
        exit_btn = tk.Button(content_frame, text="🚪  Exit Application",
                            command=self.root.quit,
                            bg='#c0392b', activebackground='#e74c3c',
                            **btn_style)
        exit_btn.pack(pady=8)
        self.add_hover_effect(exit_btn, '#e74c3c', '#c0392b')
        
        # Info Frame
        info_frame = tk.Frame(self.root, bg='#16213e', height=80)
        info_frame.pack(fill=tk.X, side=tk.BOTTOM)
        info_frame.pack_propagate(False)
        
        # Student count with icon
        student_count_frame = tk.Frame(info_frame, bg='#16213e')
        student_count_frame.pack(expand=True)
        
        icon_label = tk.Label(student_count_frame, text="👥", 
                             font=('Arial', 20), bg='#16213e')
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        info = tk.Label(student_count_frame, 
                       text=f"Registered Students: {len(self.system.known_face_names)}",
                       font=('Segoe UI', 12, 'bold'), bg='#16213e', fg='#00d4ff')
        info.pack(side=tk.LEFT)
        
        # Footer
        footer = tk.Label(info_frame, text="Powered by AI & Machine Learning",
                         font=('Segoe UI', 8), bg='#16213e', fg='#666666')
        footer.pack(side=tk.BOTTOM, pady=(0, 5))
    
    def add_hover_effect(self, button, hover_color, normal_color):
        """Add hover effect to buttons"""
        button.bind('<Enter>', lambda e: button.config(bg=hover_color))
        button.bind('<Leave>', lambda e: button.config(bg=normal_color))
    
    def custom_ask_student_name(self):
        """Custom dialog to get student name"""
        # Create custom dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("➕ Add New Student")
        dialog.geometry("600x500")
        dialog.configure(bg='#1a1a2e')
        dialog.resizable(False, False)
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (300)
        y = (dialog.winfo_screenheight() // 2) - (250)
        dialog.geometry(f'600x500+{x}+{y}')
        
        # Make it modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Result variable
        result = {'name': None}
        
        # Header Frame
        header_frame = tk.Frame(dialog, bg='#16213e', height=90)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Icon
        icon_label = tk.Label(header_frame, text="👤", 
                             font=('Arial', 35), bg='#16213e')
        icon_label.pack(pady=(10, 0))
        
        # Title
        title = tk.Label(header_frame, text="Add New Student",
                        font=('Segoe UI', 16, 'bold'), bg='#16213e', fg='#00d4ff')
        title.pack()
        
        # Content Frame
        content_frame = tk.Frame(dialog, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        # Instruction label
        instruction = tk.Label(content_frame, 
                              text="Enter the student's full name:",
                              font=('Segoe UI', 12), 
                              bg='#1a1a2e', fg='#ffffff')
        instruction.pack(pady=(0, 10))
        
        # Entry frame with border effect
        entry_frame = tk.Frame(content_frame, bg='#00d4ff', padx=2, pady=2)
        entry_frame.pack(pady=8)
        
        # Name entry
        name_var = tk.StringVar()
        name_entry = tk.Entry(entry_frame, 
                             textvariable=name_var,
                             font=('Segoe UI', 14),
                             bg='#2d2d44', 
                             fg='#ffffff',
                             insertbackground='#00d4ff',
                             relief=tk.FLAT,
                             width=30,
                             justify='center')
        name_entry.pack(ipady=10)
        name_entry.focus_set()
        
        # Hint label
        hint = tk.Label(content_frame, 
                       text="💡 Tip: Use full name for better identification",
                       font=('Segoe UI', 9), 
                       bg='#1a1a2e', fg='#a0a0a0')
        hint.pack(pady=(8, 10))
        
        # Error label (hidden initially)
        error_label = tk.Label(content_frame, 
                              text="",
                              font=('Segoe UI', 10), 
                              bg='#1a1a2e', fg='#ff6b6b')
        error_label.pack()
        
        # Button frame
        btn_frame = tk.Frame(content_frame, bg='#1a1a2e')
        btn_frame.pack(pady=20)
        
        def validate_and_submit():
            name = name_var.get().strip()
            if not name:
                error_label.config(text="❌ Please enter a name!")
                name_entry.config(bg='#ff4444')
                return
            elif len(name) < 2:
                error_label.config(text="❌ Name must be at least 2 characters!")
                name_entry.config(bg='#ff4444')
                return
            elif not all(c.isalnum() or c.isspace() for c in name):
                error_label.config(text="❌ Name should contain only letters and numbers!")
                name_entry.config(bg='#ff4444')
                return
            else:
                result['name'] = name
                dialog.destroy()
        
        def cancel():
            dialog.destroy()
        
        # Submit button with shadow effect
        submit_outer = tk.Frame(btn_frame, bg='#145a32', padx=2, pady=2)
        submit_outer.pack(side=tk.LEFT, padx=15)
        
        submit_btn = tk.Button(submit_outer, 
                              text="✓  Continue",
                              command=validate_and_submit,
                              font=('Segoe UI', 13, 'bold'),
                              bg='#28b463', fg='white',
                              activebackground='#52be80',
                              activeforeground='white',
                              width=15,
                              height=2,
                              borderwidth=2,
                              relief=tk.RAISED,
                              cursor='hand2')
        submit_btn.pack()
        
        def submit_hover_enter(e):
            submit_btn.config(bg='#52be80', relief=tk.SUNKEN)
            submit_outer.config(bg='#1e8449')
        
        def submit_hover_leave(e):
            submit_btn.config(bg='#28b463', relief=tk.RAISED)
            submit_outer.config(bg='#145a32')
        
        submit_btn.bind('<Enter>', submit_hover_enter)
        submit_btn.bind('<Leave>', submit_hover_leave)
        
        # Cancel button with shadow effect
        cancel_outer = tk.Frame(btn_frame, bg='#515a5a', padx=2, pady=2)
        cancel_outer.pack(side=tk.LEFT, padx=15)
        
        cancel_btn = tk.Button(cancel_outer, 
                              text="✖  Cancel",
                              command=cancel,
                              font=('Segoe UI', 13, 'bold'),
                              bg='#85929e', fg='white',
                              activebackground='#aab7b8',
                              activeforeground='white',
                              width=15,
                              height=2,
                              borderwidth=2,
                              relief=tk.RAISED,
                              cursor='hand2')
        cancel_btn.pack()
        
        def cancel_hover_enter(e):
            cancel_btn.config(bg='#aab7b8', relief=tk.SUNKEN)
            cancel_outer.config(bg='#626567')
        
        def cancel_hover_leave(e):
            cancel_btn.config(bg='#85929e', relief=tk.RAISED)
            cancel_outer.config(bg='#515a5a')
        
        cancel_btn.bind('<Enter>', cancel_hover_enter)
        cancel_btn.bind('<Leave>', cancel_hover_leave)
        
        # Bind Enter key
        name_entry.bind('<Return>', lambda e: validate_and_submit())
        dialog.bind('<Escape>', lambda e: cancel())
        
        # Wait for dialog to close
        self.root.wait_window(dialog)
        
        return result['name']
    
    def add_student(self):
        name = self.custom_ask_student_name()
        if name:
            # Create info dialog
            info_dialog = tk.Toplevel(self.root)
            info_dialog.title("📷 Camera Instructions")
            info_dialog.geometry("650x380")
            info_dialog.configure(bg='#1a1a2e')
            info_dialog.resizable(False, False)
            
            # Center dialog
            info_dialog.update_idletasks()
            x = (info_dialog.winfo_screenwidth() // 2) - (325)
            y = (info_dialog.winfo_screenheight() // 2) - (190)
            info_dialog.geometry(f'650x380+{x}+{y}')
            
            info_dialog.transient(self.root)
            info_dialog.grab_set()
            
            # Header
            header = tk.Frame(info_dialog, bg='#16213e', height=80)
            header.pack(fill=tk.X)
            header.pack_propagate(False)
            
            icon = tk.Label(header, text="📷", font=('Arial', 35), bg='#16213e')
            icon.pack(pady=(10, 0))
            
            title = tk.Label(header, text="Camera Instructions",
                            font=('Segoe UI', 14, 'bold'), bg='#16213e', fg='#00d4ff')
            title.pack()
            
            # Content
            content = tk.Frame(info_dialog, bg='#1a1a2e')
            content.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
            
            instructions = [
                "📸 Camera will open to capture 5 images",
                "👁️ Look directly at the camera",
                "↔️ Turn your face at different angles",
                "💡 Make sure lighting is good",
                "⌨️ Press SPACE to capture each photo",
                "⎋ Press ESC to cancel anytime"
            ]
            
            for inst in instructions:
                lbl = tk.Label(content, text=inst,
                              font=('Segoe UI', 11), 
                              bg='#1a1a2e', fg='#ffffff',
                              anchor='w')
                lbl.pack(fill=tk.X, pady=5)
            
            # Start button with improved design
            def start_capture():
                info_dialog.destroy()
                success = self.system.add_new_student(name)
                if success:
                    messagebox.showinfo("Success", f"✓ {name} added successfully!")
                    self.update_student_count()
                else:
                    messagebox.showerror("Error", "❌ Failed to add student")
            
            # Button container for centering
            btn_container = tk.Frame(content, bg='#1a1a2e')
            btn_container.pack(pady=30)
            
            # Start button with shadow effect
            start_outer = tk.Frame(btn_container, bg='#145a32', padx=3, pady=3)
            start_outer.pack(side=tk.LEFT, padx=15)
            
            start_btn = tk.Button(start_outer, 
                                 text="🚀  Start Capturing",
                                 command=start_capture,
                                 font=('Segoe UI', 14, 'bold'),
                                 bg='#28b463', fg='white',
                                 activebackground='#52be80',
                                 activeforeground='white',
                                 width=20,
                                 height=2,
                                 borderwidth=2,
                                 relief=tk.RAISED,
                                 cursor='hand2')
            start_btn.pack()
            
            def start_hover_enter(e):
                start_btn.config(bg='#52be80', relief=tk.SUNKEN)
                start_outer.config(bg='#1e8449')
            
            def start_hover_leave(e):
                start_btn.config(bg='#28b463', relief=tk.RAISED)
                start_outer.config(bg='#145a32')
            
            start_btn.bind('<Enter>', start_hover_enter)
            start_btn.bind('<Leave>', start_hover_leave)
            
            # Cancel button
            def cancel_capture():
                info_dialog.destroy()
            
            cancel_outer = tk.Frame(btn_container, bg='#515a5a', padx=3, pady=3)
            cancel_outer.pack(side=tk.LEFT, padx=15)
            
            cancel_btn = tk.Button(cancel_outer, 
                                  text="✖  Cancel",
                                  command=cancel_capture,
                                  font=('Segoe UI', 14, 'bold'),
                                  bg='#85929e', fg='white',
                                  activebackground='#aab7b8',
                                  activeforeground='white',
                                  width=20,
                                  height=2,
                                  borderwidth=2,
                                  relief=tk.RAISED,
                                  cursor='hand2')
            cancel_btn.pack()
            
            def cancel_hover_enter(e):
                cancel_btn.config(bg='#aab7b8', relief=tk.SUNKEN)
                cancel_outer.config(bg='#626567')
            
            def cancel_hover_leave(e):
                cancel_btn.config(bg='#85929e', relief=tk.RAISED)
                cancel_outer.config(bg='#515a5a')
            
            cancel_btn.bind('<Enter>', cancel_hover_enter)
            cancel_btn.bind('<Leave>', cancel_hover_leave)
            
            info_dialog.bind('<Return>', lambda e: start_capture())
            info_dialog.bind('<Escape>', lambda e: info_dialog.destroy())
                
    def start_recognition(self):
        if len(self.system.known_face_names) == 0:
            messagebox.showwarning("Warning", "No students registered yet!")
            return
            
        messagebox.showinfo("Info", "Camera will start. Press 'q' to stop recognition.")
        try:
            count = self.system.recognize_faces()
            if count == 0:
                messagebox.showwarning("Info", "No attendance marked. Camera may not have opened properly.")
            else:
                messagebox.showinfo("Attendance Complete", f"Attendance marked for {count} students")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
        
    def view_attendance(self):
        date_string = datetime.now().strftime('%Y-%m-%d')
        filename = f'attendance_records/attendance_{date_string}.csv'
        
        if not os.path.exists(filename):
            messagebox.showinfo("Info", "No attendance records for today")
            return
            
        # Read and display attendance
        with open(filename, 'r') as f:
            content = f.read()
            
        # Create new window with modern design
        window = tk.Toplevel(self.root)
        window.title(f"📊 Attendance - {date_string}")
        window.geometry("600x500")
        window.configure(bg='#1a1a2e')
        window.resizable(False, False)
        
        # Header
        header = tk.Frame(window, bg='#16213e', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_label = tk.Label(header, text=f"📊 Attendance Record - {date_string}",
                               font=('Segoe UI', 14, 'bold'), 
                               bg='#16213e', fg='#00d4ff')
        header_label.pack(expand=True)
        
        # Text frame with scrollbar
        text_frame = tk.Frame(window, bg='#1a1a2e')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text = tk.Text(text_frame, font=('Consolas', 11), 
                      bg='#2d2d44', fg='#ffffff',
                      yscrollcommand=scrollbar.set,
                      padx=10, pady=10,
                      relief=tk.FLAT)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)
        
        text.insert('1.0', content)
        text.config(state=tk.DISABLED)
        
        # Close button
        close_btn = tk.Button(window, text="✖ Close",
                             command=window.destroy,
                             font=('Segoe UI', 11, 'bold'),
                             bg='#c0392b', fg='white',
                             activebackground='#e74c3c',
                             width=15, height=2,
                             border=0, cursor='hand2')
        close_btn.pack(pady=(0, 20))
    
    def delete_student(self):
        """Delete a registered student"""
        if len(self.system.known_face_names) == 0:
            messagebox.showwarning("Warning", "No students registered yet!")
            return
        
        # Create selection window with modern design
        delete_window = tk.Toplevel(self.root)
        delete_window.title("🗑️ Delete Student")
        delete_window.geometry("500x600")
        delete_window.configure(bg='#1a1a2e')
        delete_window.resizable(False, False)
        
        # Header
        header = tk.Frame(delete_window, bg='#16213e', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_icon = tk.Label(header, text="🗑️", 
                              font=('Arial', 30), bg='#16213e')
        header_icon.pack(pady=(10, 0))
        
        title = tk.Label(header, text="Select Student to Delete",
                        font=('Segoe UI', 16, 'bold'), bg='#16213e', fg='#ff6b6b')
        title.pack()
        
        # Frame for listbox and scrollbar
        list_frame = tk.Frame(delete_window, bg='#1a1a2e')
        list_frame.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)
        
        list_frame = tk.Frame(delete_window, bg='#1a1a2e')
        list_frame.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox with students
        listbox = tk.Listbox(list_frame, font=('Segoe UI', 12), 
                            yscrollcommand=scrollbar.set,
                            bg='#2d2d44', fg='#ffffff',
                            selectmode=tk.SINGLE,
                            selectbackground='#0f4c75',
                            selectforeground='#ffffff',
                            height=12,
                            relief=tk.FLAT,
                            highlightthickness=0)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Add students to listbox
        for i, name in enumerate(self.system.get_all_students(), 1):
            listbox.insert(tk.END, f"  {i}. {name}")
        
        # Info label
        info = tk.Label(delete_window, 
                       text=f"👥 Total Students: {len(self.system.known_face_names)}",
                       font=('Segoe UI', 11, 'bold'), bg='#1a1a2e', fg='#00d4ff')
        info.pack(pady=10)
        
        # Button frame
        btn_frame = tk.Frame(delete_window, bg='#1a1a2e')
        btn_frame.pack(pady=20)
        
        def confirm_delete():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a student to delete")
                return
            
            # Extract student name (remove numbering)
            student_text = listbox.get(selection[0])
            student_name = student_text.split(". ", 1)[1] if ". " in student_text else student_text.strip()
            
            # Confirm deletion
            response = messagebox.askyesno("Confirm Delete", 
                                          f"Are you sure you want to delete {student_name}?\n\n"
                                          f"This will:\n"
                                          f"• Remove face encodings\n"
                                          f"• Delete student images\n"
                                          f"• Cannot be undone!")
            
            if response:
                success = self.system.delete_student(student_name)
                if success:
                    messagebox.showinfo("Success", f"{student_name} deleted successfully!")
                    self.update_student_count()
                    delete_window.destroy()
                else:
                    messagebox.showerror("Error", f"Failed to delete {student_name}")
        
        # Delete button with hover effect
        delete_btn = tk.Button(btn_frame, text="🗑️ Delete Selected",
                              command=confirm_delete,
                              font=('Segoe UI', 12, 'bold'),
                              bg='#c0392b', fg='white',
                              activebackground='#e74c3c',
                              width=18, height=2,
                              border=0, cursor='hand2',
                              relief=tk.FLAT)
        delete_btn.pack(side=tk.LEFT, padx=10)
        delete_btn.bind('<Enter>', lambda e: delete_btn.config(bg='#e74c3c'))
        delete_btn.bind('<Leave>', lambda e: delete_btn.config(bg='#c0392b'))
        
        # Cancel button with hover effect
        cancel_btn = tk.Button(btn_frame, text="✖ Cancel",
                              command=delete_window.destroy,
                              font=('Segoe UI', 12, 'bold'),
                              bg='#7f8c8d', fg='white',
                              activebackground='#95a5a6',
                              width=18, height=2,
                              border=0, cursor='hand2',
                              relief=tk.FLAT)
        cancel_btn.pack(side=tk.LEFT, padx=10)
        cancel_btn.bind('<Enter>', lambda e: cancel_btn.config(bg='#95a5a6'))
        cancel_btn.bind('<Leave>', lambda e: cancel_btn.config(bg='#7f8c8d'))
        
    def update_student_count(self):
        """Update the student count display"""
        def update_label(widget):
            for child in widget.winfo_children():
                if isinstance(child, tk.Label) and "Registered Students" in child.cget("text"):
                    child.config(text=f"Registered Students: {len(self.system.known_face_names)}")
                    return True
                if update_label(child):
                    return True
            return False
        update_label(self.root)

def main():
    root = tk.Tk()
    app = AttendanceSystemGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
