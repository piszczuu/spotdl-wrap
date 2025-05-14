from utils import get_main_path


def download_song(url, folder_name, settings):

   command = [
        "spotdl", "download", url,
        "--skip-album-art", 
        "--print-errors",
        "--save-errors", os.path.join(desktop_path, "spotdl", "logs", "errors.txt"),
        "--overwrite", "skip",
        "--threads", "8",
        "--bitrate", settings["bitrate"],
        "--output", os.path.join(folder_path, "{artist} - {title}.mp3"),
        "--format", settings["format"]
    ]

    



if __name__ == "__main__":
    print("test")
