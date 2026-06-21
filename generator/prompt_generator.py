import json
import os
import random
import requests
import time
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# LOAD FILES
with open(os.path.join(ROOT_DIR, "generator", "config.json"), "r") as f:
    config = json.load(f)

with open(os.path.join(ROOT_DIR, "generator", "playlists.json"), "r") as f:
    playlists_data = json.load(f)

with open(os.path.join(ROOT_DIR, "generator", "branding.json"), "r") as f:
    branding = json.load(f)

REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

today = datetime.now().strftime("%Y-%m-%d")

base_output = os.path.join(ROOT_DIR, "output", "releases", today)
os.makedirs(base_output, exist_ok=True)

counter = 1


# =========================
# AI COVER GENERATION
# =========================
def generate_cover(prompt, output_path):

    if not REPLICATE_API_TOKEN:
        with open(output_path.replace(".png", ".txt"), "w") as f:
            f.write(prompt)
        return

    response = requests.post(
        "https://api.replicate.com/v1/predictions",
        headers={
            "Authorization": f"Token {REPLICATE_API_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            # Stable Diffusion XL (public model version placeholder)
            "version": "ac732126d9a8b0b7d0d6f5c7f2f7c2d1f0c9c9b8a1a0f0e1d2c3b4a5c6d7e8f9",
            "input": {
                "prompt": prompt,
                "width": 1024,
                "height": 1024,
                "num_outputs": 1
            }
        }
    )

    if response.status_code != 201:
        print("Cover API error:", response.text)
        return

    prediction = response.json()
    get_url = prediction["urls"]["get"]

    while True:
        r = requests.get(
            get_url,
            headers={"Authorization": f"Token {REPLICATE_API_TOKEN}"}
        )
        data = r.json()

        if data["status"] == "succeeded":
            image_url = data["output"][0]
            img_data = requests.get(image_url).content

            with open(output_path, "wb") as f:
                f.write(img_data)
            break

        elif data["status"] == "failed":
            print("Cover generation failed")
            break

        time.sleep(2)


# =========================
# MAIN LOOP
# =========================
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
Create a {playlist['genre']} instrumental track.

Theme: {theme}
Mood: {playlist['mood']}
BPM: {playlist['bpm']}

Sound Design:
{', '.join(playlist['sound_profile'])}

Rules:
{', '.join(config['rules'])}

No vocals, no lyrics, seamless loop, background music only.
"""

        # COVER PROMPT
        cover_prompt = f"""
minimal cinematic ambient artwork,
theme: {theme},
style: {config['cover_style']},
abstract geometry, soft lighting, high detail, Spotify cover aesthetic
"""

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
            f.write("READY FOR SUNO + SPOTIFY RELEASE PIPELINE")

        # GENERATE COVER IMAGE
        cover_path = os.path.join(release_path, "cover.png")
        generate_cover(cover_prompt, cover_path)

        counter += 1

print("FULL RELEASE PIPELINE COMPLETED")
