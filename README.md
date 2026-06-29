# 🎵 Ambient Music Generator

A procedural ambient music generator built in Python. Given a seed, it synthesizes a multi-track `.wav` file from chord progressions, bass lines, rhythm pulses, and melodic runs — then plays it back through a live GUI with a real-time waveform visualizer.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![License](https://img.shields.io/badge/license-MIT-green)

---

## How It Works

The generator builds four simultaneous tracks around a randomly selected chord progression:

- **Pad** — sustained chord tones at octave 3, with a slow swell attack
- **Bass** — alternates between the root and fifth of each chord at octave 2
- **Rhythm** — square-wave pulse pattern with alternating accent on every other eighth note
- **Melody** — randomly walks the chord scale at octaves 4 or 5, with varying note durations

The seed (a 10-digit integer) determines which progression is chosen and controls all random decisions, so the same seed always produces the same track.

---

## Features

- 10 built-in chord progressions across Classic Ambient, Lo-fi Jazz, Smooth Jazz, Cinematic, and Dark/Moody styles
- 4 waveform types: Sine, Sawtooth, Triangle, Square
- Adjustable volume and tempo (40–180 BPM)
- Swell toggle for slow vs. sharp pad attack
- Live animated waveform visualizer that responds to volume and tempo sliders
- Seed-based generation — reproducible tracks
- Cross-platform WAV playback (macOS `afplay`, Windows `SoundPlayer`, Linux `aplay`)

---

## Project Structure

```
ambient_generator/
├── src/
│   ├── main.py          # GUI entry point (CustomTkinter)
│   ├── generator.py     # Music synthesis logic
│   ├── data.py          # Chord definitions and progressions
│   └── test.py          # Basic generation tests
├── sounds/              # Sample pre-generated WAV files
├── requirements.txt
└── README.md
```

---

## Installation

```bash
git clone https://github.com/E-Cho42/ambient_generator
cd ambient_generator
pip install -r requirements.txt
```

**Requirements:**
```
tones
customtkinter
numpy
```

> `tk`, `random`, and `math` are part of the Python standard library and don't need to be installed separately.

---

## Usage

**Run the GUI:**
```bash
python src/main.py
```

**Use the generator directly in Python:**
```python
from src.generator import generate
from tones import SINE_WAVE

result = generate(
    volume=0.7,
    tempo=90,
    swell=True,
    seed="1234567890",
    wave_type=SINE_WAVE
)
# Outputs audio.wav in the current directory
print(result)
# {'progression': ['Cmaj', 'Gmaj', 'Amin', 'Fmaj'], 'status': "Success! 'audio.wav' generated.", 'seed_used': '1234567890'}
```

---

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `volume` | float | `0.7` | Output amplitude (0.0 – 1.0) |
| `tempo` | int | `90` | Beats per minute (min: 1) |
| `swell` | bool | `True` | Slow pad attack (2s) vs. sharp (0.5s) |
| `seed` | str | `"1234567890"` | 10-digit seed for reproducible output |
| `wave_type` | const | `SINE_WAVE` | Waveform: `SINE_WAVE`, `SAWTOOTH_WAVE`, `TRIANGLE_WAVE`, `SQUARE_WAVE` |
| `reverb` | bool | `False` | Reserved for future use |
| `delay` | bool | `False` | Reserved for future use |

---

## Chord Progressions

Progressions are defined in `data.py` and selected by `int(seed[-2:]) % len(progressions)`.

| Style | Example Progression |
|-------|-------------------|
| Classic Ambient | Cmaj → Gmaj → Amin → Fmaj |
| Lo-fi Jazz | Cmaj7 → Em7 → Am7 → Gmaj7 |
| Smooth Jazz | Dm7 → G7 → Cmaj7 → A7 |
| Cinematic | Dmaj → Amaj → Emaj → F#min |
| Dark / Moody | Amin → Gmaj → Fmaj → Emaj |

New progressions can be added to the `progressions` list in `data.py` using the format:
```python
[["ChordName", ["note1", "note2", "note3"]], ...]
```

---

## Adding Custom Progressions

Open `data.py` and append to the `progressions` list:

```python
progressions.append([
    ["Dmaj7", ["d", "f#", "a", "c#"]],
    ["Bmin7", ["b", "d", "f#", "a"]],
    ["Gmaj7", ["g", "b", "d", "f#"]],
    ["A7",    ["a", "c#", "e", "g"]],
])
```

Notes must be lowercase letters (`a`–`g`). Sharps are written with `#` (e.g. `f#`, `c#`). The `chord_scale` function fills in diatonic passing tones automatically for the melody track.
