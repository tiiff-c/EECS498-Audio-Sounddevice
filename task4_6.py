import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, filtfilt, spectrogram

## Task 4: Ultrasound Down Conversion (30\%)

# To run each task, change the task function at the end of the script under "if __name__ == "__main__":"

def task4():
    # filename = "record_1.wav"
    filename = "task8_record.wav"
    # fc = 20480.0 # transmitted ultrasound frequency (Hz)
    fc = 20000.0 # for task 8
    
    #read WAV
    fs, data = wavfile.read(filename)
    
    # print("dtype:", data.dtype)
    # print("min/max before:", data.min(), data.max())
    
    # s = to_mono_float(data) 
    # normalize WAV
    # s = data.astype(np.float32) / np.max(np.abs(data))
    
    s = data / np.max(np.abs(data))
    
    #time axis 
    N = len(s)
    t = np.arange(N) / fs
    
    # Down-convert (NO low-pass) + scale by 2 to match common baseband amplitude
    I = s * np.cos(2 * np.pi * fc * t)
    Q = s * (-np.sin(2 * np.pi * fc * t))
    
    
    # normalize for plotting
    peak = max(np.max(np.abs(I)), np.max(np.abs(Q)))
    I /= peak
    Q /= peak

    # Plot first 3 seconds
    idx = int(3 * fs)

    plt.figure(figsize=(12, 5))
    plt.plot(t[:idx], I[:idx], label="Real Part")
    plt.plot(t[:idx], Q[:idx], label="Imaginary Part")
    plt.title("Baseband Signal (Real and Imaginary Parts)")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()


  
     

## Task 5: Low-pass Filtering(30\%)
def task5():
    # filename = "record_1.wav"
    filename = "task8_record.wav"
    #fc = 20480.0 # transmitted ultrasound frequency (Hz)
    fc = 20000.0 # transmitted ultrasound frequency (Hz) for task 8
    fs, data = wavfile.read(filename)

    
    s = data / np.max(np.abs(data))
    #time axis 
    N = len(s)
    t = np.arange(N) / fs
    
    # Down-convert (NO low-pass) + scale by 2 to match common baseband amplitude
    I = s * np.cos(2 * np.pi * fc * t)
    Q = s * (-np.sin(2 * np.pi * fc * t))
    
    #5th order butterworth lpf @ 100Hz
    order = 5
    cutoff = 100.0
    Wn = cutoff / (fs / 2)            # normalize by Nyquist
    b, a = butter(order, Wn, btype="low")
    
    I_f = filtfilt(b, a, I)
    Q_f = filtfilt(b, a, Q)
    
    
    
    # plot 1 filtered I/Q time series
    t_end = 3.0
    idx_end = int(min(N, t_end * fs))

    plt.figure(figsize=(12, 5))
    plt.plot(t[:idx_end], I_f[:idx_end], label="Real Part (Filtered I)")
    plt.plot(t[:idx_end], Q_f[:idx_end], label="Imaginary Part (Filtered Q)")
    plt.title("Filtered Baseband Signal (Real and Imaginary Parts)")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()
    
    # plot 2
    t_iq = 0.5
    idx_iq = int(min(N, t_iq * fs))

    plt.figure(figsize=(8, 6))
    plt.plot(I_f[:idx_iq], Q_f[:idx_iq])
    plt.title("IQ Space (First 0.5 s, Filtered)")
    plt.xlabel("I Component")
    plt.ylabel("Q Component")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


## Task 6: Feature Extraction: Ultrasound Doppler Spectrogram(30\%)

def task6():
    # filename = "record_1.wav"
    filename = "task8_record.wav"
    # fc = 20480.0
    fc = 20000.0 # for task 8
    downsample_factor = 8


    fs, data = wavfile.read(filename)
    s = data / np.max(np.abs(data))

    N = len(s)
    t = np.arange(N) / fs

    I = s * np.cos(2 * np.pi * fc * t)
    Q = s * (-np.sin(2 * np.pi * fc * t))


    cutoff = 100.0
    Wn = cutoff / (fs / 2.0)
    b, a = butter(5, Wn, btype="low")
    I_f = filtfilt(b, a, I)
    Q_f = filtfilt(b, a, Q)

    I_ds = I_f[::downsample_factor]
    Q_ds = Q_f[::downsample_factor]
    fs_ds = fs / downsample_factor

    z = I_ds + 1j * Q_ds


    # Compute spectrogram (magnitude)
    f, tt, S = spectrogram(
        z,
        fs=fs_ds,
        window="hamming",
        nperseg=1024,
        noverlap=128,
        nfft=1024,
        detrend=False,
        scaling="density",
        mode="magnitude"
    )

    # Center frequency around 0 Hz (Doppler about baseband)
    S_shift = np.fft.fftshift(S, axes=0)
    f_shift = np.fft.fftshift(f)
    

    # Focus on Doppler range ±150 Hz
    mask = (f_shift >= -150) & (f_shift <= 150)
    f_focus = f_shift[mask]
    S_focus = S_shift[mask, :]

    # Convert to dB
    S_db = 20 * np.log10(S_focus + 1e-12)


    plt.figure(figsize=(10, 5))
    plt.pcolormesh(tt, f_focus, S_db, shading="gouraud", cmap="jet")
    plt.title("Ultrasound Doppler Spectrogram (Baseband ±150 Hz)")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.yticks(np.arange(-150, 151, 25))
    cbar = plt.colorbar()
    cbar.set_label("Amplitude (dB)")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    task4()