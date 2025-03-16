from gtts import gTTS
import os
from datetime import datetime


def generate_audio(text: str, language: str) -> str:
    """
    Generates audio file for the given text in specified language.

    Args:
        text (str): The text to convert to speech
        language (str): Language code (e.g., 'de' for German, 'es' for Spanish)

    Returns:
        str: Path to the generated audio file
    """
    try:
        # Create output directory if it doesn't exist
        output_dir = "generated_audio"
        os.makedirs(output_dir, exist_ok=True)

        # Generate unique filename using timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/audio_{timestamp}.mp3"

        # Convert language names to codes if necessary
        language_codes = {
            "german": "de",
            "spanish": "es",
            "french": "fr",
            # Add more as needed
        }
        lang_code = language_codes.get(language.lower(), language.lower())

        # Generate audio file
        tts = gTTS(text=text, lang=lang_code)
        tts.save(filename)

        return filename

    except Exception as e:
        return f"Error generating audio: {str(e)}"
