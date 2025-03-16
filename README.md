# Language Learning Assistant

A comprehensive language learning tool that combines various features to help users learn new languages through songs, poems, vocabulary, and interactive exercises.

## Features

- **Language Detection & Validation**
  - Automatically detects target language
  - Validates language learning requests
  - Supports multiple languages (German, Spanish, French, Italian)

- **Content Types**
  - Songs with lyrics and translations
  - Poems with analysis
  - Vocabulary lists
  - Translation requests

- **Learning Tools**
  - Audio pronunciation
  - Vocabulary exercises
  - Translation support
  - Practice lessons
  - YouTube video integration (for songs)

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

```

## Usage

### Basic Usage

```python
from src.language_learning_assistant import LanguageLearningAssistant
import asyncio

async def main():
    assistant = LanguageLearningAssistant()
    
    # Example requests
    requests = [
        "Can you find me a German song about love?",
        "I want to learn Spanish vocabulary about food",
        "How do you say 'good morning' in French?",
        "Find me an Italian poem"
    ]
    
    for request in requests:
        result = await assistant.process_request(request)
        print(f"\nRequest: {request}")
        print("Result:", result)

if __name__ == "__main__":
    asyncio.run(main())
```

### Example Requests

1. **Songs**
```python
result = await assistant.process_request("Can you find me a German song about love?")
```

2. **Vocabulary**
```python
result = await assistant.process_request("I want to learn Spanish vocabulary about food")
```

3. **Translations**
```python
result = await assistant.process_request("How do you say 'good morning' in French?")
```

4. **Poems**
```python
result = await assistant.process_request("Find me an Italian poem")
```

## Response Format

The assistant returns responses in the following format:

```python
{
    "status": "success",
    "type": "song|poem|vocabulary|translation",
    "content": {
        "original_text": str,
        "translation": str,
        "vocabulary": {
            "words": List[str],
            "translations": Dict[str, str]
        },
        "difficulty_level": str
    },
    "audio": str,  # Path to audio file
    "exercises": Dict,  # Practice exercises
    "video": Dict  # For songs only
}
```

## Tools

### Validation Tool
- Analyzes requests to determine if they're language-learning related
- Calculates confidence scores
- Detects target language

### Content Tool
- Generates translations
- Creates vocabulary lists
- Assesses content difficulty
- Generates practice exercises

### Audio Tool
- Creates pronunciation audio files
- Supports multiple languages
- Uses gTTS (Google Text-to-Speech)

### Search Tool
- Finds songs and poems
- Retrieves lyrics and content
- Searches for related videos

## Supported Languages

- German (de)
- Spanish (es)
- French (fr)
- Italian (it)

## Development

To run tests:
```bash
python test_assistant.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Acknowledgments

- Uses DuckDuckGo for web searches
- Uses Google Text-to-Speech for audio generation
- Uses deep-translator for translations