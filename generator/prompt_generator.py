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

prompts_per_playlist = config["prompts_per_playlist"]

today = datetime.now().strftime("%Y-%m-%d")

output_folder = os.path.join(ROOT_DIR, "output", "suno", today)
os.makedirs(output_folder, exist_ok=True)

track_counter = 1

for playlist in playlists_data["playlists"]:

    playlist_name = playlist["name"]

    safe_name = (
        playlist_name
        .replace(" ", "_")
        .replace("&", "and")
        .replace("/", "_")
    )

    themes = playlist.get("themes", [])

    for i in range(prompts_per_playlist):

        theme = themes[i % len(themes)]

        prefix = random.choice(branding["release_prefixes"])

        track_title = f"{prefix} {theme}"

        description = (
            f"{playlist['genre']} music designed for "
            f"{theme.lower()}."
        )

        cover_prompt = branding["cover_styles"].get(
            playlist_name,
            "minimal ambient artwork"
        )

        suno_prompt = f"""
Create a professional {playlist['genre']} instrumental track.

Theme:
{theme}

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
{playlist_name}

IMPORTANT:
- no vocals
- no lyrics
- seamless loop
- long listening friendly
- highly repeatable
- background music only
"""

        output = f"""
TRACK TITLE:
{track_title}

ARTIST:
{branding['artist_name']}

PLAYLIST:
{playlist_name}

DESCRIPTION:
{description}

COVER IDEA:
{cover_prompt}

THEME:
{theme}

SUNO PROMPT:
{suno_prompt}
"""

        file_path = os.path.join(
            output_folder,
            f"{safe_name}_{i+1:02d}.txt"
        )

        with open(file_path, "w") as file:
            file.write(output)

        track_counter += 1

print("Themed prompt generation completed successfully")
