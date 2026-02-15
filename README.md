# Face Recognition Attendance System

एक AI/ML आधारित चेहरा पहचान प्रणाली जो स्वचालित रूप से उपस्थिति दर्ज करती है।

## Features

- **Real-time Face Recognition**: OpenCV और face_recognition library का उपयोग करके वास्तविक समय में चेहरा पहचान
- **Automatic Attendance**: पहचाने गए छात्रों की स्वचालित रूप से उपस्थिति दर्ज करें
- **Easy Student Registration**: नए छात्रों को आसानी से सिस्टम में जोड़ें
- **GUI Interface**: उपयोग में आसान ग्राफिकल इंटरफेस
- **CSV Records**: CSV फॉर्मेट में दैनिक उपस्थिति रिकॉर्ड
- **Face Encoding Storage**: तेज़ पहचान के लिए चेहरे की विशेषताएं सहेजना

## System Requirements

- Python 3.7 या उससे ऊपर
- Webcam/Camera
- Windows/Linux/Mac OS

## Installation

### Step 1: Clone या Download करें

```bash
git clone <repository-url>
cd Face_Recognition_Attendance_System
```

### Step 2: Dependencies Install करें

**Windows के लिए:**

```bash
pip install -r requirements.txt
```

**Linux/Mac के लिए:**

```bash
pip3 install -r requirements.txt
```

### Step 3: dlib के लिए विशेष निर्देश

अगर dlib इंस्टॉल करने में समस्या है:

**Windows:**
```bash
# Visual Studio Build Tools डाउनलोड करें
# फिर चलाएं:
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

### System चलाना

```bash
python main.py
```

### Features का उपयोग

#### 1. नया Student जोड़ना

1. "Add New Student" बटन पर क्लिक करें
2. Student का नाम डालें
3. Camera खुलेगा - SPACE दबाकर 5 फोटो लें
4. अलग-अलग angles से चेहरा दिखाएं
5. ESC दबाकर cancel कर सकते हैं

#### 2. Attendance लेना

1. "Start Attendance Recognition" बटन पर क्लिक करें
2. Camera में चेहरा दिखाएं
3. System automatically attendance मार्क करेगा
4. 'q' दबाकर बंद करें

#### 3. Attendance देखना

1. "View Today's Attendance" बटन पर क्लिक करें
2. आज की सभी entries दिखेंगी

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
- OpenCV का Haar Cascade या HOG algorithm उपयोग करता है
- Real-time में video stream से चेहरे detect करता है

### 2. Face Recognition
- face_recognition library (dlib के ऊपर बनी)
- 128-dimensional face encodings बनाता है
- Euclidean distance से चेहरे match करता है

### 3. Attendance Marking
- पहचाने गए चेहरे को CSV file में log करता है
- Duplicate entries prevent करता है
- Date और Time के साथ record करता है

## Technical Details

### Algorithms Used

1. **Face Detection**: HOG (Histogram of Oriented Gradients)
2. **Face Recognition**: Deep Learning-based facial recognition model
3. **Face Encoding**: 128-dimensional embedding vectors
4. **Matching**: Face distance calculation using Euclidean distance

### Libraries & Technologies

- **OpenCV**: Computer vision और image processing
- **face_recognition**: Facial recognition (dlib wrapper)
- **NumPy**: Numerical computations
- **Tkinter**: GUI development
- **PIL**: Image handling
- **CSV**: Data storage

## Troubleshooting

### Common Issues

**Issue 1: Camera नहीं खुल रहा**
```python
# main.py में VideoCapture number बदलें
cap = cv2.VideoCapture(0)  # 0 को 1 या 2 से replace करें
```

**Issue 2: Face detect नहीं हो रहा**
- अच्छी lighting में काम करें
- Camera के सामने सीधे देखें
- पास आएं

**Issue 3: Recognition accuracy कम है**
- Training के समय अलग-अलग angles से फोटो लें
- अच्छी lighting में training करें
- Images की संख्या बढ़ाएं (code में `num_images=5` को बढ़ाएं)

**Issue 4: Slow performance**
```python
# process_every_n_frames की value बढ़ाएं
process_every_n_frames = 3  # 2 से 3 या 4 करें
```

## Customization

### Recognition Tolerance बदलना

```python
# main.py में tolerance value बदलें
matches = face_recognition.compare_faces(
    self.known_face_encodings, 
    face_encoding, 
    tolerance=0.6  # कम value = ज्यादा strict
)
```

### Capture Images Count बदलना

```python
# add_new_student function में
self.system.add_new_student(name.strip(), num_images=10)  # 5 से 10
```

## Future Enhancements

- 📊 Attendance analytics और reports
- 📧 Email notifications
- 🗄️ Database integration (SQLite/MySQL)
- 🌐 Web interface
- 📱 Mobile app
- 🔐 Admin panel
- 📸 Multiple camera support
- 🎯 Unknown face alerts

## Contributing

Contributions welcome हैं! Pull requests submit करें।

## License

MIT License - इस project को freely उपयोग करें।

## Contact

किसी भी सवाल के लिए issue create करें।

---

## Quick Start Guide

```bash
# Install
pip install -r requirements.txt

# Run
python main.py

# Add students और attendance लेना शुरू करें!
```

**Made with ❤️ using Python, OpenCV, and face_recognition**
