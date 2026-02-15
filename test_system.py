"""
Test script to verify camera and dependencies
Run this before using the main application
"""

import sys

def test_imports():
    """Test if all required packages are installed"""
    print("\n" + "="*50)
    print("Testing Package Imports...")
    print("="*50 + "\n")
    
    packages = {
        'cv2': 'opencv-python',
        'face_recognition': 'face_recognition',
        'numpy': 'numpy',
        'PIL': 'Pillow',
        'tkinter': 'tkinter (built-in)'
    }
    
    all_good = True
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✓ {name:30} - OK")
        except ImportError as e:
            print(f"✗ {name:30} - MISSING")
            all_good = False
    
    return all_good

def test_camera():
    """Test if camera is accessible"""
    print("\n" + "="*50)
    print("Testing Camera...")
    print("="*50 + "\n")
    
    try:
        import cv2
        
        # Try different camera indices
        for i in range(3):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    height, width = frame.shape[:2]
                    print(f"✓ Camera {i} is working!")
                    print(f"  Resolution: {width}x{height}")
                    cap.release()
                    
                    # Show camera feed for 3 seconds
                    print("\nShowing camera feed for 3 seconds...")
                    cap = cv2.VideoCapture(i)
                    import time
                    start = time.time()
                    
                    while time.time() - start < 3:
                        ret, frame = cap.read()
                        if ret:
                            cv2.putText(frame, "Camera Test - Press 'q' to skip", 
                                      (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                                      0.7, (0, 255, 0), 2)
                            cv2.imshow('Camera Test', frame)
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                    
                    cap.release()
                    cv2.destroyAllWindows()
                    return True
                else:
                    cap.release()
            else:
                cap.release()
        
        print("✗ No working camera found!")
        print("  Please check if camera is connected and not in use")
        return False
        
    except Exception as e:
        print(f"✗ Camera test failed: {e}")
        return False

def test_face_detection():
    """Test face detection functionality"""
    print("\n" + "="*50)
    print("Testing Face Detection...")
    print("="*50 + "\n")
    
    try:
        import cv2
        import face_recognition
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("✗ Cannot open camera")
            return False
        
        print("Looking for faces... (5 seconds)")
        print("Please look at the camera!\n")
        
        import time
        start = time.time()
        face_found = False
        
        while time.time() - start < 5:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            face_locations = face_recognition.face_locations(rgb_frame)
            
            # Draw rectangles
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                face_found = True
            
            cv2.putText(frame, f"Faces detected: {len(face_locations)}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (0, 255, 0), 2)
            cv2.putText(frame, "Press 'q' to skip", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (0, 255, 0), 2)
            cv2.imshow('Face Detection Test', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if face_found:
            print("✓ Face detection is working!")
            return True
        else:
            print("⚠ No faces detected (but system is working)")
            print("  Make sure you are in good lighting")
            return True
            
    except Exception as e:
        print(f"✗ Face detection test failed: {e}")
        return False

def main():
    print("\n")
    print("╔" + "="*48 + "╗")
    print("║  Face Recognition Attendance System - Test  ║")
    print("╚" + "="*48 + "╝")
    
    # Test imports
    imports_ok = test_imports()
    
    if not imports_ok:
        print("\n" + "="*50)
        print("⚠ INSTALLATION INCOMPLETE")
        print("="*50)
        print("\nPlease install missing packages:")
        print("  pip install -r requirements.txt")
        return
    
    # Test camera
    camera_ok = test_camera()
    
    if not camera_ok:
        print("\n" + "="*50)
        print("⚠ CAMERA ISSUE")
        print("="*50)
        print("\nPlease check:")
        print("  1. Camera is connected")
        print("  2. Camera is not being used by another application")
        print("  3. Camera permissions are granted")
        return
    
    # Test face detection
    detection_ok = test_face_detection()
    
    # Final result
    print("\n" + "="*50)
    if imports_ok and camera_ok and detection_ok:
        print("✓ ALL TESTS PASSED!")
        print("="*50)
        print("\nYour system is ready!")
        print("Run: python main.py")
    else:
        print("⚠ SOME TESTS FAILED")
        print("="*50)
        print("\nPlease fix the issues above before running main.py")
    print("\n")

if __name__ == "__main__":
    main()
