import json
import os
from datetime import datetime

# BASE DIRECTORY (fix per GitHub Actions)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# LOAD CONFIG
with open(os.path.join(BASE_DIR, "config.json"), "r") as f:
    config = json.load(f)

with open(os.path.join(BASE_DIR, "playlists.json"), "r") as f:
    playlists_data = json.load(f)

prompts_per_playlist = config["prompts_per_playlist"]

# OUTPUT FOLDER
today = datetime.now().strftime("%Y-%m-%d")
output_folder = os.path.join("output", "suno", today)
os.makedirs(output_folder, exist_ok=True)

# GENERATION LOOP
for playlist in playlists_data["playlists"]:

    playlist_name = playlist["name"]

    # safe filename
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

Designed for Spotify playlist:
{playlist['name']}

IMPORTANT:
- no vocals
- no lyrics
- loopable structure
- background music for focus and relaxation
"""

        file_path = os.path.join(output_folder, f"{title}.txt")

        with open(file_path, "w") as file:
            file.write(prompt)

print("Generation completed successfully")
