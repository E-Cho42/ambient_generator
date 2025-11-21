from tones.mixer import Mixer
import random

# Setup mixer
mixer = Mixer(44100, 0.4)
mixer.create_track(0)

# Scale notes (C minor pentatonic)
scale = ["c", "d#", "f", "g", "a#"]

# Generate random melody
for _ in range(16):
    note = random.choice(scale)
    duration = 0.25  # quarter note
    mixer.add_note(0, note =note, duration= duration)

mixer.write_wav("melody_simple.wav")