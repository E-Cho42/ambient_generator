## How to Run (Mac)

Follow these steps to run the Ambient Generator on macOS:

### 1. Clone the repository

```bash
git clone https://github.com/E-Cho42/ambient_generator.git
cd ambient_generator
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

This creates a folder called `venv/` that isolates the Python environment for this project.

### 3. Activate the virtual environment

```bash
source venv/bin/activate
```

You should see your terminal prompt change to something like:

```
(venv) yourname@MacBook-Pro ambient_generator %
```

The `(venv)` indicates the environment is active.

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

This installs all required libraries, including `tones`.

### 5. Run the generator

```bash
python src/generator.py --duration 60 --output sounds/ambient_output.wav
```

* `--duration` specifies the length of the generated track in seconds
* `--output` specifies the output WAV file path

After running, you will find your generated track in the `sounds/` folder.

### 6. Deactivate the virtual environment (optional)

```bash
deactivate
```

This returns your terminal to the normal environment.
