

from pathlib import Path
import re
import yt_dlp
import requests
from urllib.parse import urlparse
    
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

# Main function that creates the playlist folder structure
def create_playlist_folder() -> str | None:
    provider = get_playlist_provider()
    if provider == 'spotify':
        playlist_name = get_spotify_playlist_name() 
    elif provider == 'youtube':
        playlist_name = get_youtube_playlist_name()
    
    if provider is None:
        return None

    if not playlist_name:  # Check if name retrieval failed
        return None
    clean_playlist_name = clear_name(playlist_name)

    folder_path = Path(get_main_path()) / 'spotdl' / 'music' / provider / clean_playlist_name
    folder_path.mkdir(parents=True, exist_ok=True)  # Create all missing directories
    return str(folder_path)

# Entry point for script execution
if __name__ == "__main__":
    if path := create_playlist_folder():
        print(f"Created folder: {path}")
    else:
        print("Failed to create folder.")