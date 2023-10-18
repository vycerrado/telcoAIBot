
import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv('.env')

def text_to_speech(text, filename=None):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))

    if filename is not None:
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True, filename=filename)
    else:
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name = os.environ.get('SPEECH_VOICE_NAME', 'en-IN-NeerjaNeural')
    # speech_config.speech_synthesis_pitch = 200
    # speech_config.speech_synthesis_rate = -100
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Get text from the console and synthesize to the default speaker.

    if '<' in text:
        speech_synthesis_result = speech_synthesizer.speak_ssml(f"""
                                    <speak
                                        xmlns="http://www.w3.org/2001/10/synthesis"
                                        xmlns:mstts="http://www.w3.org/2001/mstts"
                                        xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-IN">
                                        <voice name="{speech_config.speech_synthesis_voice_name}">
                                            {text}
                                        </voice>
                                    </speak>
                                    """)

    else:
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()


    return speech_synthesis_result

