import os
import json
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTPUT_DIR = os.path.join(ROOT, "output", "releases", str(date.today()))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# CONFIG PLAYLIST (ESMPIO)
# =========================
PLAYLISTS = [
    {"name": "Workout Energy", "theme": "high energy gym music"},
    {"name": "Chill Vibes", "theme": "lofi chill relaxing"},
    {"name": "Focus Mode", "theme": "deep focus instrumental"},
]

tracks = []

# =========================
# GENERAZIONE FILE TRACK
# =========================
for i, pl in enumerate(PLAYLISTS, start=1):

    track_title = f"Track_{i}_{pl['name'].replace(' ', '_')}"

    track_folder = os.path.join(OUTPUT_DIR, track_title)
    os.makedirs(track_folder, exist_ok=True)

    prompt = f"Create a {pl['theme']} song for playlist {pl['name']}"

    with open(os.path.join(track_folder, "audio_suno_prompt.txt"), "w") as f:
        f.write(prompt)

    with open(os.path.join(track_folder, "metadata.json"), "w") as f:
        json.dump(pl, f, indent=2)

    # placeholder cover
    with open(os.path.join(track_folder, "cover.png"), "wb") as f:
        f.write(b"")

    tracks.append({
        "title": track_title,
        "theme": pl["theme"],
        "playlist": pl["name"]
    })

# =========================
# MANIFEST (QUESTO ERA IL PROBLEMA)
# =========================
manifest = {
    "date": str(date.today()),
    "tracks": tracks
}

with open(os.path.join(OUTPUT_DIR, "release_manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2)

print("OK - release generated")
