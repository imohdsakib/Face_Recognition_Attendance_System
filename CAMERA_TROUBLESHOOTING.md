# 📷 Camera Troubleshooting Guide

## Camera Window Not Opening?

### Quick Fixes:

#### 1️⃣ **Change Camera Index**

If camera window is not opening, try this:

```python
# Change CAMERA_INDEX in config.py
CAMERA_INDEX = 0  # Default
# or
CAMERA_INDEX = 1  # External webcam
# or
CAMERA_INDEX = 2  # Third camera
```

#### 2️⃣ **Close Other Applications**

Camera can only be used by one application at a time. Close:
- Microsoft Teams
- Zoom
- Skype
- WhatsApp Desktop
- Camera App (Windows)
- Any other video apps

#### 3️⃣ **Check Camera Permissions**

**Windows 10/11:**
1. Settings → Privacy → Camera
2. Turn ON "Allow apps to access your camera"
3. Turn ON "Allow desktop apps to access your camera"

#### 4️⃣ **Update Camera Driver**

1. Open Device Manager (Win + X → Device Manager)
2. Expand "Cameras" or "Imaging devices"
3. Right-click your camera → "Update driver"

#### 5️⃣ **Test in Terminal**

```bash
python test_system.py
```

This script will check:
- Whether camera is working
- Whether face detection is working

---

## Error Messages and Solutions:

### Error: "Could not open camera"

**Possible Reasons:**
1. Camera is being used by another application
2. Camera permissions are denied
3. Camera is not properly connected
4. Wrong camera index

**Solution:**
```python
# Try different camera index in main.py
cap = cv2.VideoCapture(1)  # Try 1 or 2 instead of 0
```

### Error: "Failed to read frame"

**Possible Reasons:**
1. Camera got disconnected
2. Low system resources
3. Camera hardware issue

**Solution:**
1. Check camera cable (if external)
2. Change USB port
3. Restart system

### Camera opens but freezes

**Solution:**
```python
# Increase process_every_n_frames in config.py
PROCESS_EVERY_N_FRAMES = 3  # or 4
```

---

## Manual Camera Test:

### Test directly with Python:

```python
import cv2

# Camera test
cap = cv2.VideoCapture(0)

if cap.isOpened():
    print("✓ Camera is working!")
    ret, frame = cap.read()
    if ret:
        print("✓ Frame read successful!")
        cv2.imshow('Test', frame)
        cv2.waitKey(3000)  # 3 seconds
else:
    print("✗ Camera failed to open")
    print("Try:")
    print("  cv2.VideoCapture(1)")
    print("  cv2.VideoCapture(2)")

cap.release()
cv2.destroyAllWindows()
```

Save and run:
```bash
python camera_test.py
```

---

## System-specific Fixes:

### Windows:

```bash
# 1. Test with Camera app
# Start → Camera

# 2. View camera devices in PowerShell
Get-PnpDevice | Where-Object {$_.FriendlyName -like "*camera*"}
```

### Linux:

```bash
# 1. Check available cameras
ls -l /dev/video*

# 2. Install v4l-utils
sudo apt-get install v4l-utils

# 3. List cameras
v4l2-ctl --list-devices

# 4. Test camera
ffplay /dev/video0
```

### Mac:

```bash
# 1. Check camera permissions
# System Preferences → Security & Privacy → Camera

# 2. Allow camera access to Terminal

# 3. Check camera
system_profiler SPCameraDataType
```

---

## Advanced Troubleshooting:

### Find Multiple Cameras:

```python
import cv2

def find_cameras():
    """Find all available cameras"""
    available = []
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                h, w = frame.shape[:2]
                available.append({
                    'index': i,
                    'resolution': f"{w}x{h}"
                })
                print(f"Camera {i}: {w}x{h}")
            cap.release()
    return available

cameras = find_cameras()
print(f"\nFound {len(cameras)} camera(s)")
```

### Change Camera Resolution:

```python
# Add after VideoCapture in main.py
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

---

## Still Not Working?

### Alternative Solutions:

1. **Use USB Webcam**
   - Internal camera may have issues
   - Buy external USB webcam

2. **Use Phone as Webcam**
   - Apps: DroidCam, iVCam, EpocCam
   - Connect via USB or WiFi

3. **Use Virtual Camera**
   - OBS Virtual Camera
   - ManyCam
   - Split Camera

---

## Contact Info:

If you still have problems:
1. Take screenshot of error message
2. Copy terminal output
3. Create an issue with details

---

**💡 Pro Tip:** Always run `test_system.py` first before the application!

```bash
python test_system.py
```
