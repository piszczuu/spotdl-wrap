import subprocess
from src.settings import SPOTDL_SETTINGS



def download_song(url, settings):
    command = ["spotdl", "download", url]

    for key, value in settings.items():
        if value is None:  # flaga CLI
            command.append(key)
        else:
            command.extend([key, str(value)])

    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to download: {url}, error: {e}")
        return False


if __name__ == "__main__":
    print("test")
