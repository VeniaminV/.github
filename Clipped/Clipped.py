import numpy as np
import scipy.io.wavfile as wav
import sounddevice as sd


NSECS = 1                 # duration in seconds
SAMPLE_RATE = 48000       # samples per second
NSAMPLES = NSECS * SAMPLE_RATE
FREQUENCY = 440           # tone frequency in Hz

# make time values from 0 to 1 second
t = np.linspace(0, NSECS, num=NSAMPLES, endpoint=False, dtype=np.float32)


# Part 1. making the normal sine wave


# quarter amplitude sine wave (-8192 to 8192)
sine_wave = np.sin(2 * np.pi * FREQUENCY * t) * 8192

# convert to 16-bit signed integers
sine_wave = sine_wave.astype(np.int16)

# saving  to sine.wav
wav.write("sine.wav", SAMPLE_RATE, sine_wave)



# Part 2. make clipped sine wave


# half amplitude sine wave (-16384 to 16384)
clipped_wave = np.sin(2 * np.pi * FREQUENCY * t) * 16384

# clip values so they stay between -8192 and 8192
clipped_wave = np.clip(clipped_wave, -8192, 8192)

# convert to 16-bit signed integers
clipped_wave = clipped_wave.astype(np.int16)

# save to clipped.wav
wav.write("clipped.wav", SAMPLE_RATE, clipped_wave)


# Part 3. play clipped sine wave

sd.play(clipped_wave, SAMPLE_RATE)

# will wait until the sound has finished playing before exiting the program
sd.wait()
