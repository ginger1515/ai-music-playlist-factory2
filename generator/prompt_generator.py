import os
import json
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATE = str(date.today())
OUTPUT_DIR = os.path.join(ROOT, "output", "releases", DATE)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# PLAYLIST SOURCE OF TRUTH
# =========================
PLAYLISTS = [
    {"name": "Workout Energy", "theme": "high energy gym music"},
    {"name": "Chill Vibes", "theme": "lofi chill relaxing"},
    {"name": "Focus Mode", "theme": "deep ambient focus music"},
]

tracks = []

# =========================
# GENERAZIONE TRACK UNIFICATA
# =========================
for i, pl in enumerate(PLAYLISTS, start=1):

    title = f"Track_{i}_{pl['name'].replace(' ', '_')}"
    folder = os.path.join(OUTPUT_DIR, title)
    os.makedirs(folder, exist_ok=True)

    # 🔥 SINGLE SOURCE PROMPT (Suno)
    prompt = f"""
Create a professional music track.

Style: {pl['theme']}
Playlist: {pl['name']}

Make it high quality, streaming-ready, emotional, and consistent.
"""

    prompt_path = os.path.join(folder, "suno_prompt.txt")
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(prompt.strip())

    # metadata unico
    metadata = {
        "title": title,
        "playlist": pl["name"],
        "theme": pl["theme"],
        "suno_prompt_file": "suno_prompt.txt"
    }

    with open(os.path.join(folder, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    # =========================
    # COVER (placeholder PRO)
    # =========================
    cover_prompt = f"album cover, {pl['theme']}, cinematic, modern music branding"

    with open(os.path.join(folder, "cover_prompt.txt"), "w", encoding="utf-8") as f:
        f.write(cover_prompt)

    tracks.append(metadata)

# =========================
# MANIFEST (UNICA FONTE VERITÀ)
# =========================
manifest = {
    "date": DATE,
    "tracks": tracks
}

manifest_path = os.path.join(OUTPUT_DIR, "release_manifest.json")

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print("✔ PRO PIPELINE COMPLETE")
print("✔ Manifest:", manifest_path)
