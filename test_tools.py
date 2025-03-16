import asyncio
from src.tools.audio_tools import generate_audio
from src.tools.search_tools import web_search, find_youtube_video, get_song_lyrics
from src.tools.content_tools import ContentCreator, generate_practice_lessons
from src.tools.validation_tools import analyze_language_confidence
import json


def test_tools():
    print("\n=== Testing Validation Tool ===")
    test_texts = [
        "How do you say 'hello' in German?",
        "What's the weather like today?",
        "Ich möchte Deutsch lernen",
        "Can you translate this to Spanish?",
    ]

    for text in test_texts:
        result = analyze_language_confidence(text)
        print(f"\nInput: {text}")
        print(f"Analysis: {result}")

    print("\n=== Testing Content Creation ===")
    creator = ContentCreator()
    content = creator.create_learning_content(
        text="Guten Morgen, wie geht es dir?",
        target_language="de",
        native_language="en",
    )
    print("\nLearning content:", json.dumps(content, indent=2))

    # Generate practice lessons
    if "vocabulary" in content:
        exercises = generate_practice_lessons(
            content["vocabulary"]["words"], content["vocabulary"]["translations"]
        )
        print("\nPractice exercises:", json.dumps(exercises, indent=2))

    print("\n=== Testing Audio Generation ===")
    audio_result = generate_audio("Hallo, wie geht es dir?", "german")
    print(f"Audio file generated: {audio_result}")

    print("\n=== Testing Search ===")
    search_result = web_search("99 Luftballons song meaning")
    print(f"Search results: {search_result}")


if __name__ == "__main__":
    test_tools()
