# Veniamin Velikoretskikh veniamin@pdx.edu
# CS416p computer music and sound assignment 2: Bell 103 modem decoder

import numpy as np
from scipy.io import wavfile
import os

# each bit is 160 samples (given: 48kHz / 300 baud ≈ 160 samples per bit)
BIT_SAMPLES = 160

FREQ_ZERO = 2025   # represents binary 0 (space tone)
FREQ_ONE = 2225    # represents binary 1 (mark tone)


#Load WAV file
# fs = sample frequency (rate)
# data = audio samples
def load_wav(filename):
    # check file exists before trying to read it
    if not os.path.exists(filename):
        raise FileNotFoundError(filename + " not found")

    # read WAV file sample rate and data
    fs, data = wavfile.read(filename)

    # take only first channel only
    if len(data.shape) > 1:
        data = data[:, 0]  

    # convert integers (-32768 to 32767) into floats (-1 to 1)
    # this avoids overflow when doing math later
    data = data.astype(np.float32) / 32768.0

    # debug info so we know file loaded correctly
    print("Loaded file:", filename)
    print("Sample rate:", fs)
    print("Total samples:", len(data))

    return fs, data



# Build reference sine/cos waves
def make_references(fs):
    # time index for one bit
    t = np.arange(BIT_SAMPLES)

    # We create sine/cos waves for both frequencies.
    # These are used to match against the signal. 

    # 2025 Hz references (for 0 bit)
    cos0 = np.cos(2 * np.pi * FREQ_ZERO * t / fs)
    sin0 = np.sin(2 * np.pi * FREQ_ZERO * t / fs)

    # 2225 Hz references (for 1 bit)
    cos1 = np.cos(2 * np.pi * FREQ_ONE * t / fs)
    sin1 = np.sin(2 * np.pi * FREQ_ONE * t / fs)

    return cos0, sin0, cos1, sin1



# Measure how strong a frequency is in a block
def tone_power(samples, cos_ref, sin_ref):
    # I and Q are correlation results

    I = np.dot(samples, cos_ref)
    Q = np.dot(samples, sin_ref)


    return I * I + Q * Q



# Convert audio into bits
def decode_bits(data, cos0, sin0, cos1, sin1):
    bits = []

    # go through audio in chunks of 160 samples (1 bit)
    for i in range(0, len(data), BIT_SAMPLES):
        block = data[i:i + BIT_SAMPLES]

        # if last block is incomplete, then we ignore it
        if len(block) < BIT_SAMPLES:
            break

        # measure how strong each frequency is
        power0 = tone_power(block, cos0, sin0)
        power1 = tone_power(block, cos1, sin1)

        # whichever tone is stronger determines the bit
        if power1 > power0:
            bits.append(1)
        else:
            bits.append(0)


    print("Total bits decoded:", len(bits))
    return bits



# Convert bits to bytes (8N1 format)
def bits_to_bytes(bits):
    output = []

    # we process bits in groups of 10: 1 start bit, 8 data bits, 1 stop bit
    for i in range(0, len(bits), 10):
        frame = bits[i:i + 10]

        if len(frame) < 10:
            break

        # framing bits
        start_bit = frame[0]
        data_bits = frame[1:9]
        stop_bit = frame[9]

        # check if framing looks correct
        # start should be 0, stop should be 1
        if start_bit != 0 or stop_bit != 1:
            print("Warning: framing issue at byte", i // 10)

        # convert 8 bits into one byte (LSB first)
        value = 0
        for j in range(8):
            value |= (data_bits[j] << j)

        output.append(value)

    print("Total bytes decoded:", len(output))
    return output


# Convert bytes to readable text
def bytes_to_string(byte_list):
    text = ""

    for b in byte_list:
        # keep printable ASCII + newline characters
        if 32 <= b <= 126 or b in (10, 13):
            text += chr(b)
        else:
            # replace unreadable bytes
            text += "?"

    return text



# Main program
def main():
    # input file (must exist in same folder)
    filename = "message.wav"

    # load audio
    fs, data = load_wav(filename)

    # build reference waves for correlation
    cos0, sin0, cos1, sin1 = make_references(fs)

    # convert waveform to bits
    bits = decode_bits(data, cos0, sin0, cos1, sin1)

    # group bits into bytes
    bytes_out = bits_to_bytes(bits)

    # convert bytes to text
    message = bytes_to_string(bytes_out)

    # show result
    print("\n")
    print("Decoded Message")

    print(message)

    # save output file as a message.txt
    with open("MESSAGE.txt", "w") as f:
        f.write(message)

    print("\nSaved as MESSAGE.txt")


# run program
if __name__ == "__main__":
    main()