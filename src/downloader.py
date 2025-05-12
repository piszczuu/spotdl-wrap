import subprocess, os, json

#returns spotdl_wrap path
from utils import get_main_path
#returns folder path
from utils import create_playlist_folder

# # Zadania:
# # Składa komendę spotdl na podstawie settings
# # Obsługuje błędy
# # Zwraca sukces / fail

def 
# wywołanie spotdl z opcjami z settings
def download(get_input(), folder_name, settings):
    main_path = get_main_path()
    folder_path = create_playlist_folder()

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    ensure_logs_directory()  # Upewnij się, że folder logs istnieje

#     command = [
#         "spotdl", "download", url,
#         "--skip-album-art",
#         "--print-errors",
#         "--save-errors", os.path.join(main_path, "spotdl", "logs", "errors.txt"),
#         "--overwrite", "skip",
#         "--threads", "8",
#         "--bitrate", settings["bitrate"],
#         "--output", os.path.join(folder_path, "{artist} - {title}.mp3"),
#         "--format", settings["format"]
#     ]

#     try:
#         subprocess.run(command, check=True)
#         return True
#     except subprocess.CalledProcessError as e:
#         print(f"Nie udało się pobrać: {url}, błąd: {e}")
#         return False

