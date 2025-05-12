# Zaimportuje wszystkie moduły z tools
from src.utils import create_playlist_folder, clear_name

# główny program
def main():
    # logika główna
    print("test")

# wykonanie programu jeśli jest jako program a nie import

if __name__ == "__main__":
    while True:
        main()

        retry = input("\n🔁 Try again? Yes(y) / No(q):\n> ").strip().lower()
        if retry not in ("y", "yes"):
            print("👋 Exiting.")
            break
