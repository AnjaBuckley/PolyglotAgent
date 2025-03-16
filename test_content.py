import json
from src.tools.content_tools import ContentCreator, generate_practice_lessons


def test_translation():
    creator = ContentCreator()

    # Test with German
    german_text = "Guten Morgen, wie geht es dir?"
    print("\nTesting German translation:")
    content = creator.create_learning_content(
        text=german_text, target_language="de", native_language="en"
    )
    print(json.dumps(content, indent=2))

    # Test with Spanish
    spanish_text = "¿Cómo estás? Buenos días!"
    print("\nTesting Spanish translation:")
    content = creator.create_learning_content(
        text=spanish_text, target_language="es", native_language="en"
    )
    print(json.dumps(content, indent=2))

    # Generate practice exercises
    print("\nGenerating practice exercises:")
    exercises = generate_practice_lessons(
        content["vocabulary"]["words"], content["vocabulary"]["translations"]
    )
    print(json.dumps(exercises, indent=2))


if __name__ == "__main__":
    test_translation()
