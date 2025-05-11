from utils import get_desktop_path
import os, json

def ensure_logs_directory():
    logs_path = os.path.join(get_desktop_path(), "spotdl_wrap", "logs")
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)