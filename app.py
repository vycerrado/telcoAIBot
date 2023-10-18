from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
import os
from modules.query_LLM import get_LLM_response
from modules.speech_to_text import speech_to_text_from_file, speech_to_text_from_stream
from fastapi.responses import FileResponse
from modules.text_to_speech import text_to_speech
from modules.utils import convert_webm_to_wav_file



app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



# Define an endpoint to receive audio data.
@app.post("/upload-audio/")
async def upload_audio(audio_file: UploadFile = File(...), conversation_log: str = Form(...)):
    try:
        if audio_file.content_type != "audio/webm":
            return JSONResponse(content={"error": "Invalid audio format"}, status_code=400)

        # Save the uploaded audio file to a temporary location.
        audio_file_path = f"uploaded_audio/{audio_file.filename}"

        print("CONVERSATION LOG", conversation_log)

        with open(audio_file_path, "wb") as file:
            file.write(audio_file.file.read())

        # Convert into wav file
        input_file = audio_file_path
        user_wav_audio_filepath = 'uploaded_audio/output.wav'
        user_wav_audio_filepath = convert_webm_to_wav_file(input_file, user_wav_audio_filepath)

        # Pass to Azure for speech to text
        recognized_text = speech_to_text_from_file(user_wav_audio_filepath)

        # LLM conversation
        bot_response = get_LLM_response(conversation_log, recognized_text)

        bot_response_audio_filepath = 'uploaded_audio/bot_response.wav'

        # use Azure text to Speech to prepare bot audio response
        text_to_speech(bot_response, filename=bot_response_audio_filepath)


        # Add your audio processing logic here.
        # For this example, we simply return a success message.

        print({"message": "Audio processing complete", 
                "recognized_text":recognized_text['recognized_text'],
                "bot_response":bot_response})
        
        response = FileResponse(bot_response_audio_filepath, headers={"message": "Audio processing complete", 
                                                  "recognized_text":recognized_text['recognized_text'].replace('\n', ' '),
                                                  "bot_response":bot_response.replace('\n', ' ')})


        return response

    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("templates/index.html", "r") as file:
        content = file.read()
    return content

if __name__ == "__main__":
    os.makedirs("uploaded_audio", exist_ok=True)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
