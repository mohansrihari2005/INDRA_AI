import io
import base64
from gtts import gTTS


def generate_voice_alert(text: str, lang: str):
    """
    Generate audio from text using gTTS.
    lang: 'te' (Telugu), 'hi' (Hindi), 'en' (English), 'or' (Odia), 'ta' (Tamil)
    Returns: base64-encoded MP3 data
    """
    lang_map = {
        "te": "te",
        "hi": "hi",
        "en": "en",
        "or": "or",
        "ta": "ta",
    }

    gtts_lang = lang_map.get(lang, "en")

    try:
        tts = gTTS(text=text, lang=gtts_lang, slow=False)

        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode("utf-8")

        return audio_base64

    except Exception as e:
        raise Exception(f"Voice generation failed: {str(e)}")
