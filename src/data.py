# data.py

# A master list of chords for reference if needed
chords_list = [
    ["Amaj", ["a", "c#", "e"]],
    ["Amin", ["a", "c", "e"]],
    ["Bmaj", ["b", "d#", "f#"]],
    ["Bmin", ["b", "d", "f#"]],
    ["Cmaj", ["c", "e", "g"]],
    ["Cmin", ["c", "d#", "g"]],
    ["Dmaj", ["d", "f#", "a"]],
    ["Dmin", ["d", "f", "a"]],
    ["Emaj", ["e", "g#", "b"]],
    ["Emin", ["e", "g", "b"]],
    ["Fmaj", ["f", "a", "c"]],
    ["Fmin", ["f", "g#", "c"]],
    ["Gmaj", ["g", "b", "d"]],
    ["Gmin", ["g", "a#", "d"]],
    ["A#maj", ["a#", "d", "f"]],
    ["C#maj", ["c#", "f", "g#"]],
    ["D#maj", ["d#", "g", "a#"]],
    ["F#maj", ["f#", "a#", "c#"]],
    ["G#maj", ["g#", "c", "d#"]],
    # 7th and Extended Chords
    ["Cmaj7", ["c", "e", "g", "b"]],
    ["Amin7", ["a", "c", "e", "g"]],
    ["Emin7", ["e", "g", "b", "d"]],
    ["Gmaj7", ["g", "b", "d", "f#"]],
    ["Dmin7", ["d", "f", "a", "c"]],
    ["G7", ["g", "b", "d", "f"]],
    ["A7", ["a", "c#", "e", "g"]],
    ["E7", ["e", "g#", "b", "d"]],
    ["D7", ["d", "f#", "a", "c"]],
    ["Fmaj7", ["f", "a", "c", "e"]],
    ["D9", ["d", "f#", "a", "c", "e"]],
    ["G13", ["g", "b", "d", "f#", "a", "c", "e"]],
    ["Em7b5", ["e", "g", "a#", "d"]],
    ["C7", ["c", "e", "g", "a#"]],
    ["F7", ["f", "a", "c", "d#"]],
    ["B7", ["b", "d#", "f#", "a"]],
    ["Cadd9", ["c", "e", "g", "d"]],
    ["Gsus4", ["g", "c", "d"]],
    ["Am7", ["a", "c", "e", "g"]]
]

progressions = [
    # --- Classic Ambient / Pop ---
    [["Cmaj", ["c", "e", "g"]], ["Gmaj", ["g", "b", "d"]], ["Amin", ["a", "c", "e"]], ["Fmaj", ["f", "a", "c"]]],
    [["Emin", ["e", "g", "b"]], ["Cmaj", ["c", "e", "g"]], ["Gmaj", ["g", "b", "d"]], ["Dmaj", ["d", "f#", "a"]]],
    
    # --- Lo-fi / Chill Jazz ---
    [["Cmaj7", ["c", "e", "g", "b"]], ["Emin7", ["e", "g", "b", "d"]], ["Amin7", ["a", "c", "e", "g"]], ["Gmaj7", ["g", "b", "d", "f#"]]],
    [["Fmaj7", ["f", "a", "c", "e"]], ["Emin7", ["e", "g", "b", "d"]], ["Amin7", ["a", "c", "e", "g"]], ["G13", ["g", "b", "d", "f#", "a", "c", "e"]]],
    
    # --- Smooth Jazz Cycle ---
    [["Dmin7", ["d", "f", "a", "c"]], ["G7", ["g", "b", "d", "f"]], ["Cmaj7", ["c", "e", "g", "b"]], ["A7", ["a", "c#", "e", "g"]]],
    [["Fmaj7", ["f", "a", "c", "e"]], ["G13", ["g", "b", "d", "f#", "a", "c", "e"]], ["Em7b5", ["e", "g", "a#", "d"]], ["A7", ["a", "c#", "e", "g"]]],
    
    # --- Cinematic / Beautiful ---
    [["Dmaj", ["d", "f#", "a"]], ["Amaj", ["a", "c#", "e"]], ["Emaj", ["e", "g#", "b"]], ["F#min", ["f#", "a", "c#"]]],
    [["Cadd9", ["c", "e", "g", "d"]], ["Gsus4", ["g", "c", "d"]], ["Fmaj7", ["f", "a", "c", "e"]], ["Am7", ["a", "c", "e", "g"]]],
    
    # --- Dark / Moody ---
    [["Amin", ["a", "c", "e"]], ["Gmaj", ["g", "b", "d"]], ["Fmaj", ["f", "a", "c"]], ["Emaj", ["e", "g#", "b"]]],
    [["Dmin", ["d", "f", "a"]], ["A#maj", ["a#", "d", "f"]], ["Cmaj", ["c", "e", "g"]], ["Amaj", ["a", "c#", "e"]]]
]