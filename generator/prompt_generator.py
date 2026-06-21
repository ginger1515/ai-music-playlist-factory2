import json
import os
import random
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT_DIR, "generator", "config.json"), "r") as f:
    config = json.load(f)

with open(os.path.join(ROOT_DIR, "generator", "playlists.json"), "r") as f:
    playlists_data = json.load(f)

with open(os.path.join(ROOT_DIR, "generator", "branding.json"), "r") as f:
    branding = json.load(f)

today = datetime.now().strftime("%Y-%m-%d")

base_output = os.path.join(ROOT_DIR, "output", "releases", today)
os.makedirs(base_output, exist_ok=True)

counter = 1

for playlist in playlists_data["playlists"]:

    themes = playlist.get("themes", [])

    for i in range(config["prompts_per_playlist"]):

        theme = themes[i % len(themes)]

        prefix = random.choice(branding["release_prefixes"])
        title = f"{prefix} {theme} {counter:03d}"

        folder_name = title.replace(" ", "_")
        release_path = os.path.join(base_output, folder_name)
        os.makedirs(release_path, exist_ok=True)

        cover_prompt = f"{config['cover_style']}, theme: {theme}, mood: {playlist['mood']}"

        suno_prompt = f"""
Create a {playlist['genre']} track.

Theme: {theme}
Mood: {playlist['mood']}
BPM: {playlist['bpm']}

Sound:
{', '.join(playlist['sound_profile'])}

Rules:
{', '.join(config['rules'])}

No vocals, no lyrics, seamless loop.
"""

        metadata = {
            "title": title,
            "artist": branding["artist_name"],
            "playlist": playlist["name"],
            "description": f"{playlist['genre']} music for {theme.lower()}"
        }

        # write files
        open(os.path.join(release_path, "audio_suno_prompt.txt"), "w").write(suno_prompt)
        open(os.path.join(release_path, "cover_prompt.txt"), "w").write(cover_prompt)
        open(os.path.join(release_path, "metadata.txt"), "w").write(str(metadata))
        open(os.path.join(release_path, "spotify_title.txt"), "w").write(title)
        open(os.path.join(release_path, "artist.txt"), "w").write(branding["artist_name"])

        counter += 1

print("Release packs generated successfully")
