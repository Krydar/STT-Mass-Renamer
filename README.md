# STT-Mass-Renamer
Mass audio file renamer that uses AI speech recognition to determine filename.

Created for the Marathon community.

# Dependancies

- Python 3.9 or newer.

# Installation

**Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate 
# Torch in requirements.txt might fail so we should fetch it directly beforehand.
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128 
pip install -r requirements.txt
```

# Usage
place `massRenamer.py` into the folder of your choice and run the Python script. 
