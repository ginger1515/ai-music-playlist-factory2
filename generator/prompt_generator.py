import json
import os
from datetime import datetime

# ROOT DEL PROGETTO (fix definitivo GitHub Actions)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# CARICA CONFIG
with open(os.path.join(ROOT_DIR, "generator", "config.json"), "r") as f:
    config = json.load(f)

with open(os.path.join(ROOT_DIR, "generator", "playlists.json"), "r") as f:
    playlists_data = json.load(f)

prompts_per_playlist = config["prompts_per_playlist"]

# OUTPUT FOLDER
today = datetime.now().strftime("%Y-%m-%d")
output_folder = os.path.join(ROOT_DIR, "output", "suno", today)
os.makedirs(output_folder, exist_ok=True)

# GENERAZIONE
for playlist in playlists_data["playlists"]:

    playlist_name = playlist["name"]

    safe_name = (
        playlist_name
        .replace(" ", "_")
        .replace("&", "and")
        .replace("/", "_")
    )

    for i in range(1, prompts_per_playlist + 1):

        title = f"{safe_name}_{i:02d}"

        prompt = f"""
TITLE:
{title}

PLAYLIST:
{playlist['name']}

SUNO PROMPT:

Create a {playlist['genre']} track.

Mood:
{playlist['mood']}

BPM:
{playlist['bpm']}

Keywords:
{playlist['keywords']}

Sound Design:
{', '.join(playlist['sound_profile'])}

Rules:
{', '.join(config['rules'])}

Spotify Context:
Designed for background listening in playlist: {playlist['name']}

IMPORTANT:
- no vocals
- no lyrics
- loopable structure
- non-intrusive sound
"""

        file_path = os.path.join(output_folder, f"{title}.txt")

        with open(file_path, "w") as file:
            file.write(prompt)

print("✔ Generation completed successfully")
