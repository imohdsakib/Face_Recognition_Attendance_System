# Face Recognition Attendance System Configuration

# Recognition Settings
RECOGNITION_TOLERANCE = 0.6  # Lower value = stricter matching (0.4 to 0.7)
PROCESS_EVERY_N_FRAMES = 2   # Process every nth frame (higher = faster but less accurate)
FRAME_RESIZE_FACTOR = 0.25   # Resize factor for processing (0.25 = 25% of original)

# Student Registration Settings
NUM_IMAGES_PER_STUDENT = 5   # Number of images to capture per student

# Camera Settings
CAMERA_INDEX = 0             # Camera device index (0, 1, 2, etc.)

# File Paths
STUDENTS_DIR = 'students_images'
ATTENDANCE_DIR = 'attendance_records'
ENCODINGS_DIR = 'encodings'
ENCODINGS_FILE = 'encodings/face_encodings.pkl'

# GUI Settings
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 400
THEME_COLOR = '#2c3e50'
BUTTON_COLOR = '#3498db'

# Attendance Settings
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
