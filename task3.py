### Task 3: Audio Analysis (Frequency domain and Spectorgram) (30\%)

import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import rfft, rfftfreq
from scipy.signal import spectrogram

# Write a Python script ```task3.py``` to:

def to_mono_float32(x: np.ndarray) -> np.ndarray:
    """Convert audio array to mono float32 in range [-1, 1] if originally integer."""
    if x.ndim == 2:
        x = x.mean(axis=1)  # stereo -> mono
    # Convert int PCM to float32 [-1, 1]
    if np.issubdtype(x.dtype, np.integer):
        max_val = np.iinfo(x.dtype).max
        x = x.astype(np.float32) / max_val
    else:
        x = x.astype(np.float32)
    return x

def main():
    
# - Read the recorded WAV file ```record.wav```.
    filename = "record_0.wav"
    fs, data = wavfile.read(filename)
    audio = to_mono_float32(data)
    
    print(f"Loaded '{filename}'")
    print(f"Sample rate: {fs} Hz")
    print(f"Samples: {len(audio)}")
    print(f"Duration: {len(audio) / fs:.2f} sec")
# - Play back the audio using the speakers.
    print("Playing back audio...")
    sd.play(audio, samplerate=fs)
    sd.wait()
    print("Playback done.")

# - Visualize the frequency domain of the audio using Fourier Transform (FFT).

    N = len(audio)
    audio_dc = audio - np.mean(audio) #remove DC offset (helps peak detection and plot clarity)
    
    #compute FFT
    X = rfft(audio_dc)
    freqs = rfftfreq(N, d=1/fs)
    
    #magnitude spectrum (linear)
    mag = np.abs(X)
    
    #convert to dB for better visualization 
    mag_db = 20 *np.log10(mag+ 1e-12)
    low_cut_hz = 20
    valid_idx = np.where(freqs >= low_cut_hz)[0]
    
    K = 10
    top_idx = valid_idx[np.argsort(mag[valid_idx])[-K:]][::-1]

    print("\nDominant frequency components (approx.):")
    for i, idx in enumerate(top_idx, start=1):
        print(f"{i:2d}) {freqs[idx]:8.1f} Hz | magnitude={mag[idx]:.6f}")

    print("\nInterpretation guide:")
    print("- Peaks near ~60 Hz (or 50 Hz) and multiples can indicate electrical hum.")
    print("- Broad energy 100 Hz–4 kHz is common for speech.")
    print("- Very high peaks at specific frequencies indicate tonal sounds.")
    print("- If the recording is mostly noise, the spectrum will look flatter.\n")
    
    plt.figure()
    plt.plot(freqs, mag_db)
    plt.title("FFT Magnitude Spectrum (dB)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.xlim(0, min(24000, fs/2))  # show up to Nyquist (max 24k for 48k fs)
    plt.grid(True)
    
# - Visualize the time-frequency domain of the sound signals.
    # Use spectrogram (FFT in short windows)
    f, t, Sxx = spectrogram(
        audio_dc,
        fs=fs,
        window="hann",
        nperseg=2048,
        noverlap=1024,
        scaling="density",
        mode="magnitude"
    )

    Sxx_db = 20 * np.log10(Sxx + 1e-12)

    plt.figure()
    plt.pcolormesh(t, f, Sxx_db, shading="gouraud")
    plt.title("Spectrogram (Time-Frequency, dB)")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.ylim(0, min(24000, fs/2))
    plt.colorbar(label="Magnitude (dB)")

    plt.show()


# - Analysis the frequency components.

if __name__ == "__main__":
    main()


# Analysis results of ```record.wav```: 
# - What are the dominant frequency components in the audio?

# The dominant frequency component of the recording is a strong narrowband tone near 20.5 kHz, 
# with additional high-frequency content around 18.4 kHz. 
# Lower-frequency components include a mid-frequency tone near 1 kHz and a 120 Hz component consistent with power-line interference. 
# The spectrogram confirms that the high-frequency tones are stable over time, 
# while the remaining spectrum consists primarily of broadband noise.

# Dominant frequency components (approx.):
#  1)  20480.0 Hz | magnitude=18752.914062
#  2)   1024.0 Hz | magnitude=8415.040039
#  3)  18432.0 Hz | magnitude=5846.565430
#  4)  20479.7 Hz | magnitude=843.209595
#  5)    120.0 Hz | magnitude=745.751587
#  6)  20479.3 Hz | magnitude=591.159058
#  7)  20484.7 Hz | magnitude=562.351807
#  8)  20485.0 Hz | magnitude=552.776794
#  9)  20484.3 Hz | magnitude=543.476929
# 10)  20485.3 Hz | magnitude=540.898499


