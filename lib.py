import subprocess
import sys
import os

dependencias = [
    "pillow",
    "opencv-python",
    "easyocr",
    "pandas",
    "rapidfuzz"
]

for pacote in dependencias:
    subprocess.run([sys.executable, "-m", "pip", "install", "--user", pacote], check=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
main_script = os.path.join(BASE_DIR, "main.py")

subprocess.run([sys.executable, main_script], check=True)
