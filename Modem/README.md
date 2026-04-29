# Bell 103 Modem Decoder

Name: Veniamin Velikoretskikh  
Email: veniamin@pdx.edu  

## Description

This program decodes a message that was sent using a simplified Bell 103 modem protocol. The input is a .wav audio file, and the output is the decoded ASCII text.

The modem uses two tones:
- 2025 Hz = 0  
- 2225 Hz = 1  

Each character is sent using 10 bits (8N1 format):
- 1 start bit  
- 8 data bits (LSB first)  
- 1 stop bit  

## How it works

1. The program reads the WAV file and converts the samples to floats.
2. It splits the audio into chunks of 160 samples (1 bit each).
3. For each chunk, it checks which frequency is stronger (2025 or 2225 Hz).
4. It converts the detected bits into bytes using the 8N1 format.
5. The bytes are turned into ASCII characters.
6. The final message is printed and saved to MESSAGE.txt

   
## How to run
Make sure you have numpy and scipy installed:
pip install numpy scipy
