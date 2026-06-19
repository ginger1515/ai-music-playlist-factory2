import json
import random
from datetime import datetime
import os

# carica configurazione
with open("generator/config.json", "r") as f:
    data = json.load(f)

def pick(items):
    return random.choice(items)

genre = pick(data["genres"])
use_case = pick(data["use_cases"])
mood = pick(data["moods"])
sound = pick(data["sound_elements"])
context = pick(data["contexts"])

title = f"{use_case} - {mood} {genre}"

prompt = f"""
Create a {genre} track designed for {use_case.lower()}.

Mood: {mood}
Atmosphere: {context}

Include sounds like: {sound}.

Rules:
- no vocals
- no lyrics
- background music for Spotify playlists
- smooth repetitive structure
"""

# crea cartella output se non esiste
os.makedirs("output/prompts", exist_ok=True)

# salva file
filename = datetime.now().strftime("%Y-%m-%d") + ".txt"
path = f"output/prompts/{filename}"

with open(path, "w") as f:
    f.write(title + "\n\n" + prompt)

print("Generated:", title)
