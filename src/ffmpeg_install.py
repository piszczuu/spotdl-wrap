import subprocess
import platform
from pathlib import Path

def install_ffmpeg():
    try:
        # Sprawdź, czy FFmpeg jest już dostępny
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("✅ FFmpeg jest już zainstalowany.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("🔍 FFmpeg nie jest zainstalowany. Próbuję zainstalować...")

        # Instalacja w zależności od systemu operacyjnego
        system = platform.system()
        try:
            if system == "Windows":
                # Instalacja przez winget (Windows 10/11)
                subprocess.run(["winget", "install", "ffmpeg"], check=True)
            elif system == "Linux":
                # Instalacja przez apt (Debian/Ubuntu)
                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"], check=True)
            elif system == "Darwin":  # macOS
                subprocess.run(["brew", "install", "ffmpeg"], check=True)
            print("✅ FFmpeg został pomyślnie zainstalowany!")
            return True
        except Exception as e:
            print(f"❌ Nie udało się zainstalować FFmpeg: {e}")
            print("ℹ️ Ręczna instalacja wymagana: https://ffmpeg.org/download.html")
            return False