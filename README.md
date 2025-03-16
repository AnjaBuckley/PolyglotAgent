# Language Learning Assistant

A comprehensive language learning tool that combines various features to help users learn new languages through songs, poems, vocabulary, and interactive exercises.

## Features

### Core Functionality
- Language detection and validation
- Content translation
- Vocabulary extraction
- Practice exercise generation

### Audio Support
Audio generation is available when specifically requested using keywords:
- "pronounce"
- "pronunciation"
- "say"
- "speak"
- "audio"
- "sound"

### Content Types
1. **Songs**
   - Lyrics retrieval
   - Translation
   - YouTube video links
   - Optional pronunciation audio

2. **Poems**
   - Text retrieval
   - Translation
   - Optional pronunciation audio

3. **Vocabulary**
   - Topic-based word lists
   - Translations
   - Optional pronunciation audio

4. **Translations**
   - Text translation
   - Optional pronunciation audio

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd language-learning-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure
Polyglot/
├── .env # For API keys if needed
├── .gitignore # Git ignore file
├── README.md # Project documentation
├── requirements.txt # Dependencies
├── src/
│ ├── init.py
│ ├── language_learning_assistant.py
│ └── tools/
│ ├── init.py
│ ├── audio_tools.py
│ ├── content_tools.py
│ ├── search_tools.py
│ └── validation_tools.py
└── test_assistant.py # Main test/demo script

## Usage Examples

### With Audio Generation
```python
# These requests will include audio
requests_with_audio = [
    "How do you pronounce 'hello' in German?",
    "Can you teach me how to say 'good morning' in Spanish?",
    "I want to hear the pronunciation of these French words about food"
]
```

### Without Audio Generation
```python
# These requests will not include audio
requests_without_audio = [
    "Find me a German song about love",
    "Translate 'good evening' to Italian",
    "Show me some Spanish vocabulary about colors"
]
```

### Basic Usage
```python
from src.language_learning_assistant import LanguageLearningAssistant
import asyncio

async def main():
    assistant = LanguageLearningAssistant()
    
    # Example with audio
    result = await assistant.process_request(
        "How do you pronounce 'hello' in German?"
    )
    print(result)  # Will include audio paths
    
    # Example without audio
    result = await assistant.process_request(
        "Translate 'good morning' to Spanish"
    )
    print(result)  # Will not include audio

if __name__ == "__main__":
    asyncio.run(main())
```

## Response Format

### With Audio Request
```python
{
    "status": "success",
    "type": "translation",
    "content": {
        "original_text": str,
        "translation": str,
        "vocabulary": {
            "words": List[str],
            "translations": Dict[str, str]
        }
    },
    "audio": "path/to/audio.mp3",  # Only included when audio is requested
    "exercises": Dict
}
```

### Without Audio Request
```python
{
    "status": "success",
    "type": "translation",
    "content": {
        "original_text": str,
        "translation": str,
        "vocabulary": {
            "words": List[str],
            "translations": Dict[str, str]
        }
    },
    "exercises": Dict
}
```

## Supported Languages
- German (de)
- Spanish (es)
- French (fr)
- Italian (it)

## Testing
Run the test script to see examples of different types of requests:
```bash
python test_assistant.py
```

## Error Handling
The assistant validates requests and returns appropriate error messages:
```python
{
    "status": "error",
    "message": "Please ask a language-related question."
}
```

## Dependencies
- deep-translator: For translations
- gTTS: For audio generation (when requested)
- langdetect: For language detection
- duckduckgo-search: For web content retrieval

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License

## Notes
- Audio files are only generated when explicitly requested
- Audio generation requires internet connection (uses gTTS)
- Generated audio files are saved in the `generated_audio` directory