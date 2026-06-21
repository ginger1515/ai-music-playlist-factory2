import os
import json
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTPUT_DIR = os.path.join(ROOT, "output", "releases", str(date.today()))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# PLAYLIST (EDIT QUI)
# =========================
PLAYLISTS = [
    {"name": "Workout Energy", "theme": "high energy gym music"},
    {"name": "Chill Vibes", "theme": "lofi chill relaxing"},
    {"name": "Focus Mode", "theme": "deep focus instrumental"},
]

tracks = []

# =========================
# GENERAZIONE TRACK
# =========================
for i, pl in enumerate(PLAYLISTS, start=1):

    title = f"Track_{i}_{pl['name'].replace(' ', '_')}"
    folder = os.path.join(OUTPUT_DIR, title)
    os.makedirs(folder, exist_ok=True)

    prompt = f"Create a {pl['theme']} song for playlist {pl['name']}"

    with open(os.path.join(folder, "audio_suno_prompt.txt"), "w", encoding="utf-8") as f:
        f.write(prompt)

    with open(os.path.join(folder, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(pl, f, indent=2)

    with open(os.path.join(folder, "cover.png"), "wb") as f:
        f.write(b"")

    tracks.append({
        "title": title,
        "theme": pl["theme"],
        "playlist": pl["name"]
    })

# =========================
# MANIFEST (CRITICO)
# =========================
manifest = {
    "date": str(date.today()),
    "tracks": tracks
}

manifest_path = os.path.join(OUTPUT_DIR, "release_manifest.json")

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print("OK GENERATION COMPLETE")
print("Manifest:", manifest_path)
