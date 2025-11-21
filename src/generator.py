import customtkinter as ctk
import tkinter as tk  # For the Canvas
import numpy as np    # For wave calculations
import math           # For sine/cosine
import main as m      # Assuming main.py has the updated generate function
import random         
# The following import assumes these wave types are defined in a file named 'main.py' or 'data.py'
# For this example, we'll keep the import as is, assuming they are defined elsewhere and imported by main.py
from main import SINE_WAVE, SAWTOOTH_WAVE, TRIANGLE_WAVE, SQUARE_WAVE

# ---------------------Theme--------------------- #
class AppStyles:
    BG_COLOR = "#1a1a1a"           # Very dark gray
    SIDEBAR_COLOR = "#242424"      # Slightly lighter gray
    MAIN_FRAME_COLOR = "transparent"
    
    PRIMARY_COLOR = "#00aA66"       # A deep, modern green
    PRIMARY_HOVER_COLOR = "#00cc88" # A lighter, vibrant green
    SECONDARY_COLOR = "#333333"    # For inactive elements
    
    FG_COLOR = "#eceff4"
    INACTIVE_FG_COLOR = "#999999"  # Neutral gray
    
    FONT_FAMILY = "Helvetica"
    FONT_TITLE = (FONT_FAMILY, 32, "bold")
    FONT_H2 = (FONT_FAMILY, 18, "bold")
    FONT_LABEL = (FONT_FAMILY, 14)
    FONT_BUTTON = (FONT_FAMILY, 14, "bold")
    FONT_STATUS = (FONT_FAMILY, 12)
    FONT_AXIS_LABEL = (FONT_FAMILY, 10) 

# ---------------------Wave Presets--------------------- #
wave_presets = {
    "Sine": SINE_WAVE,
    "Sawtooth": SAWTOOTH_WAVE,
    "Triangle": TRIANGLE_WAVE,
    "Square": SQUARE_WAVE
}

# --- Visualizer Wave Functions (Simplified for GUI drawing) ---
def sine_func(x, phase):
    """Generates a pure sine wave."""
    frequency = 0.04
    return np.sin(x * frequency + phase)

def square_func(x, phase):
    """Generates a square wave approximation using numpy's sign function."""
    frequency = 0.04
    return np.sign(np.sin(x * frequency + phase))

def sawtooth_func(x, phase):
    """Generates a sawtooth wave using modulo/remainder."""
    frequency = 0.04
    scaled_x = (x * frequency + phase) / (2 * np.pi) 
    return (scaled_x - np.floor(scaled_x)) * 2 - 1

def triangle_func(x, phase):
    """Generates a triangle wave approximation."""
    frequency = 0.04
    scaled_x = x * frequency + phase
    return np.arcsin(np.sin(scaled_x)) * (2 / np.pi)

VISUALIZER_FUNCTIONS = {
    "Sine": sine_func,
    "Square": square_func,
    "Sawtooth": sawtooth_func,
    "Triangle": triangle_func
}
# -------------------------------------------------------------

