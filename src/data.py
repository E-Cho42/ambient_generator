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
    ["G#maj", ["g#", "c", "d#"]]
]

progressions = [
    # Existing ones
    [ ["Cmaj",["c","e","g"]], ["Gmaj",["g","b","d"]], ["Amin",["a","c","e"]], ["Fmaj",["f","a","c"]] ],  # I-V-vi-IV
    [ ["Amin",["a","c","e"]], ["Fmaj",["f","a","c"]], ["Cmaj",["c","e","g"]], ["Gmaj",["g","b","d"]] ],  # vi-IV-I-V
    [ ["Dmin",["d","f","a"]], ["Gmin",["g","a#","d"]], ["A#maj",["a#","d","f"]], ["Cmaj",["c","e","g"]] ], # modal
    [ ["Cmaj",["c","e","g"]], ["Fmaj",["f","a","c"]], ["Gmaj",["g","b","d"]], ["Cmaj",["c","e","g"]] ],  # I-IV-V-I
    [ ["Emin",["e","g","b"]], ["Cmaj",["c","e","g"]], ["Gmaj",["g","b","d"]], ["Dmaj",["d","f#","a"]] ],  # ambient

    # --- New Progressions ---

    # Pop / Rock
    [ ["Cmaj",["c","e","g"]], ["Amin",["a","c","e"]], ["Fmaj",["f","a","c"]], ["Gmaj",["g","b","d"]] ],  # I-vi-IV-V (50s)
    [ ["Fmaj",["f","a","c"]], ["Gmaj",["g","b","d"]], ["Emin",["e","g","b"]], ["Amin",["a","c","e"]] ],  # IV-V-iii-vi
    [ ["Dmaj",["d","f#","a"]], ["Amaj",["a","c#","e"]], ["Bm",["b","d","f#"]], ["Gmaj",["g","b","d"]] ],  # I-V-vi-IV (D major)
    [ ["Gmaj",["g","b","d"]], ["Dmaj",["d","f#","a"]], ["Emin",["e","g","b"]], ["Cmaj",["c","e","g"]] ],  # I-V-vi-IV (G)

    # Lo-fi / Chill
    [ ["Cmaj7",["c","e","g","b"]], ["Emin7",["e","g","b","d"]], ["Amin7",["a","c","e","g"]], ["Gmaj7",["g","b","d","f#"]] ],
    [ ["Amin7",["a","c","e","g"]], ["D9",["d","f#","a","c","e"]], ["Gmaj7",["g","b","d","f#"]], ["Cmaj7",["c","e","g","b"]] ],  # ii-V-I-vi
    [ ["Fmaj7",["f","a","c","e"]], ["Emin7",["e","g","b","d"]], ["Amin7",["a","c","e","g"]], ["G13",["g","b","d","f#","a","c","e"]] ],

    # Minor key
    [ ["Amin",["a","c","e"]], ["Gmaj",["g","b","d"]], ["Fmaj",["f","a","c"]], ["Emaj",["e","g#","b"]] ],  # i-VII-VI-V (harmonic minor)
    [ ["Emin",["e","g","b"]], ["Cmaj",["c","e","g"]], ["Dmaj",["d","f#","a"]], ["B7",["b","d#","f#","a"]] ], # i-VI-VII-V7
    [ ["Dmin",["d","f","a"]], ["Bbmaj",["a#","d","f"]], ["Cmaj",["c","e","g"]], ["Amaj",["a","c#","e"]] ], # i-bVI-bVII-V

    # Jazz
    [ ["Dmin7",["d","f","a","c"]], ["G7",["g","b","d","f"]], ["Cmaj7",["c","e","g","b"]], ["A7",["a","c#","e","g"]] ], # ii-V-I-VI
    [ ["Cmaj7",["c","e","g","b"]], ["E7",["e","g#","b","d"]], ["Amin7",["a","c","e","g"]], ["D7",["d","f#","a","c"]] ], # I-III-vi-II
    [ ["Fmaj7",["f","a","c","e"]], ["G13",["g","b","d","f#","a","c","e"]], ["Em7b5",["e","g","a#","d"]], ["A7",["a","c#","e","g"]] ], # jazz cycle

    # Blues
    [ ["C7",["c","e","g","a#"]], ["F7",["f","a","c","d#"]], ["C7",["c","e","g","a#"]], ["G7",["g","b","d","f"]] ],   # 12-bar simplified
    [ ["E7",["e","g#","b","d"]], ["A7",["a","c#","e","g"]], ["B7",["b","d#","f#","a"]] , ["E7",["e","g#","b","d"]] ],

    # Cinematic / Ambient
    [ ["Dmaj",["d","f#","a"]], ["Amaj",["a","c#","e"]], ["Emaj",["e","g#","b"]], ["F#min",["f#","a","c#"]] ],
    [ ["Cadd9",["c","e","g","d"]], ["Gsus4",["g","c","d"]], ["Fmaj7",["f","a","c","e"]], ["Am7",["a","c","e","g"]] ],
    [ ["Emin",["e","g","b"]], ["Gmaj",["g","b","d"]], ["Amaj",["a","c#","e"]], ["Dmaj",["d","f#","a"]] ],

    # EDM / House
    [ ["Fmaj",["f","a","c"]], ["Gmaj",["g","b","d"]], ["Amin",["a","c","e"]], ["Em",["e","g","b"]] ],   # IV-V-vi-iii
    [ ["Dmin",["d","f","a"]], ["Amin",["a","c","e"]], ["Fmaj",["f","a","c"]], ["Gmaj",["g","b","d"]] ],  # ii-vi-IV-V
    [ ["Amin",["a","c","e"]], ["Cmaj",["c","e","g"]], ["Gmaj",["g","b","d"]], ["Fmaj",["f","a","c"]] ],  # vi-I-V-IV
]
