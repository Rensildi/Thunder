import subprocess
import sys
import time

# Run app.py as a background process
app_process = subprocess.Popen([sys.executable, "app.py"])

# Wait for app.py o start
time.sleep(0.5)

# Run main.py in the foreground
subprocess.run([sys.executable, "main.py"])

# Wait for main.py to finish, then terminate app.py
app_process.terminate()

