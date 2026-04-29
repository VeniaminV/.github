# .github
## This repository will hold projects from my CS416 computers, sound, and music at Portland State University.

### Clipped.py
This project generates and works with digital audio using Python. It creates a sine wave, saves it as a WAV file, creates a clipped version of the same wave, and then plays the clipped sound through the computer’s speakers.

I used NumPy to generate the sine wave and scipy.io.wavfile to save it as an audio file. At first it was a bit confusing, but once I understood how samples work, it made more sense. I then added clipping by limiting the values of the wave.
