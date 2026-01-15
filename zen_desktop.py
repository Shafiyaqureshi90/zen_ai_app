import webview
import subprocess
import time
import sys
import subprocess

subprocess.Popen([sys.executable, "-m", "streamlit", "run", "example.py"])


# Step 2: Wait for Streamlit to load
time.sleep(5)  # Increase if needed

# Step 3: Open Streamlit in a native window
webview.create_window("Zen-AI: Mindful Productivity", "http://localhost:8501", width=1000, height=800)
webview.start()

# Step 4: When done, kill Streamlit server
process.terminate()
