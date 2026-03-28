# test.py   (Place this in your ampy folder)
import sys
import os

# Add current directory to Python path so it can find the local ampy package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ampy.pyboard import Pyboard
from ampy.files import Files     # ← This should work now

# ================== CONFIGURE HERE ==================
PORT = "/dev/ttyUSB0"        # Change this to your actual port
# Common ports:
# Linux:   "/dev/ttyUSB0" or "/dev/ttyACM0"
# macOS:   "/dev/cu.usbserial-..." 
# Windows: "COM3"

BAUDRATE = 115200
# ====================================================

print(f"Connecting to board on {PORT}...")

pyb = Pyboard(PORT, baudrate=BAUDRATE)
files = Files(pyb)

# Create a reasonably large test file (you can increase this)
test_code = """# Test large file upload
print("Hello from large uploaded file!")
for i in range(200):
    print(f"Line {i}: Testing ampy put function")
print("Upload test completed successfully!")
""" * 80   # This should create ~300+ lines

local_filename = "test_large_upload.py"

with open(local_filename, "w", encoding="utf-8") as f:
    f.write(test_code)

print(f"Created local test file: {local_filename} ({len(test_code):,} bytes)")

# === Use your improved put function ===
try:
    with open(local_filename, "rb") as f:
        data = f.read()

    print("Starting upload using your modified put()...")
    files.put(local_filename, data)

    print("Upload completed successfully!")
    print("Files on board:")
    print(files.ls())

except Exception as e:
    print(f"❌ Upload failed: {e}")

finally:
    pyb.close()
    print("Connection closed.")