# ---------------------Main Application Class--------------------- #
class AmbientMusicApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("Ambient Music Generator")
        self.geometry("900x600")
        self.configure(fg_color=AppStyles.BG_COLOR)
        self.resizable(False, False)

        # --- Variables ---
        self.volume_var = ctk.DoubleVar(value=70)
        self.tempo_var = ctk.DoubleVar(value=90)
        self.reverb_var = ctk.BooleanVar(value=False)
        self.delay_var = ctk.BooleanVar(value=False)
        self.swell_var = ctk.BooleanVar(value=True)
        self.seed_var = tk.StringVar(value=str(random.randint(1000000000, 9999999999)))
        self.last_song_data = None # Store song data here

        # --- Animation State ---
        self.phase_offset = 0.0
        self.anim_running = True

        # --- Layout Setup ---
        self.grid_columnconfigure(0, weight=0, minsize=240)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        # --- Create Widgets ---
        self._create_sidebar()
        self._create_main_frame()
        self._create_status_bar()
        
        # --- Start Animations ---
        self.after(100, self._start_animation_loop)

    # ---------------------Widget Creation Methods--------------------- #
    def _create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, fg_color=AppStyles.SIDEBAR_COLOR, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        title_label = ctk.CTkLabel(self.sidebar_frame, text="PARAMETERS", font=AppStyles.FONT_H2, text_color=AppStyles.FG_COLOR)
        title_label.pack(padx=20, pady=(20, 10), anchor="w")

        # Volume
        volume_label = ctk.CTkLabel(self.sidebar_frame, text="Volume", font=AppStyles.FONT_LABEL, text_color=AppStyles.INACTIVE_FG_COLOR)
        volume_label.pack(padx=20, pady=(10, 0), anchor="w")
        volume_slider = ctk.CTkSlider(self.sidebar_frame, from_=0, to=100, variable=self.volume_var,
                                      fg_color=AppStyles.SECONDARY_COLOR, progress_color=AppStyles.PRIMARY_COLOR,
                                      button_color=AppStyles.PRIMARY_COLOR, button_hover_color=AppStyles.PRIMARY_HOVER_COLOR)
        volume_slider.pack(padx=20, pady=(5, 20), fill="x")

        # Tempo
        tempo_label = ctk.CTkLabel(self.sidebar_frame, text="Tempo (BPM)", font=AppStyles.FONT_LABEL, text_color=AppStyles.INACTIVE_FG_COLOR)
        tempo_label.pack(padx=20, pady=(10, 0), anchor="w")
        tempo_slider = ctk.CTkSlider(self.sidebar_frame, from_=40, to=180, variable=self.tempo_var, number_of_steps=140,
                                     fg_color=AppStyles.SECONDARY_COLOR, progress_color=AppStyles.PRIMARY_COLOR,
                                     button_color=AppStyles.PRIMARY_COLOR, button_hover_color=AppStyles.PRIMARY_HOVER_COLOR)
        tempo_slider.pack(padx=20, pady=(5, 20), fill="x")

        # Effects
        fx_label = ctk.CTkLabel(self.sidebar_frame, text="EFFECTS", font=AppStyles.FONT_H2, text_color=AppStyles.FG_COLOR)
        fx_label.pack(padx=20, pady=(20, 10), anchor="w")

        reverb_switch = ctk.CTkSwitch(self.sidebar_frame, text="Reverb", variable=self.reverb_var,
                                      font=AppStyles.FONT_LABEL, progress_color=AppStyles.PRIMARY_COLOR)
        reverb_switch.pack(padx=20, pady=10, fill="x")
        delay_switch = ctk.CTkSwitch(self.sidebar_frame, text="Delay", variable=self.delay_var,
                                     font=AppStyles.FONT_LABEL, progress_color=AppStyles.PRIMARY_COLOR)
        delay_switch.pack(padx=20, pady=10, fill="x")
        swell_switch = ctk.CTkSwitch(self.sidebar_frame, text="Swell", variable=self.swell_var,
                                     font=AppStyles.FONT_LABEL, progress_color=AppStyles.PRIMARY_COLOR)
        swell_switch.pack(padx=20, pady=10, fill="x")

    def _create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=AppStyles.MAIN_FRAME_COLOR)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)

        title_label = ctk.CTkLabel(self.main_frame, text="Ambient Music", font=AppStyles.FONT_TITLE, text_color=AppStyles.FG_COLOR)
        title_label.pack(pady=(0, 10), anchor="w")

        # Wave Visualizer
        self.vis_canvas = tk.Canvas(self.main_frame, bg=AppStyles.BG_COLOR, height=120, highlightthickness=0)
        self.vis_canvas.pack(fill="x", pady=20)

        # Waveform selection
        wave_label = ctk.CTkLabel(self.main_frame, text="WAVEFORM", font=AppStyles.FONT_H2, text_color=AppStyles.FG_COLOR)
        wave_label.pack(pady=(10, 5), anchor="w")

        self.wave_preset_button = ctk.CTkSegmentedButton(self.main_frame, 
                                                         values=list(wave_presets.keys()),
                                                         font=AppStyles.FONT_LABEL,
                                                         selected_color=AppStyles.PRIMARY_COLOR,
                                                         selected_hover_color=AppStyles.PRIMARY_HOVER_COLOR,
                                                         unselected_color=AppStyles.SECONDARY_COLOR)
        self.wave_preset_button.set("Sine")  # default
        self.wave_preset_button.pack(fill="x", pady=10)
        
        # --- Seed Entry and New Button (Layout using a sub-frame) ---
        seed_control_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        seed_control_frame.pack(fill="x", pady=(0, 20))
        seed_control_frame.grid_columnconfigure(0, weight=1)
        seed_control_frame.grid_columnconfigure(1, weight=0)
        
        # Seed Label
        seed_label = ctk.CTkLabel(seed_control_frame, text="Seed: 10 Digits", font=AppStyles.FONT_LABEL, text_color=AppStyles.INACTIVE_FG_COLOR)
        seed_label.grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky="w")
        
        # Seed Entry
        seed_entry = ctk.CTkEntry(seed_control_frame, textvariable=self.seed_var, font=AppStyles.FONT_LABEL,
                                  fg_color=AppStyles.SECONDARY_COLOR, text_color=AppStyles.FG_COLOR, placeholder_text="Enter seed...")
        seed_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10))

        # New Seed Button
        self.new_seed_button = ctk.CTkButton(seed_control_frame, text="New Seed", font=AppStyles.FONT_BUTTON,
                                             command=self._generate_new_seed, fg_color=AppStyles.SECONDARY_COLOR,
                                             hover_color=AppStyles.PRIMARY_HOVER_COLOR)
        self.new_seed_button.grid(row=1, column=1, sticky="e")
        # -------------------------------------------------------------

        # Generate Button
        self.generate_button = ctk.CTkButton(self.main_frame, text="Generate Music", font=AppStyles.FONT_BUTTON,
                                             command=self._on_generate, fg_color=AppStyles.PRIMARY_COLOR,
                                             hover_color=AppStyles.PRIMARY_HOVER_COLOR, height=50, corner_radius=10)
        self.generate_button.pack(fill="x", pady=(10, 5), ipady=5)

        # --- Song Information Container ---
        self.song_info_label = ctk.CTkLabel(self.main_frame, text="LAST GENERATED SONG DETAILS", 
                                            font=AppStyles.FONT_STATUS, text_color=AppStyles.INACTIVE_FG_COLOR)
        self.song_info_label.pack(pady=(15, 5), anchor="w")
        
        self.song_info_frame = ctk.CTkFrame(self.main_frame, fg_color=AppStyles.SECONDARY_COLOR, corner_radius=8)
        self._update_song_info_display(None) # Initialize with placeholder text
        self.song_info_frame.pack(fill="x", pady=(0, 20))
        # ----------------------------------

    def _create_status_bar(self):
        self.status_bar_frame = ctk.CTkFrame(self, fg_color=AppStyles.SIDEBAR_COLOR, height=25, corner_radius=0)
        self.status_bar_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.status_label = ctk.CTkLabel(self.status_bar_frame, text="Ready.", font=AppStyles.FONT_STATUS, text_color=AppStyles.INACTIVE_FG_COLOR)
        self.status_label.pack(side="left", padx=20)

    # -------------------- Utility Method -------------------- #
    def _generate_new_seed(self):
        """Generates a new random 10-digit seed and updates the variable."""
        new_seed = str(random.randint(1000000000, 9999999999))
        self.seed_var.set(new_seed)
        self.status_label.configure(text="New seed generated.")

    # -------------------- Animation -------------------- #
    def _start_animation_loop(self):
        self.anim_running = True
        self._animate_visualizer()

    def _animate_visualizer(self):
        if not self.anim_running:
            return
            
        canvas_width = self.vis_canvas.winfo_width()
        canvas_height = self.vis_canvas.winfo_height()
        volume = self.volume_var.get() / 100
        tempo = self.tempo_var.get()
        self.vis_canvas.delete("all")
        
        # Axis parameters
        mid_y = canvas_height / 2
        axis_color = AppStyles.INACTIVE_FG_COLOR
        axis_width = 2
        
        # --- Draw Axes and Labels ---
        self.vis_canvas.create_line(0, mid_y, canvas_width, mid_y, fill=axis_color, width=axis_width)
        v_axis_x = 5
        self.vis_canvas.create_line(v_axis_x, 0, v_axis_x, canvas_height, fill=axis_color, width=axis_width)
        
        label_color = AppStyles.INACTIVE_FG_COLOR
        font = AppStyles.FONT_AXIS_LABEL
        text_offset = 2 
        
        self.vis_canvas.create_text(v_axis_x + text_offset, 5, text="+Vol", anchor="nw", 
                                    fill=label_color, font=font)
        self.vis_canvas.create_text(v_axis_x + text_offset, canvas_height - 5, text="-Vol", anchor="sw", 
                                    fill=label_color, font=font)
        self.vis_canvas.create_text(v_axis_x + text_offset, mid_y, text="0", anchor="w", 
                                    fill=label_color, font=font)
        self.vis_canvas.create_text(canvas_width - 5, mid_y - text_offset, text="Time ->", anchor="se", 
                                    fill=label_color, font=font)
        # ----------------------------
        
        amplitude = volume * (canvas_height / 2.5)
        speed = (tempo / 120) * 0.1
        self.phase_offset += speed
        
        x = np.linspace(0, canvas_width, num=canvas_width)

        # --- Dynamic Waveform Calculation (Right-to-Left Scrolling) ---
        wave_choice = self.wave_preset_button.get()
        wave_function = VISUALIZER_FUNCTIONS.get(wave_choice, sine_func)
        
        wave_data = wave_function(x, -self.phase_offset) 
        
        y = mid_y + amplitude * wave_data
        # ------------------------------------

        points = list(zip(x, y))
        self.vis_canvas.create_line(points, fill=AppStyles.PRIMARY_COLOR, width=2.5)
        self.after(33, self._animate_visualizer)

    # -------------------- Song Info Display -------------------- #

    def _update_song_info_display(self, data):
        # Clear previous content
        for widget in self.song_info_frame.winfo_children():
            widget.destroy()

        if data is None:
            placeholder = ctk.CTkLabel(self.song_info_frame, text="No song generated yet. Press 'Generate Music' to see details.", 
                                    font=AppStyles.FONT_LABEL, text_color=AppStyles.FG_COLOR)
            placeholder.pack(padx=10, pady=10, fill="x")
            return

        # Create a grid container inside the song_info_frame
        inner_frame = ctk.CTkFrame(self.song_info_frame, fg_color="transparent")
        inner_frame.pack(fill="x", expand=False, padx=10, pady=10)

        # Configure the grid to make the two columns flexible
        # Column 0 (Parameter) and Column 1 (Value) will share the width equally
        inner_frame.grid_columnconfigure(0, weight=1) 
        inner_frame.grid_columnconfigure(1, weight=1) 
        
        row_index = 0

        # Helper to create each row using .grid()
        def create_row(param, value, is_header=False):
            nonlocal row_index
            
            color = AppStyles.PRIMARY_COLOR if is_header else AppStyles.FG_COLOR
            font_style = AppStyles.FONT_H2 if is_header else AppStyles.FONT_STATUS
            
            # --- Column 0: Parameter Label (Left-aligned) ---
            ctk.CTkLabel(inner_frame, text=param, font=font_style, text_color=color, anchor="w").grid(
                row=row_index, column=0, sticky="w", pady=2, padx=(0, 10))
                
            # --- Column 1: Value Label (Right-aligned) ---
            ctk.CTkLabel(inner_frame, text=value, font=font_style, text_color=color, anchor="e").grid(
                row=row_index, column=1, sticky="e", pady=2, padx=(10, 0))
                
            row_index += 1

        # Table rows
        create_row("Parameter", "Value", is_header=True)
        
        # Add a separator line for clarity
        separator = ctk.CTkFrame(inner_frame, height=1, fg_color=AppStyles.INACTIVE_FG_COLOR)
        separator.grid(row=row_index, column=0, columnspan=2, sticky="ew", pady=(5, 5))
        row_index += 1 

        create_row("Chord Progression:", ", ".join(data.get('progression', ['N/A'])))
        create_row("Note Duration Base:", f"{data.get('seed_length_base', 'N/A')} beats")
        octave = data.get('seed_octave_offset', 'N/A')
        octave_text = f"+{octave:.1f}" if isinstance(octave, (int, float)) else "N/A"
        create_row("Octave Shift:", octave_text)
        create_row("Waveform:", self.wave_preset_button.get())
        create_row("Output File:", "audio.wav")
        
    # -------------------- Generate Music -------------------- #
    def _on_generate(self):
        seed = self.seed_var.get()
        volume = self.volume_var.get() / 100
        tempo = self.tempo_var.get()
        reverb = self.reverb_var.get()
        delay = self.delay_var.get()
        swell = self.swell_var.get()
        wave_choice = self.wave_preset_button.get()
        wave_type = wave_presets[wave_choice]

        print("--- GENERATING NEW MUSIC ---")
        print(f"  Seed: {seed}")
        print(f"  Waveform: {wave_choice}")
        print(f"  Volume: {volume:.0f}")
        print(f"  Tempo: {tempo:.0f}")
        print(f"  Reverb: {reverb}, Delay: {delay}, Swell: {swell}")
        print("------------------------------")

        self.status_label.configure(text="Generating ambient sounds... 🎵")
        self.generate_button.configure(text="Generating...", state="disabled")

        # Assume m.generate returns the dictionary of song info
        # *** THIS LINE IS THE CRITICAL DEPENDENCY ***
        try:
            self.last_song_data = m.generate(volume=volume, tempo=tempo, reverb=reverb, delay=delay, swell=swell,
                                             seed=seed, wave_type=wave_type)
        except Exception as e:
            self.status_label.configure(text=f"ERROR in main.py: {e}")
            self.last_song_data = None # Ensure it fails gracefully
            self.generate_button.configure(text="Generate Music", state="normal")
            return

        self.after(1, self._on_generate_complete)

    def _on_generate_complete(self):
        self.status_label.configure(text="Ambient music ready! ✨")
        self.generate_button.configure(text="Generate Music", state="normal")
        
        # Update the detailed information table
        self._update_song_info_display(self.last_song_data)


# -------------------- Main -------------------- #
if __name__ == "__main__":
    app = AmbientMusicApp()
    app.mainloop()