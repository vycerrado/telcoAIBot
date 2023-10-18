import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

load_dotenv('.env')

# Replace with your subscription key and service region
subscription_key = os.environ.get('SPEECH_KEY')
service_region = os.environ.get('SPEECH_REGION')

def speech_to_text_microphone():
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, 
                                           region=service_region
                                           
                                           )
    
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        output = {'status':'success', 'recognized_text':result.text}
    elif result.reason == speechsdk.ResultReason.NoMatch:
        output = {'status':'failed', 'recognized_text':'No speech could be recognized'}
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        output = {'status':'cancelled', 'reason':'cancellation_details.reason'}
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    return output

def speech_to_text_from_file(audio_file_path):
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)

    # Set the path to your audio file
    audio_input = speechsdk.audio.AudioConfig(filename=audio_file_path)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        output = {'status': 'success', 'recognized_text': result.text}
    elif result.reason == speechsdk.ResultReason.NoMatch:
        output = {'status': 'failed', 'recognized_text': 'No speech could be recognized'}
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        output = {'status': 'cancelled', 'reason': cancellation_details.reason}
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    return output


def speech_to_text_from_stream(audio_stream):
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)

    audio_input = speechsdk.audio.AudioConfig(stream=audio_stream)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    else:
        return None

if __name__ == "__main__":
    speech_to_text_microphone()
