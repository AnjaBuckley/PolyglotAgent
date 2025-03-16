from src.tools.validation_tools import analyze_language_confidence


def test_validation():
    # Test cases with expected high confidence
    high_confidence_cases = [
        "How do you say 'hello' in German?",
        "Can you translate this to Spanish: Good morning",
        "I want to learn French vocabulary about food",
        "Was bedeutet 'Apfel' auf Englisch?",  # German
        "¿Cómo se dice 'cat' en español?",  # Spanish
        "Ich möchte Deutsch lernen",  # German sentence
    ]

    # Test cases with expected low confidence
    low_confidence_cases = [
        "What's the weather like today?",
        "Can you order pizza for me?",
        "Tell me a joke",
        "What time is it?",
    ]

    print("\n=== Testing High Confidence Cases ===")
    print("These should all have confidence scores >= 0.8\n")

    for text in high_confidence_cases:
        result = analyze_language_confidence(text)
        print(f"Text: '{text}'")
        print(f"Confidence Score: {result['confidence_score']}")
        print(f"Is Language Question: {result['is_language_question']}")
        print(f"Detected Languages: {result.get('detected_languages', [])}")
        print(f"Analysis: {result.get('analysis', {})}")
        print("-" * 50)

    print("\n=== Testing Low Confidence Cases ===")
    print("These should all have confidence scores < 0.8\n")

    for text in low_confidence_cases:
        result = analyze_language_confidence(text)
        print(f"Text: '{text}'")
        print(f"Confidence Score: {result['confidence_score']}")
        print(f"Is Language Question: {result['is_language_question']}")
        print(f"Analysis: {result.get('analysis', {})}")
        print("-" * 50)

    # Test edge cases
    print("\n=== Testing Edge Cases ===")
    edge_cases = [
        "",  # Empty string
        "?",  # Just punctuation
        "a" * 1000,  # Very long input
        "123456",  # Just numbers
        "¿¿¿???!!!",  # Just punctuation
    ]

    for text in edge_cases:
        result = analyze_language_confidence(text)
        print(f"Text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        print(f"Confidence Score: {result['confidence_score']}")
        print(f"Is Language Question: {result['is_language_question']}")
        print("-" * 50)

    # Test specific language detection
    print("\n=== Testing Language Detection ===")
    language_samples = [
        ("Guten Tag, wie geht es dir?", "German"),
        ("Buenos días, ¿cómo estás?", "Spanish"),
        ("Bonjour, comment allez-vous?", "French"),
        ("Hello, how are you?", "English"),
        ("Ciao, come stai?", "Italian"),
    ]

    for text, expected_language in language_samples:
        result = analyze_language_confidence(text)
        print(f"Text: '{text}'")
        print(f"Expected Language: {expected_language}")
        print(f"Detected Languages: {result.get('detected_languages', [])}")
        print(f"Confidence Score: {result['confidence_score']}")
        print("-" * 50)


if __name__ == "__main__":
    test_validation()
