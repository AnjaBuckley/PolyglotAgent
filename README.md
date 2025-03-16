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

## How It Works: Tool Selection Logic

The Language Learning Assistant uses a sophisticated decision-making process to determine which tools to use based on the user's request. This process happens in multiple layers:

### Decision Layers

1. **Validation Layer** (Always Used)
```python
validation = analyze_language_confidence(user_request)
```
- Uses validation_tools to check if the request is language-learning related
- Determines the confidence score
- Detects the target language

2. **Audio Layer** (Conditionally Used)
```python
wants_audio = any(word in user_request.lower() 
                for word in ['pronounce', 'pronunciation', 'say', 'speak', 'audio', 'sound'])
```
- Checks if audio generation is requested
- Only activates audio_tools if specifically asked

3. **Content Type Layer** (Tool Combinations)
```python
if "song" in user_request.lower():
    return await self._handle_song_request(...)
elif "poem" in user_request.lower():
    return await self._handle_poem_request(...)
elif any(word in user_request.lower() for word in ["vocabulary", "words", "vocab"]):
    return await self._handle_vocabulary_request(...)
else:
    return await self._handle_general_translation_request(...)
```

### Tool Combinations by Request Type

1. **Song Requests**
   - search_tools.web_search (find songs)
   - search_tools.find_youtube_video (get video)
   - search_tools.get_song_lyrics (get lyrics)
   - content_tools.create_learning_content (translation)
   - audio_tools.generate_audio (if requested)

2. **Poem Requests**
   - search_tools.web_search (find poems)
   - content_tools.create_learning_content (translation)
   - audio_tools.generate_audio (if requested)

3. **Vocabulary Requests**
   - content_tools.create_learning_content (word lists)
   - content_tools.generate_practice_lessons
   - audio_tools.generate_audio (if requested)

4. **Translation Requests**
   - content_tools.create_learning_content
   - audio_tools.generate_audio (if requested)

### Example Requests and Tool Usage

```python
# Uses search_tools, content_tools, and audio_tools
"How do you pronounce this German song about love?"

# Uses only search_tools and content_tools
"Find me a Spanish poem"

# Uses content_tools and audio_tools
"How do you say 'hello' in French?"

# Uses only content_tools
"Translate 'good morning' to Italian"
```

### Implementation Example

Here's how the agent processes a song request with pronunciation:

```python
async def _handle_song_request(self, request: str, target_language: str, native_language: str, wants_audio: bool) -> Dict:
    # 1. Use search tools to find song
    search_results = web_search(f"popular {target_language} song lyrics")
    
    # 2. Get video information
    video_info = find_youtube_video(search_results.split('\n')[0])
    
    # 3. Get lyrics
    lyrics = get_song_lyrics(search_results.split('\n')[0])
    
    # 4. Create learning content
    content = self.content_creator.create_learning_content(
        text=lyrics,
        target_language=target_language,
        native_language=native_language
    )
    
    result = {
        "status": "success",
        "type": "song",
        "content": content,
        "video": video_info,
    }

    # 5. Generate audio if requested
    if wants_audio:
        vocab_audio = {}
        for word in content["vocabulary"]["words"]:
            audio_path = generate_audio(word, target_language)
            vocab_audio[word] = audio_path
        result["vocabulary_audio"] = vocab_audio
    
    return result
```

### Benefits of This Approach

1. **Efficiency**: Only uses necessary tools for each request
2. **Modularity**: Easy to add new tools or request types
3. **Clarity**: Clear decision-making process
4. **Flexibility**: Can handle various types of language learning requests
5. **Resource Management**: Audio generation only when needed

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
