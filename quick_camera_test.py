"""
Quick Camera Test Script
Run this to check if your camera is working
"""

import cv2
import sys

def test_camera(camera_index=0):
    """Test a specific camera"""
    print(f"\n{'='*50}")
    print(f"Testing Camera {camera_index}...")
    print('='*50)
    
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"✗ Camera {camera_index} could not be opened")
        return False
    
    print(f"✓ Camera {camera_index} opened successfully!")
    
    # Try to read a frame
    ret, frame = cap.read()
    
    if not ret:
        print(f"✗ Could not read frame from camera {camera_index}")
        cap.release()
        return False
    
    height, width = frame.shape[:2]
    print(f"✓ Frame read successful!")
    print(f"  Resolution: {width}x{height}")
    
    print(f"\nShowing camera feed for 5 seconds...")
    print("Press 'q' to quit early")
    
    import time
    start_time = time.time()
    
    while time.time() - start_time < 5:
        ret, frame = cap.read()
        if not ret:
            print("✗ Frame read failed during test")
            break
        
        # Add text to frame
        cv2.putText(frame, f"Camera {camera_index} Test", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'q' to quit", (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        elapsed = int(5 - (time.time() - start_time))
        cv2.putText(frame, f"Time remaining: {elapsed}s", (10, 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow(f'Camera {camera_index} Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Test stopped by user")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"✓ Camera {camera_index} test completed successfully!\n")
    return True

def find_all_cameras():
    """Find all available cameras"""
    print("\n" + "="*50)
    print("Searching for all available cameras...")
    print("="*50 + "\n")
    
    available_cameras = []
    
    for i in range(10):  # Check first 10 indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                h, w = frame.shape[:2]
                available_cameras.append(i)
                print(f"✓ Camera {i} found - Resolution: {w}x{h}")
            cap.release()
    
    if not available_cameras:
        print("✗ No cameras found!")
    else:
        print(f"\n✓ Found {len(available_cameras)} camera(s): {available_cameras}\n")
    
    return available_cameras

def main():
    print("\n" + "="*50)
    print("      QUICK CAMERA TEST")
    print("="*50)
    
    # Find all cameras
    cameras = find_all_cameras()
    
    if not cameras:
        print("\n❌ NO CAMERAS FOUND!\n")
        print("Troubleshooting steps:")
        print("1. Check if camera is connected")
        print("2. Close other apps using camera (Teams, Zoom, Skype)")
        print("3. Check camera permissions in Windows Settings")
        print("4. Try restarting your computer")
        print("\nFor more help, see CAMERA_TROUBLESHOOTING.md\n")
        return
    
    # Test each camera
    for camera_index in cameras:
        success = test_camera(camera_index)
        if not success:
            print(f"⚠ Camera {camera_index} test failed\n")
    
    print("\n" + "="*50)
    print("RECOMMENDATION:")
    print("="*50)
    
    if cameras:
        recommended = cameras[0]
        print(f"\nUse Camera {recommended} in your application")
        print(f"\nTo change camera in the application:")
        print(f"  1. Open config.py")
        print(f"  2. Change CAMERA_INDEX = {recommended}")
        print(f"  3. Restart the application\n")
    
    print("\nIf camera window doesn't open in main application:")
    print("1. Make sure no other app is using the camera")
    print("2. Check camera permissions")
    print("3. Try running as administrator")
    print("4. See CAMERA_TROUBLESHOOTING.md for more help\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        print("Please check:")
        print("1. opencv-python is installed: pip install opencv-python")
        print("2. Camera drivers are working")
        print("3. Camera permissions are granted\n")
        sys.exit(1)
