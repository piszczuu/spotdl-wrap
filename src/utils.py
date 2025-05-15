import subprocess
import platform
import re
import yt_dlp
import requests
from pathlib import Path
from urllib.parse import urlparse
from colorama import Fore, Style, init

    
MAX_FILENAME_LENGTH = 255  # Maximum allowed filename length for most filesystems
ALLOWED_DOMAINS = {
    'spotify': ['open.spotify.com'],
    'youtube': ['youtube.com', 'www.youtube.com', 'youtu.be']
}


# Returns the root path of the project (spotdl_wrap directory)
def get_main_path() -> Path:
    return Path(__file__).parent.parent


# Handles user selection of music platform (Spotify/YouTube)
def get_playlist_provider() -> str:
    for _ in range(3):  # Maximum 3 attempts
        choice = input("Platform? Spotify(1) | YouTube(2) | Exit(q)\n> ").strip().lower()
        if choice == 'q':
            return None
        if choice in ('1', 'spotify'):
            return 'spotify'
        if choice in ('2', 'youtube'):
            return 'youtube'
        print('Invalid choice. Try again or press "q" to quit.')
    return None


#get url
def get_url():
    url = input('> ')
    return url


# Fetches Spotify playlist name from URL
def get_spotify_playlist_name() -> str | None:
    print('Spotify playlist url:')
    url = get_url().strip()
    if not validate_url(url, 'spotify'):
        print("Error: Invalid Spotify URL")
        return None
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        title_match = re.search(r'<title>(.+?)</title>', response.text)
        
        # Compact conditional logic for title extraction
        return title_match.group(1).replace(" | Spotify", "").strip() if title_match else None
    except Exception as e:
        # Detailed error logging
        print(f"Error: {e}")
        return None


# Fetches YouTube playlist name from URL using yt-dlp
def get_youtube_playlist_name() -> str | None:
    print('Youtube playlist url:')
    url = get_url().strip()
    if not validate_url(url, 'youtube'):
        print("Error: Invalid YouTube URL")
        return None
    try:
        ydl_opts = {
            "quiet": True,  # Suppress console output
            "extract_flat": True,  # Minimal data extraction
            "playlist_items": "0",  # Only fetch playlist metadata
            "socket_timeout": 3,  # Connection timeout in seconds
            "force_generic_extractor": True,  # Skip specialized parsers
            "ignoreerrors": True  # Skip errors in individual videos
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if info := ydl.extract_info(url, download=False):
                return clear_name(info.get('title'))
    except Exception as e:
        print(f"YouTube error: {type(e).__name__}")
    return None


def get_playlist_info() -> tuple[str, str] | None:
   
    provider = get_playlist_provider()
    if provider is None:
        return None

    if provider == 'spotify':
        playlist_name = get_spotify_playlist_name()
    elif provider == 'youtube':
        playlist_name = get_youtube_playlist_name()
    else:
        return None

    if playlist_name is None:
        return None

    return playlist_name, provider


#get folder path
def get_playlist_path() -> str | None:

    result = get_playlist_info()
    if result is None:
        return None
    playlist_name, provider = result
    clean_playlist_name = clear_name(playlist_name)
    main_path = get_main_path()

    playlist_path = main_path / 'spotdl' / 'music' / provider / clean_playlist_name
    return str(playlist_path)
playlist_path = get_playlist_path()

# creates the playlist folder structure
def create_playlist_folder(playlist_path) -> str | None:

    if not playlist_path:
        print("Error: Failed to get playlist path.")    
        return None
    
    playlist_path.mkdir(parents=True, exist_ok=True)  # Create directories







''' 
aby stworzyc folder potrzebuje: 
sciezke do folderu -> 
'''





# ---------------------------------------------------------------------


# Entry point for script execution
if __name__ == "__main__":
    if path := create_playlist_folder():
        print(f"Created folder: {path}")
    else:
        print("Failed to create folder.")


# print colored text with colorama
init(autoreset=True)
def colored_text(text: str, color: str = 'white', style: str = 'normal') -> None:
    
    colors = {
        "black": Fore.BLACK,
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE
    }
    styles= {
        "dim": Style.DIM,
        "normal": Style.NORMAL,
        "bright": Style.BRIGHT
    }
    
    color_code = colors.get(color.lower(), Fore.WHITE)
    style_code = styles.get(style.lower(), Style.NORMAL)

    print(style_code + color_code + text + Style.RESET_ALL)

# Clears the console screen
def clear_screen():
    try:
        if platform.system() == "Windows":
            subprocess.run("cls", shell=True)
        else:
            subprocess.run(["clear"])
    except Exception:
        print("Error clearing screen")

# Sanitizes filename by removing special characters and truncating length
def clear_name(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*\s]', '_', name.strip())
    return name[:MAX_FILENAME_LENGTH]


# Validates if URL belongs to the specified provider's allowed domains
def validate_url(url: str, provider: str) -> bool:
    try:
        domain = urlparse(url).netloc
        return any(allowed in domain for allowed in ALLOWED_DOMAINS[provider])
    except Exception:
        return False
    