# 📷 Camera Troubleshooting Guide

## Camera Window नहीं खुल रही है?

### Quick Fixes:

#### 1️⃣ **Camera Index बदलें**

अगर camera window नहीं खुल रही है, तो ये try करें:

```python
# config.py में CAMERA_INDEX बदलें
CAMERA_INDEX = 0  # Default
# या
CAMERA_INDEX = 1  # External webcam
# या
CAMERA_INDEX = 2  # Third camera
```

#### 2️⃣ **अन्य Applications बंद करें**

Camera को केवल एक application एक समय में use कर सकती है। बंद करें:
- Microsoft Teams
- Zoom
- Skype
- WhatsApp Desktop
- Camera App (Windows)
- Any other video apps

#### 3️⃣ **Camera Permissions Check करें**

**Windows 10/11:**
1. Settings → Privacy → Camera
2. "Allow apps to access your camera" को ON करें
3. "Allow desktop apps to access your camera" को ON करें

#### 4️⃣ **Camera Driver Update करें**

1. Device Manager खोलें (Win + X → Device Manager)
2. "Cameras" या "Imaging devices" expand करें
3. अपना camera right-click करें → "Update driver"

#### 5️⃣ **Terminal में Test करें**

```bash
python test_system.py
```

ये script check करेगा:
- Camera working है या नहीं
- Face detection working है या नहीं

---

## Error Messages और Solutions:

### Error: "Could not open camera"

**Possible Reasons:**
1. Camera दूसरी application में use हो रही है
2. Camera permissions denied हैं
3. Camera properly connected नहीं है
4. Wrong camera index

**Solution:**
```python
# main.py में camera index try करें
cap = cv2.VideoCapture(1)  # 0 की जगह 1 या 2
```

### Error: "Failed to read frame"

**Possible Reasons:**
1. Camera disconnect हो गई
2. Low system resources
3. Camera hardware issue

**Solution:**
1. Camera cable check करें (if external)
2. USB port बदलें
3. System restart करें

### Camera खुलती है लेकिन freeze हो जाती है

**Solution:**
```python
# config.py में process_every_n_frames बढ़ाएं
PROCESS_EVERY_N_FRAMES = 3  # या 4
```

---

## Manual Camera Test:

### Python से directly test करें:

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

Save karke run करें:
```bash
python camera_test.py
```

---

## System-specific Fixes:

### Windows:

```bash
# 1. Camera app से test करें
# Start → Camera

# 2. PowerShell में camera devices देखें
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

# 2. Terminal को camera access allow करें

# 3. Check camera
system_profiler SPCameraDataType
```

---

## Advanced Troubleshooting:

### Multiple Cameras का पता लगाएं:

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

### Camera Resolution बदलें:

```python
# main.py में VideoCapture के बाद add करें
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

---

## Still Not Working?

### Alternative Solutions:

1. **USB Webcam use करें**
   - Internal camera issue हो सकती है
   - External USB webcam खरीदें

2. **Phone को Webcam बनाएं**
   - Apps: DroidCam, iVCam, EpocCam
   - USB या WiFi से connect करें

3. **Virtual Camera use करें**
   - OBS Virtual Camera
   - ManyCam
   - Split Camera

---

## Contact Info:

अगर फिर भी problem है तो:
1. Error message का screenshot लें
2. Terminal output copy करें
3. Issue create करें with details

---

**💡 Pro Tip:** हमेशा `test_system.py` पहले चलाएं application से पहले!

```bash
python test_system.py
```
