import asyncio
from src.language_learning_assistant import LanguageLearningAssistant
import json


async def test_assistant():
    assistant = LanguageLearningAssistant()

    # Test requests with and without audio
    test_requests = [
        # Requests that should include audio
        "How do you pronounce 'hello' in German?",
        "Can you teach me how to say 'good morning' in Spanish?",
        "I want to hear the pronunciation of these French words about food",
        # Requests that should not include audio
        "Find me a German song about love",
        "Translate 'good evening' to Italian",
        "Show me some Spanish vocabulary about colors",
        # Edge cases
        "Tell me a joke",  # Should fail validation
        "What's the weather like?",  # Should fail validation
    ]

    for request in test_requests:
        print("\n" + "=" * 50)
        print(f"Testing request: {request}")
        print("=" * 50)

        result = await assistant.process_request(request)

        # Pretty print the result
        print("\nResult:")
        if isinstance(result, dict):
            # Check if audio was generated
            has_audio = "audio" in result or "vocabulary_audio" in result
            print(f"\nAudio generated: {has_audio}")
            print("\nResponse structure:")
            print(json.dumps(result, indent=2))
        else:
            print(result)
        print("\n")


if __name__ == "__main__":
    asyncio.run(test_assistant())
