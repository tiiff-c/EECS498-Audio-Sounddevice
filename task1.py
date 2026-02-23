### Task 1: Test Microphone and Speakers (20\%)

# Write a Python script ```task1.py``` to:

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write 

# - Record 5 seconds of audio using the laptop’s microphone at a sampling rate of 48 kHz (mono channel).
duration = 5          # seconds
fs = 48000            # Hz
channels = 1          # mono

print("Recording... (5 seconds)")
recording = sd.rec(
    int(duration * fs),
    samplerate=fs,
    channels=channels,
    dtype='float32'   # record directly as 32-bit float
)
sd.wait()
print("Recording complete.")


# - Save the recorded audio as a WAV file in 32-bit floating-point format.
recording = np.asarray(recording, dtype=np.float32)

filename = "task1.wav"
write(filename, fs, recording)  # SciPy will write float32 WAV if data is float32
print(f"Saved: {filename} (float32)")

# - Play back the recorded audio using the speakers.

print("Playing back...")
sd.play(recording, samplerate=fs)
sd.wait()
print("Done.")





