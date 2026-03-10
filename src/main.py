from tones.mixer import Mixer
from tones import SINE_WAVE, SAWTOOTH_WAVE, TRIANGLE_WAVE, SQUARE_WAVE
import random

try:
    from data import progressions
except ImportError:
    progressions = [[('Cmaj', ['c', 'e', 'g']), ('Gmaj', ['g', 'b', 'd'])]]

def chord_scale(notes):
    scale = set(notes)
    mapping = {'c': 'd', 'd': 'e', 'e': 'f', 'f': 'g', 'g': 'a', 'a': 'b', 'b': 'c'}
    for note in notes:
        if note in mapping:
            scale.add(mapping[note])
    return sorted(list(scale))

def generate(volume=0.7, tempo=90, reverb=False, delay=False, swell=True, seed="1234567890", wave_type=SINE_WAVE):
    # --- Safety Checks ---
    if not progressions:
        return {"error": "Progressions list is empty."}
    
    # Ensure tempo is at least 1 BPM to avoid division by zero
    tempo = max(1, tempo)
    random.seed(int(seed))
    
    mixer = Mixer(44100, amplitude=0.5 * volume)

    prog_idx = int(seed[-2:]) % len(progressions)
    chosen_prog = progressions[prog_idx]
    progression_names = [chord[0] for chord in chosen_prog]

    beat_dur = 60 / tempo
    measure_dur = beat_dur * 4

    mixer.create_track("pad", wave_type, attack=2.0 if swell else 0.5, decay=1.5)
    mixer.create_track("bass", SINE_WAVE, attack=0.05, decay=0.4)
    mixer.create_track("rhythm", SQUARE_WAVE, attack=0.01, decay=0.1)
    mixer.create_track("melody", wave_type, attack=0.4, decay=2.0)

    loops = 4 + random.randint(0, 2)
    
    for _ in range(loops):
        for _, notes in chosen_prog:
            if not notes: continue
            
            root = notes[0]
            fifth = notes[2] if len(notes) > 2 else notes[0]

            # --- PAD ---
            for note in notes:
                amp = random.uniform(0.1, 0.15)
                mixer.add_note("pad", note=note, octave=3, duration=measure_dur, amplitude=amp)

            # --- BASS ---
            for _ in range(4):
                b_note = random.choice([root, fifth])
                mixer.add_note("bass", note=b_note, octave=2, duration=beat_dur)

            # --- RHYTHM ---
            rhythm_slice = measure_dur / 8
            for i in range(8):
                r_note = root
                amp = 0.05 + 0.05*(i % 2)
                # Ensure the sound duration isn't longer than the slice itself
                sound_dur = min(0.1, rhythm_slice * 0.5) 
                silence_dur = max(0.01, rhythm_slice - sound_dur)
                
                mixer.add_note("rhythm", note=r_note, octave=2, duration=sound_dur, amplitude=amp)
                mixer.add_note("rhythm", note=r_note, octave=2, duration=silence_dur, amplitude=0)

            # --- MELODY ---
            scale = chord_scale(notes)
            if not scale: scale = notes # Fallback
            
            melody_oct = random.choice([4, 5])
            elapsed = 0
            while elapsed < (measure_dur - 0.01): # Small buffer for float precision
                m_note = random.choice(scale)
                dur = random.choice([0.25, 0.5, 1.0]) * beat_dur
                
                if elapsed + dur > measure_dur:
                    dur = measure_dur - elapsed
                
                # Prevent micro-durations that cause clicks or errors
                if dur > 0.02:
                    mixer.add_note("melody", note=m_note, octave=melody_oct, duration=dur, amplitude=random.uniform(0.2, 0.3))
                
                elapsed += dur

    mixer.write_wav("audio.wav")
    
    return {
        "progression": progression_names,
        "status": "Success! 'audio.wav' generated.",
        "seed_used": seed
    }