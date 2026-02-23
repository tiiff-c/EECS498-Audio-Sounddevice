### Task 7: Design an Data Collection Tool for Ultrasound Playback, Recording and File Saving

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import time
import threading
import sys
from pynput import keyboard


FS = 48000                  # sampling rate (Hz)
DURATION_BUF = 3            # seconds of rolling buffer
FC = 20000.0                # playback tone frequency (Hz)
AMP = 0.2                   # playback amplitude (keep modest to avoid clipping)
CHANNELS = 1                # mono

# Rolling buffer size
BUF_LEN = int(FS * DURATION_BUF)

# Ring buffer + write index
ring = np.zeros(BUF_LEN, dtype=np.float32)
write_idx = 0

# Phase accumulator for continuous sine (avoids clicks)
phase = 0.0
phase_inc = 2.0 * np.pi * FC / FS

# Lock for safe buffer snapshotting
lock = threading.Lock()

# Counter for filenames
save_count = 0

def snapshot_buffer():
    global ring, write_idx
    with lock:
        idx = write_idx
        # ring contains most recent samples ending at write_idx-1
        out = np.concatenate((ring[idx:], ring[:idx])).copy()
    return out

def save_wav():
    """Save last 3 seconds of mic audio to float32 WAV."""
    global save_count
    audio = snapshot_buffer()  # float32 (BUF_LEN,)
    save_count += 1
    filename = f"record_{save_count:03d}.wav"

    # scipy.io.wavfile.write writes float32 WAV if array is float32
    write(filename, FS, audio.astype(np.float32))
    print(f"\nSaved {filename} (last {DURATION_BUF} seconds, float32)\n")


def callback(indata, outdata, frames, time_info, status):
    """Full-duplex callback: record mic into ring buffer + play 20kHz tone."""
    global write_idx, ring, phase

    if status:
        # underrun/overrun warnings show here
        # not fatal; just print once in a while
        print(status, file=sys.stderr)

    # record
    # indata is shape (frames, channels)
    x = indata[:, 0].astype(np.float32)

    with lock:
        n = len(x)
        end = write_idx + n
        if end < BUF_LEN:
            ring[write_idx:end] = x
        else:
            first = BUF_LEN - write_idx
            ring[write_idx:] = x[:first]
            ring[:end % BUF_LEN] = x[first:]
        write_idx = end % BUF_LEN

    # play
    # Make a phase-continuous sine to avoid clicks at block boundaries
    phases = phase + phase_inc * np.arange(frames, dtype=np.float32)
    y = (AMP * np.sin(phases)).astype(np.float32)

    # Update phase for next callback
    phase = float((phases[-1] + phase_inc) % (2.0 * np.pi))

    outdata[:, 0] = y
    
running = True
    
def on_press(key):
    global running

    try:
        if key.char == 'r':
            save_wav()
        elif key.char == 'q':
            print("Quitting...")
            running = False
            return False   # stop listener
    except:
        pass


def main():
    print("Starting Task 7 tool...")
    print(f"- Recording mic into a {DURATION_BUF}s rolling buffer @ {FS} Hz")
    print(f"- Playing continuous {FC:.0f} Hz tone")
    print("Controls:")
    print("  r = save last 3 seconds to WAV")
    print("  q = quit\n")

# Write a Python script ```task7.py``` to:
    with sd.Stream(
        samplerate=FS,
        channels=CHANNELS,
        dtype="float32",
        callback=callback
    ):

# - Record audio using a 3-second streamable rolling buffer at a sampling rate of 48 kHz.

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        while running:
            time.sleep(0.1)
        
# - Continuously play back a 20,000 Hz sine wave using sounddevice. (in my callback)

# - Save the the rolling buffer audio as a WAV file in 32-bit floating-point format. (in save_wav)

if __name__ == "__main__":
    main()
