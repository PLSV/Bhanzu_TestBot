import requests
from elevenlabs import set_api_key
import os
from playsound import playsound

def read_report(report_data):
    voice_setup()
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.environ.get('ELEVEN_LABS_API_KEY')
    }

    data = {
        "text": "Congratulations on completing the worksheet. This shows that you are willing to learn and improve. Keep up the good work!!",
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    print("Playing sound now!!")
    playsound('output.mp3')

def voice_setup():
    ELEVEN_LABS_API_KEY = os.environ.get('ELEVEN_LABS_API_KEY')
    set_api_key(ELEVEN_LABS_API_KEY)