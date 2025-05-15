#importy
import subprocess
    
from src.utils import create_playlist_folder, clear_screen, colored_text, get_url, playlist_path
from src.ascii_art import ascii_art_name
# from src.downloader import download_song    
from src.settings import SPOTDL_SETTINGS, output_path_template

# główny program
def main():
    # logika główna
    try:

        # ---------------------------------

        clear_screen()
        colored_text("\n  Welcome to the Playlist Downloader!", color="green", style="bright") 
        colored_text(ascii_art_name(), color="green", style="bright")
        print()

        default_setup = input("Would you like to use the default settings?\n" \
        "   1. Yes\n"
        "   2. No\n> ").strip()
        if default_setup not in ("1", "2"):
            print("Invalid choice.")
        else:
            if default_setup == "1":
                folder = create_playlist_folder()
                SPOTDL_SETTINGS["--output"] = output_path_template.format(
                    folder=folder,
                    artist_title_format="{artist} - {title}.mp3"
                )
                url = get_url()

            else:
                print("Custom settings:")

                job_choice = input("What would you like to do?\n" \
                "   1. Download a playlist\n> ").strip()
                if job_choice not in ("1", "2"):
                    print("Invalid choice.")
                else:
                    pass            
                
                url_source_choice = input("Where would you like to import urls form?\n" \
                "   1. Paste them here\n"
                "   2. From .txt file...\n> ").strip()
                if url_source_choice not in ("1", "2"):
                    print("Invalid choice.")
                else:
                    pass
                
                platform_choice = input("What would you like to download from?\n" \
                "   1. From Spotify\n"
                "   2. From Youtube\n> ").strip()
                if platform_choice not in ("1", "2"):
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
