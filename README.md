# Face Recognition Attendance System

An AI/ML-based face recognition system that automatically records attendance.

## Features

- **Real-time Face Recognition**: Real-time face detection using OpenCV and face_recognition library
- **Automatic Attendance**: Automatically record attendance for recognized students
- **Easy Student Registration**: Easily add new students to the system
- **GUI Interface**: User-friendly graphical interface
- **CSV Records**: Daily attendance records in CSV format
- **Face Encoding Storage**: Store facial features for fast recognition

## System Requirements

- Python 3.7 or higher
- Webcam/Camera
- Windows/Linux/Mac OS

## Installation

### Step 1: Clone or Download

```bash
git clone https://github.com/imohdsakib/Face_Recognition_Attendance_System.git
cd Face_Recognition_Attendance_System
```

### Step 2: Install Dependencies

**For Windows:**

```bash
pip install -r requirements.txt
```

**For Linux/Mac:**

```bash
pip3 install -r requirements.txt
```

### Step 3: Special Instructions for dlib

If you face issues installing dlib:

**Windows:**
```bash
# Download Visual Studio Build Tools
# Then run:
pip install cmake
pip install dlib
```

**Mac:**
```bash
brew install cmake
pip install dlib
```

**Linux:**
```bash
sudo apt-get install cmake
sudo apt-get install python3-dev
pip install dlib
```

## Usage

### Running the System

```bash
python main.py
```

### Using Features

#### 1. Adding a New Student

1. Click on "Add New Student" button
2. Enter student's name
3. Camera will open - Press SPACE to capture 5 photos
4. Show your face from different angles
5. Press ESC to cancel

#### 2. Taking Attendance

1. Click on "Start Attendance Recognition" button
2. Show your face to the camera
3. System will automatically mark attendance
4. Press 'q' to close

#### 3. Viewing Attendance

1. Click on "View Today's Attendance" button
2. All today's entries will be displayed

## Project Structure

```
Face_Recognition_Attendance_System/
│
├── main.py                          # Main application file
├── requirements.txt                 # Python dependencies
├── README.md                        # Documentation
│
├── students_images/                 # Student photos storage
│   ├── Student_Name_1/
│   │   ├── image_0.jpg
│   │   ├── image_1.jpg
│   │   └── ...
│   └── Student_Name_2/
│       └── ...
│
├── attendance_records/              # Attendance CSV files
│   ├── attendance_2026-02-15.csv
│   └── ...
│
└── encodings/                       # Face encodings storage
    └── face_encodings.pkl
```

## How It Works

### 1. Face Detection
- Uses OpenCV's Haar Cascade or HOG algorithm
- Detects faces from video stream in real-time

### 2. Face Recognition
- face_recognition library (built on top of dlib)
- Creates 128-dimensional face encodings
- Matches faces using Euclidean distance

### 3. Attendance Marking
- Logs recognized faces to CSV file
- Prevents duplicate entries
- Records with date and time

## Technical Details

### Algorithms Used

1. **Face Detection**: HOG (Histogram of Oriented Gradients)
2. **Face Recognition**: Deep Learning-based facial recognition model
3. **Face Encoding**: 128-dimensional embedding vectors
4. **Matching**: Face distance calculation using Euclidean distance

### Libraries & Technologies

- **OpenCV**: Computer vision and image processing
- **face_recognition**: Facial recognition (dlib wrapper)
- **NumPy**: Numerical computations
- **Tkinter**: GUI development
- **PIL**: Image handling
- **CSV**: Data storage

## Future Enhancements

- 📊 Attendance analytics and reports
- 📧 Email notifications
- 🗄️ Database integration (SQLite/MySQL)
- 🌐 Web interface
- 📱 Mobile app
- 🔐 Admin panel
- 📸 Multiple camera support
- 🎯 Unknown face alerts

**Made with ❤️ using Python, OpenCV, and face_recognition**
