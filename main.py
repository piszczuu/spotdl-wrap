#importy
import subprocess

from src.utils import create_playlist_folder, clear_name, clear_screen, colored_text
from src.ascii_art import ascii_art_name

# główny program
def main():
    # logika główna
    try:

        # ---------------------------------
        clear_screen()
        colored_text("\n  Welcome to the Playlist Downloader!", color="green", style="bright") 
        colored_text(ascii_art_name(), color="green", style="bright")
        print()
        job_choice = input("What would you like to do?\n" \
        "   1. Download a playlist\n> ").strip()
        if job_choice not in ("1", "2"):
            print("Invalid choice.")
        else:
            pass

        # ---------------------------------

    except KeyboardInterrupt:
        print("\nProgram interrupted. Cleaning up...")

if __name__ == "__main__":
    while True:
        main()
        try:
            retry = input("Try again? Yes(y) / No(q):\n> ").strip().lower()
            if retry not in ("y", "yes"):
                print(" Exiting.")
                break
        except KeyboardInterrupt:
            print("\nExiting...")
            break
