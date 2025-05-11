# import subprocess, os, json
# from utils import get_default_path
# # Zadania:
# # Składa komendę spotdl na podstawie settings
# # Wywołuje subprocess.run(...)
# # Obsługuje błędy
# # Zwraca sukces / fail


# # wywołanie spotdl z opcjami z settings
# def download(url, folder_name, settings):
#     default_path = get_default_path()
#     music_path = os.path.join(desktop_path, "spotdl", "music")
#     folder_path = os.path.join(music_path, folder_name)

#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)

#     ensure_logs_directory()  # Upewnij się, że folder logs istnieje

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

