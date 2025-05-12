# # Zadania:
# # Wczytuje i zapisuje stats.json
# # Obsługuje download_history.txt
# # Liczy sukcesy / porażki
# # Tworzy log sesji

# import json, os, datetime

# # def load_stats(): ...
# # def update_stats(stats): ...
# # def log_download_history(...): 

# # def save_stats(stats): ...
# # def update_stats(stats, success): ...
# # def log_download_history(url, success, name): ...
# # def create_session_log(folder_name, successes, failures): ...



# def load_stats():
#     stats_path = os.path.join(get_desktop_path(), "spotdl", "stats.json")
#     if not os.path.exists(stats_path):
#         stats = {"total_downloads": 0, "total_failures": 0, "last_download": ""}
#         with open(stats_path, "w", encoding="utf-8") as f:
#             json.dump(stats, f, indent=4)
#         print("Utworzono plik stats.json z domyślnymi statystykami.")
#     with open(stats_path, "r", encoding="utf-8") as f:
#         return json.load(f)
