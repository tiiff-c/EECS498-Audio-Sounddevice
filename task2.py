### Task 2: Generate and Play a continuous sine Wave (30\%)

import sounddevice as sd
import numpy as np

# Write a Python script ```task2.py``` to:

# - Generate a mono-channel 400 Hz sine wave with a 5-second duration and a sampling rate of 48 kHz.

# - Play back the generated sine wave using sounddevice.

# - Repeat the above steps for:

#    - 20,000 Hz sine wave.

#   - 20,000 Hz and 20,250 Hz combined signals.

#    - 20,000 Hz and 21,000 Hz combined signals.


def play_signal(signal, fs, label):
    print(f"Playing: {label}")
    sd.play(signal, samplerate=fs)
    sd.wait()

def main():
    fs = 4800 #sampling rate (Hz)
    duration = 5
    A = 0.5
  
    t = np.linspace(0, duration, int(fs*duration), endpoint=False)
  
    #400 Hz sine wave
    f1 = 400
    sine_400 = A * np.sin(2*np.pi*f1*t)
    play_signal(sine_400.astype(np.float32), fs, "400 Hz")
  
    #20000 Hz sine wave
    f2 = 20000
    sine_20000 = A * np.sin(2*np.pi*f2*t)
    play_signal(sine_20000.astype(np.float32), fs, "20000 Hz")
  
    #20000 Hz + 20250 Hz
    f3 = 20250
    combo1 = A * (np.sin(2*np.pi*f2*t) + np.sin(2*np.pi*f3*t)) / 2 # divide to avoid clipping
    play_signal(combo1.astype(np.float32), fs, "20000 Hz + 20250 Hz")


    #20000 Hz + 21000 Hz
    f4 = 21000
    combo2 = A * (np.sin(2*np.pi*f2*t) + np.sin(2*np.pi*f4*t)) / 2 # divide to avoid clipping
    play_signal(combo2.astype(np.float32), fs, "20000 Hz + 21000 Hz")
    
    
    print("Finished playing all signals.")
  
    
    
if __name__ == "__main__":
    main()