from pydub import AudioSegment
from pydub.playback import play

def convert_webm_to_wav_file(input_file, output_file):

    # Load the WebM audio file
    audio = AudioSegment.from_file(input_file, format="webm")

    # Set the desired audio properties
    sample_rate = 16000
    channels = 1  # Mono
    sample_width = 2  # 16-bit

    # Resample the audio to the desired sample rate (16 kHz)
    audio = audio.set_frame_rate(sample_rate)

    # Set the number of channels to mono (1 channel)
    audio = audio.set_channels(channels)

    # Set the sample width to 16-bit
    audio = audio.set_sample_width(sample_width)

    # Export the audio to WAV format
    audio.export(output_file, format="wav")

    return output_file
