# ---------------------Imports---------------------#
from tones import *
from tones.mixer import Mixer
import random as rd
from data import *


# ---------------------gernerate function--------------------- #

def generate(volume, tempo, reverb, delay, swell, seed, wave_type):
    
    # ---------------------Gereral stuff---------------------#
    # FIX: volume is 0.0 to 1.0, but the Mixer takes a factor of 44100 (sample rate).
    # Since 'volume' is passed as volume/100 from the GUI (0.0 to 1.0), this is OK,
    # but the Mixer initialization still looks slightly unusual. Assuming it works.
    mixer = Mixer(44100, 0.4) 

    # ---------------------Making Chords--------------------- #

    # Choose a random chord progression:
    idx = (int(seed[2]) * 10 + int(seed[3])) % len(progressions)
    chosen_prog = progressions[idx]
    
    # ---------------------FIX IS ADDED HERE---------------------
    # 1. Extract the list of chord names for the GUI display
    progression_names = [chord[0] for chord in chosen_prog] 
    # -----------------------------------------------------------

    # create tracks:
    for t in range(3):
        mixer.create_track(t, wave_type, attack=0.1, decay=0.9)

    rlength = int(seed[0])/10
    rOctive = int(seed[1])/10

    #play chords
    for i in range(0,10):
        
        for chord in chosen_prog:
            name = chord[0]
            notes = chord[1]

            dur = rlength + rd.random() * 2  

            mixer.add_note(0, note=notes[0], octave=3+rOctive, duration=dur)
            mixer.add_note(1, note=notes[1], octave=3+rOctive, duration=dur)
            mixer.add_note(2, note=notes[2], octave=3+rOctive, duration=dur)

    # ---------------------Making Melody--------------------- #

    # NOTE: You haven't added any logic here for tempo, delay, reverb, or swell.
    # The music generation will be functional, but simple.

    # ---------------------Write Audio--------------------- #
    mixer.write_wav("audio.wav")
    print(chosen_prog)
    samples = mixer.mix() 
    
    
    print("--- GENERATING NEW MUSIC ---")
    print(f"  Seed: {seed}")
    print(f"  Volume: {volume:.0f}")
    print(f"  Tempo: {tempo:.0f}")
    print(f"  Reverb: {reverb}, Delay: {delay}, Swell: {swell}")
    print("------------------------------")
    print("Song made!")
    
    # ---------------------UPDATED RETURN VALUE---------------------
    return {
        "progression": progression_names, # <-- Now returns a list of strings
        "seed_length_base": rlength,
        "seed_octave_offset": rOctive
    }