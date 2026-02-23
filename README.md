# PA1_1 – Ultrasound Sensing & Audio Processing (EECS 498/598)

This project explores audio signal processing and ultrasound-based gesture sensing using Python. It covers microphone testing, sine wave generation, frequency analysis, ultrasound down-conversion, filtering, Doppler spectrogram extraction, and real-time data collection.
The assignment progresses from basic audio system interaction to extracting Doppler features from ultrasound signals for gesture recognition.

**Project Overview**

Task 0 – Audio Setup

	•	Query available audio devices
	•	Configure default microphone and speaker
	•	Verify audio system using sounddevice

Task 1 – Microphone & Speaker Test

	•	Record 5 seconds of audio (48 kHz, mono)
	•	Save as 32-bit float WAV file
	•	Playback recorded audio

Task 2 – Sine Wave Generation

	•	Generate 400 Hz sine wave
	•	Generate 20 kHz sine wave
	•	Generate combined ultrasonic tones (20 kHz + 20.25 kHz, 20 kHz + 21 kHz)
	•	Playback signals

Task 3 – Audio Analysis

	•	Compute FFT
	•	Plot frequency spectrum
	•	Generate spectrogram
	•	Analyze frequency components

Task 4–6 – Ultrasound Signal Processing

	•	Read 20.48 kHz ultrasound recording
	•	Down-convert to baseband (I/Q components)
	•	Apply 5th-order Butterworth low-pass filter (100 Hz cutoff)
	•	Plot I/Q time series and phase trajectory
	•	Downsample filtered signals
	•	Compute Doppler spectrogram using STFT
	•	Focus on ±150 Hz Doppler shift region

Task 7 – Data Collection Tool

	•	3-second rolling audio buffer
	•	Continuous 20 kHz playback
	•	Press r to save WAV file

Task 8 – Custom Data Collection

	•	Locate laptop microphone
	•	Record push/pull gesture
	•	Extract Doppler features

**HOW TO RUN THE FILES**
Install required libraries:
pip install sounddevice numpy scipy matplotlib

Each task is implemented as a separate Python script.
Run using:

python3 task0.py
python3 task1.py
python3 task2.py
python3 task3.py
python3 task4_6.py
python3 task7.py

Make sure:

	•	Your microphone and speakers are enabled
	•	Default audio devices are configured correctly
	•	You run scripts from the project directory

