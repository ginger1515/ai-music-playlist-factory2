import json
import os
import random
import base64
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# LOAD FILES
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

# OPTIONAL IMAGE GENERATION (SAFE MOCK IF NO API KEY)
def generate_cover_image(prompt, path):
    """
    Placeholder: saves prompt as txt if no API configured.
    Replace with Replicate/DALL·E call when ready.
    """
    with open(path.replace(".png", ".txt"), "w") as f:
        f.write("COVER PROMPT:\n" + prompt)

for playlist in playlists_data["playlists"]:

    themes = playlist.get("themes", [])

    for i in range(config["prompts_per_playlist"]):

        theme = themes[i % len(themes)]

        prefix = random.choice(branding["release_prefixes"])
        title = f"{prefix} {theme} {counter:03d}"

        folder_name = title.replace(" ", "_")
        release_path = os.path.join(base_output, folder_name)
        os.makedirs(release_path, exist_ok=True)

        # SUNO PROMPT
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

        # COVER PROMPT (AI IMAGE)
        cover_prompt = f"{config['cover_style']}, theme: {theme}, cinematic ambient artwork"

        # METADATA
        metadata = {
            "title": title,
            "artist": branding["artist_name"],
            "playlist": playlist["name"],
            "description": f"{playlist['genre']} music for {theme.lower()}"
        }

        # WRITE FILES
        with open(os.path.join(release_path, "audio_suno_prompt.txt"), "w") as f:
            f.write(suno_prompt)

        with open(os.path.join(release_path, "cover_prompt.txt"), "w") as f:
            f.write(cover_prompt)

        with open(os.path.join(release_path, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)

        with open(os.path.join(release_path, "upload_ready.txt"), "w") as f:
            f.write("READY FOR SUNO + DISTROKID UPLOAD")

        # COVER GENERATION PLACEHOLDER
        cover_path = os.path.join(release_path, "cover.png")
        generate_cover_image(cover_prompt, cover_path)

        counter += 1

print("Release system with cover pipeline completed")
