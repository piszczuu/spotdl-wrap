import os
import subprocess
import sys
import time
import threading
import json
from datetime import datetime



def get_playlist_name(url):
    try:
        # Uruchamiamy spotdl z flagą 'download', aby wyciągnąć nazwę playlisty z outputu
        result = subprocess.run(
            ["spotdl", "download", url],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Szukamy w stdout frazy "Found X songs in [Nazwa Playlisty]"
        for line in result.stdout.splitlines():
            if "Found" in line and "songs" in line:
                playlist_name = line.split("in", 1)[1].strip()  # Wyciągamy nazwę playlisty
                return playlist_name

        return "Nieznana_nazwa"  # W razie, gdybyśmy nie znaleźli nazwy w outputcie
    except subprocess.CalledProcessError:
        return "Nieznana_nazwa"  # Jeśli wystąpił błąd podczas uruchamiania spotdl

def download_song(url, folder_name, settings):
    desktop_path = get_desktop_path()
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    ensure_logs_directory()  # Upewnij się, że folder logs istnieje

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

    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Nie udało się pobrać: {url}, błąd: {e}")
        return False

def log_download_history(url, success, name):
    ensure_logs_directory()  # Upewnij się, że folder logs istnieje
    history_log_path = os.path.join(get_desktop_path(), "spotdl", "logs", "download_history.txt")
    with open(history_log_path, "a", encoding="utf-8") as history_file:
        history_file.write(f"{name} | {url} | {'OK' if success else 'ERROR'}\n")

def update_stats(stats, success):
    if success:
        stats["total_downloads"] += 1
    else:
        stats["total_failures"] += 1
    stats["last_download"] = str(datetime.today().date())
    return stats

def save_stats(stats):
    stats_path = os.path.join(get_desktop_path(), "spotdl", "stats.json")
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4)

def create_session_log(folder_name, successes, failures):
    ensure_logs_directory()  # Upewnij się, że folder logs istnieje
    session_log_path = os.path.join(get_desktop_path(), "spotdl", "logs", f"session_{folder_name}.txt")
    with open(session_log_path, "w", encoding="utf-8") as session_file:
        session_file.write(f"Sesja pobierania: {folder_name}\n")
        session_file.write(f"Udało się pobrać: {len(successes)}\n")
        session_file.write(f"Nieudane pobrania: {len(failures)}\n")
        if successes:
            session_file.write("\nSukcesy:\n")
            for name in successes:
                session_file.write(f"- {name}\n")
        if failures:
            session_file.write("\nNiepowodzenia:\n")
            for failure in failures:
                session_file.write(f"- {failure['name']} | {failure['url']} | Błąd: {failure['error']}\n")

def shutdown_computer_after_timeout(timeout_seconds=300):
    print(f"\nBrak aktywności przez {timeout_seconds // 60} min — komputer zostanie wyłączony.")
    print("Aby temu zapobiec, naciśnij dowolny klawisz...")
    def wait_and_shutdown():
        try:
            time.sleep(timeout_seconds)
            print("Czas minął. Wyłączam komputer...")
            if sys.platform == "win32":
                os.system("shutdown /s /t 0")
            else:
                os.system("shutdown -h now")
        except KeyboardInterrupt:
            print("Anulowano wyłączenie.")
    t = threading.Thread(target=wait_and_shutdown)
    t.daemon = True
    t.start()
    input()  # Jeśli użytkownik coś kliknie — przerwie shutdown

if __name__ == "__main__":
    desktop_path = get_desktop_path()
    settings = load_settings()
    stats = load_stats()

    urls = []
    print("Wybierz sposób wprowadzenia linków:")
    print("1. Ręczne wpisywanie")
    print("2. Wczytaj z pliku 'urls.txt' (jeden link na linię)")
    choice = input("Twój wybór (1/2): ").strip()

    if choice == "1":
        try:
            num_links = int(input("Ile linków chcesz pobrać? "))
        except ValueError:
            print("Musisz podać liczbę całkowitą.")
            sys.exit(1)

        for i in range(num_links):
            raw_url = input(f"Podaj URL #{i + 1}: ")
            urls.append(raw_url.strip())
    elif choice == "2":
        file_path = input("Podaj ścieżkę do pliku (Enter = domyślny 'urls.txt' na pulpicie): ").strip()
        if not file_path:
            file_path = os.path.join(desktop_path, "spotdl", "urls.txt")
        if not os.path.isfile(file_path):
            print("Nie znaleziono pliku.")
            sys.exit(1)
        with open(file_path, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
    else:
        print("Nieprawidłowy wybór.")
        sys.exit(1)

    folder_name = input("Podaj nazwę folderu na pobrane pliki: ")

    successes = []
    failures = []

    for url in urls:
        name = get_playlist_name(url)
        print(f"\n>>> Pobieranie: {name} ({url})")
        success = download_song(url, folder_name, settings)
        log_download_history(url, success, name)

        if success:
            successes.append(name)
        else:
            failures.append({"name": name, "url": url, "error": "Błąd pobierania"})

    print("\n--- Podsumowanie ---")
    print(f"Udało się pobrać: {len(successes)}")
    print(f"Nieudane pobrania: {len(failures)}")

    if successes:
        print("✔ Sukcesy:")
        for name in successes:
            print(f"- {name}")
    if failures:
        print("✖ Niepowodzenia:")
        for failure in failures:
            print(f"- {failure['name']} | URL: {failure['url']} | Błąd: {failure['error']}")

    stats = update_stats(stats, success)
    save_stats(stats)
    create_session_log(folder_name, successes, failures)

    shutdown_computer_after_timeout(timeout_seconds=settings["timeout_minutes"] * 60)
