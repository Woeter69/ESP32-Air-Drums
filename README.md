# ESP32 -> MIDI -> Python Audio Player

Lightweight Python desktop app that listens for incoming MIDI messages over UDP (for example from ESP32 devices sending MIDI over Wi‑Fi), parses them, and plays corresponding sounds. Includes a minimal Tkinter UI that shows recent notes.

Features
- UDP server listening for incoming MIDI bytes
- MIDI parsing using `mido` (with a small fallback parser)
- Simple audio engine using `numpy` + `pygame` to synthesize notes
- Minimal Tkinter UI showing recent notes
- A fake MIDI UDP sender for local testing

Requirements
- Python 3.11+
- Install dependencies (recommended inside a venv):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Running
- Start the app (listens on UDP port 6000 by default):

```powershell
python run.py --host 0.0.0.0 --port 6000
```

- In another terminal you can run the test sender to send fake MIDI note_on / note_off messages to localhost:

```powershell
python send_fake_midi.py --host 127.0.0.1 --port 6000
```

Configuration
- Default UDP listen host: 0.0.0.0
- Default UDP listen port: 6000

Notes
- If `mido` is not installed or available, the project falls back to a minimal parser (supports note_on, note_off, control_change basic messages).
- The audio engine synthesizes short sine wave tones on the fly, so no sample files are required.

License: MIT
