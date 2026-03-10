import customtkinter as ctk
import tkinter as tk
import numpy as np
import random
import os
import platform
import subprocess
from tones.mixer import Mixer
from tones import SINE_WAVE, SAWTOOTH_WAVE, TRIANGLE_WAVE, SQUARE_WAVE

# --------------------- BACKEND LOGIC --------------------- #

progressions = [
    [('Cmaj7', ['c', 'e', 'g', 'b']), ('Am7', ['a', 'c', 'e', 'g']), ('Fmaj7', ['f', 'a', 'c', 'e']), ('G7', ['g', 'b', 'd', 'f'])],
    [('Dm9', ['d', 'f', 'a', 'c', 'e']), ('G13', ['g', 'b', 'd', 'f', 'a', 'e']), ('Cmaj9', ['c', 'e', 'g', 'b', 'd'])],
    [('i-VI-III-VII', ['a', 'c', 'e']), ('Fmaj', ['f', 'a', 'c']), ('Cmaj', ['c', 'e', 'g']), ('Gmaj', ['g', 'b', 'd'])]
]

def chord_scale(notes):
    scale = set(notes)
    mapping = {'c': 'd', 'd': 'e', 'e': 'f', 'f': 'g', 'g': 'a', 'a': 'b', 'b': 'c'}
    for note in notes:
        if note in mapping:
            scale.add(mapping[note])
    return sorted(list(scale))

def generate_music(volume=0.7, tempo=90, reverb=False, delay=False, swell=True, seed="1234567890", wave_type=SINE_WAVE):
    tempo = max(1, tempo)
    random.seed(int(seed))
    
    mixer = Mixer(44100, amplitude=0.4 * volume)
    prog_idx = int(seed[-2:]) % len(progressions)
    chosen_prog = progressions[prog_idx]
    
    beat_dur = 60 / tempo
    measure_dur = beat_dur * 4

    mixer.create_track("pad", wave_type, attack=2.0 if swell else 0.5, decay=1.5)
    mixer.create_track("bass", SINE_WAVE, attack=0.05, decay=0.4)
    mixer.create_track("rhythm", SQUARE_WAVE, attack=0.01, decay=0.1)
    mixer.create_track("melody", wave_type, attack=0.4, decay=2.0)

    loops = 4 + random.randint(0, 2)
    for _ in range(loops):
        for _, notes in chosen_prog:
            for note in notes:
                mixer.add_note("pad", note=note, octave=3, duration=measure_dur, amplitude=0.12)
            for _ in range(4):
                mixer.add_note("bass", note=notes[0], octave=2, duration=beat_dur)
            
            r_slice = measure_dur / 8
            for i in range(8):
                sound = min(0.1, r_slice * 0.4)
                mixer.add_note("rhythm", note=notes[0], octave=2, duration=sound, amplitude=0.05 if i%2==0 else 0.08)
                mixer.add_note("rhythm", note=notes[0], octave=2, duration=max(0.01, r_slice-sound), amplitude=0)
            
            scale = chord_scale(notes)
            elapsed = 0
            while elapsed < (measure_dur - 0.02):
                m_note = random.choice(scale)
                dur = random.choice([0.5, 1.0]) * beat_dur
                if elapsed + dur > measure_dur: dur = measure_dur - elapsed
                mixer.add_note("melody", note=m_note, octave=5, duration=dur, amplitude=0.2)
                elapsed += dur

    output_path = os.path.join(os.getcwd(), "audio.wav")
    mixer.write_wav(output_path)
    return {"progression": [c[0] for c in chosen_prog], "tempo": tempo, "wave": wave_type}

# --------------------- GUI INTERFACE --------------------- #

class AppStyles:
    BG_COLOR = "#1a1a1a"           
    SIDEBAR_COLOR = "#242424"      
    MAIN_FRAME_COLOR = "transparent"
    PRIMARY_COLOR = "#00aA66"       
    PRIMARY_HOVER_COLOR = "#00cc88" 
    SECONDARY_COLOR = "#333333"    
    FG_COLOR = "#eceff4"
    INACTIVE_FG_COLOR = "#999999"  
    FONT_FAMILY = "Helvetica"
    FONT_TITLE = (FONT_FAMILY, 32, "bold")
    FONT_H2 = (FONT_FAMILY, 18, "bold")
    FONT_LABEL = (FONT_FAMILY, 14)
    FONT_BUTTON = (FONT_FAMILY, 14, "bold")
    FONT_STATUS = (FONT_FAMILY, 12)

wave_presets = {"Sine": SINE_WAVE, "Sawtooth": SAWTOOTH_WAVE, "Triangle": TRIANGLE_WAVE, "Square": SQUARE_WAVE}
VISUALIZER_FUNCTIONS = {
    "Sine": lambda x, p: np.sin(x * 0.04 + p),
    "Square": lambda x, p: np.sign(np.sin(x * 0.04 + p)),
    "Sawtooth": lambda x, p: ((x * 0.04 + p) / (2 * np.pi) % 1) * 2 - 1,
    "Triangle": lambda x, p: np.arcsin(np.sin(x * 0.04 + p)) * (2 / np.pi)
}

class AmbientMusicApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ambient Music Generator")
        self.geometry("900x800") 
        self.configure(fg_color=AppStyles.BG_COLOR)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Variables
        self.volume_var = ctk.DoubleVar(value=70)
        self.tempo_var = ctk.DoubleVar(value=90)
        self.reverb_var = ctk.BooleanVar(value=False)
        self.delay_var = ctk.BooleanVar(value=False)
        self.swell_var = ctk.BooleanVar(value=True)
        self.seed_var = tk.StringVar(value=str(random.randint(1000000000, 9999999999)))
        
        self.player_process = None 
        self.phase_offset = 0.0

        self.grid_columnconfigure(0, weight=0, minsize=240)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._create_sidebar()
        self._create_main_frame()
        self._create_status_bar()
        self.after(100, self._animate_visualizer)

    def _create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, fg_color=AppStyles.SIDEBAR_COLOR, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar_frame, text="PARAMETERS", font=AppStyles.FONT_H2, text_color=AppStyles.FG_COLOR).pack(padx=20, pady=(20, 10), anchor="w")
        
        ctk.CTkLabel(self.sidebar_frame, text="Volume", font=AppStyles.FONT_LABEL, text_color=AppStyles.INACTIVE_FG_COLOR).pack(padx=20, pady=(10, 0), anchor="w")
        ctk.CTkSlider(self.sidebar_frame, from_=0, to=100, variable=self.volume_var, progress_color=AppStyles.PRIMARY_COLOR).pack(padx=20, pady=(5, 20), fill="x")
        
        ctk.CTkLabel(self.sidebar_frame, text="Tempo (BPM)", font=AppStyles.FONT_LABEL, text_color=AppStyles.INACTIVE_FG_COLOR).pack(padx=20, pady=(10, 0), anchor="w")
        ctk.CTkSlider(self.sidebar_frame, from_=40, to=180, variable=self.tempo_var, progress_color=AppStyles.PRIMARY_COLOR).pack(padx=20, pady=(5, 20), fill="x")
        
        ctk.CTkLabel(self.sidebar_frame, text="EFFECTS", font=AppStyles.FONT_H2, text_color=AppStyles.FG_COLOR).pack(padx=20, pady=(20, 10), anchor="w")
        ctk.CTkSwitch(self.sidebar_frame, text="Reverb", variable=self.reverb_var).pack(padx=20, pady=10, anchor="w")
        ctk.CTkSwitch(self.sidebar_frame, text="Delay", variable=self.delay_var).pack(padx=20, pady=10, anchor="w")
        ctk.CTkSwitch(self.sidebar_frame, text="Swell", variable=self.swell_var).pack(padx=20, pady=10, anchor="w")

    def _create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=AppStyles.MAIN_FRAME_COLOR)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)
        
        ctk.CTkLabel(self.main_frame, text="Ambient Music", font=AppStyles.FONT_TITLE, text_color=AppStyles.FG_COLOR).pack(pady=(0, 10), anchor="w")
        
        self.vis_canvas = tk.Canvas(self.main_frame, bg=AppStyles.BG_COLOR, height=120, highlightthickness=0)
        self.vis_canvas.pack(fill="x", pady=20)
        
        ctk.CTkLabel(self.main_frame, text="WAVEFORM", font=AppStyles.FONT_H2, text_color=AppStyles.FG_COLOR).pack(pady=(10, 5), anchor="w")
        self.wave_btn = ctk.CTkSegmentedButton(self.main_frame, values=list(wave_presets.keys()))
        self.wave_btn.set("Sine")
        self.wave_btn.pack(fill="x", pady=10)

        seed_control_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        seed_control_frame.pack(fill="x", pady=(10, 10))
        seed_control_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(seed_control_frame, text="Seed: 10 Digits", font=AppStyles.FONT_LABEL, text_color=AppStyles.INACTIVE_FG_COLOR).grid(row=0, column=0, pady=(0, 5), sticky="w")
        ctk.CTkEntry(seed_control_frame, textvariable=self.seed_var, font=AppStyles.FONT_LABEL, fg_color=AppStyles.SECONDARY_COLOR).grid(row=1, column=0, sticky="ew", padx=(0, 10))
        ctk.CTkButton(seed_control_frame, text="New Seed", font=AppStyles.FONT_BUTTON, command=self._generate_new_seed, fg_color=AppStyles.SECONDARY_COLOR, width=100).grid(row=1, column=1, sticky="e")

        self.gen_btn = ctk.CTkButton(self.main_frame, text="Generate Music", font=AppStyles.FONT_BUTTON, command=self._on_generate, fg_color=AppStyles.PRIMARY_COLOR, height=50)
        self.gen_btn.pack(fill="x", pady=(5, 5))

        self.play_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.play_frame.pack(fill="x", pady=10)
        ctk.CTkButton(self.play_frame, text="▶ Play", command=self._play_music, fg_color="#2b719e", height=50).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ctk.CTkButton(self.play_frame, text="⏹ Stop", command=self._stop_music, fg_color=AppStyles.SECONDARY_COLOR, height=50).pack(side="right", expand=True, fill="x", padx=(5, 0))

        # INFO TABLE SECTION (Bottom space)
        self.info_table_frame = ctk.CTkFrame(self.main_frame, fg_color=AppStyles.SIDEBAR_COLOR, corner_radius=8)
        self.info_table_frame.pack(fill="x", pady=(20, 0))
        self.info_table_frame.pack_forget() # Hidden initially

    def _update_info_table(self, data):
        # Clear existing table content
        for widget in self.info_table_frame.winfo_children():
            widget.destroy()
        
        self.info_table_frame.grid_columnconfigure((0, 1), weight=1)
        
        details = [
            ("Current Seed", self.seed_var.get()),
            ("Tempo", f"{data['tempo']} BPM"),
            ("Waveform", self.wave_btn.get()),
            ("Progression", " → ".join(data['progression']))
        ]

        for i, (label, value) in enumerate(details):
            # Row shading
            row_bg = AppStyles.SIDEBAR_COLOR if i % 2 == 0 else AppStyles.SECONDARY_COLOR
            f = ctk.CTkFrame(self.info_table_frame, fg_color=row_bg, corner_radius=0)
            f.pack(fill="x")
            
            ctk.CTkLabel(f, text=label, font=(AppStyles.FONT_FAMILY, 12, "bold"), text_color=AppStyles.PRIMARY_COLOR, width=120, anchor="w").pack(side="left", padx=15, pady=8)
            ctk.CTkLabel(f, text=value, font=(AppStyles.FONT_FAMILY, 12), text_color=AppStyles.FG_COLOR, anchor="w").pack(side="left", padx=5, pady=8)

        self.info_table_frame.pack(fill="x", pady=(20, 0))

    def _create_status_bar(self):
        self.status_bar = ctk.CTkFrame(self, fg_color=AppStyles.SIDEBAR_COLOR, height=25, corner_radius=0)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.status_label = ctk.CTkLabel(self.status_bar, text="Ready.", font=AppStyles.FONT_STATUS, text_color=AppStyles.INACTIVE_FG_COLOR)
        self.status_label.pack(side="left", padx=20)

    def _play_music(self):
        self._stop_music()
        path = os.path.join(os.getcwd(), "audio.wav")
        if os.path.exists(path):
            sys_name = platform.system()
            if sys_name == "Darwin": self.player_process = subprocess.Popen(["afplay", path])
            elif sys_name == "Windows": self.player_process = subprocess.Popen(["powershell", f"(New-Object Media.SoundPlayer '{path}').PlaySync()"])
            else: self.player_process = subprocess.Popen(["aplay", path])
            self.status_label.configure(text="Playing track...")
        else: self.status_label.configure(text="Error: audio.wav not found.")

    def _stop_music(self):
        if self.player_process:
            self.player_process.terminate()
            self.player_process = None
            self.status_label.configure(text="Playback stopped.")

    def on_closing(self):
        self._stop_music()
        self.destroy()

    def _generate_new_seed(self):
        self.seed_var.set(str(random.randint(1000000000, 9999999999)))

    def _on_generate(self):
        self._stop_music()
        self.status_label.configure(text="Generating ambient sounds... 🎵")
        self.update_idletasks()
        try:
            res = generate_music(
                volume=self.volume_var.get()/100,
                tempo=self.tempo_var.get(),
                reverb=self.reverb_var.get(),
                delay=self.delay_var.get(),
                swell=self.swell_var.get(),
                seed=self.seed_var.get(),
                wave_type=wave_presets[self.wave_btn.get()]
            )
            self._update_info_table(res)
            self.status_label.configure(text="Generation Complete! ✨")
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}")

    def _animate_visualizer(self):
        try:
            w, h = self.vis_canvas.winfo_width(), self.vis_canvas.winfo_height()
            if w > 1:
                mid_y = h / 2
                self.vis_canvas.delete("all")
                amp = (self.volume_var.get() / 100) * (h / 3)
                self.phase_offset += (self.tempo_var.get() / 120) * 0.1
                x = np.linspace(0, w, num=w)
                func = VISUALIZER_FUNCTIONS.get(self.wave_btn.get())
                points = list(zip(x, mid_y + amp * func(x, -self.phase_offset)))
                self.vis_canvas.create_line(points, fill=AppStyles.PRIMARY_COLOR, width=2.5)
            self.after(33, self._animate_visualizer)
        except: pass

if __name__ == "__main__":
    app = AmbientMusicApp()
    app.mainloop()