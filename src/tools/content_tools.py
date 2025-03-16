from typing import Dict, List
from deep_translator import GoogleTranslator
import json


class ContentCreator:
    def __init__(self):
        self.translator = GoogleTranslator()

    def create_learning_content(
        self, text: str, target_language: str, native_language: str
    ) -> Dict:
        """
        Creates learning content including translations and key vocabulary.
        Uses free Google Translate API wrapper.

        Args:
            text: Text to analyze
            target_language: Language being learned (e.g., 'de' for German)
            native_language: Student's native language (e.g., 'en' for English)
        """
        try:
            # Extract key vocabulary first
            vocab_list = self._extract_key_vocabulary(text)

            # Set up translator
            translator = GoogleTranslator(
                source=target_language, target=native_language
            )

            # Translate full text
            full_translation = translator.translate(text)

            # Translate vocabulary
            vocab_translations = {}
            for word in vocab_list:
                try:
                    translation = translator.translate(word)
                    vocab_translations[word] = translation
                except:
                    vocab_translations[word] = f"[Translation error for: {word}]"

            return {
                "original_text": text,
                "translation": full_translation,
                "vocabulary": {"words": vocab_list, "translations": vocab_translations},
                "difficulty_level": self._assess_difficulty(text),
                "language_pair": f"{target_language}-{native_language}",
            }

        except Exception as e:
            return {
                "error": f"Error creating learning content: {str(e)}",
                "original_text": text,
            }

    def _extract_key_vocabulary(self, text: str) -> List[str]:
        """
        Extracts important vocabulary from the text.
        Basic implementation - could be enhanced with NLP.
        """
        # Remove punctuation and split into words
        words = text.lower().replace(",", " ").replace(".", " ").split()
        # Remove duplicates and sort by length (longer words often more important)
        unique_words = sorted(set(words), key=len, reverse=True)
        # Return top 10 words (could be improved with actual importance scoring)
        return unique_words[:10]

    def _assess_difficulty(self, text: str) -> str:
        """
        Assesses the difficulty level of the text.
        Basic implementation - could be enhanced with more sophisticated analysis.
        """
        words = text.split()
        avg_word_length = sum(len(word) for word in words) / len(words)

        if avg_word_length < 5:
            return "beginner"
        elif avg_word_length < 7:
            return "intermediate"
        else:
            return "advanced"


def generate_practice_lessons(
    vocab_list: List[str], translations: Dict[str, str]
) -> Dict:
    """
    Generates various types of practice exercises from vocabulary.
    """
    try:
        exercises = {
            "matching": {
                "type": "matching",
                "instructions": "Match the words with their translations",
                "words": vocab_list,
                "translations": [translations[word] for word in vocab_list],
            },
            "multiple_choice": {
                "type": "multiple_choice",
                "questions": [
                    {
                        "word": word,
                        "correct": translations[word],
                        "options": [
                            translations[word],
                            translations.get(
                                vocab_list[(i + 1) % len(vocab_list)], "Option"
                            ),
                            translations.get(
                                vocab_list[(i + 2) % len(vocab_list)], "Option"
                            ),
                        ],
                    }
                    for i, word in enumerate(vocab_list)
                ],
            },
            "fill_in_blanks": {
                "type": "fill_in_blanks",
                "instructions": "Fill in the missing words",
                "sentences": [
                    f"_____ means '{translations[word]}'" for word in vocab_list
                ],
                "answers": vocab_list,
            },
        }

        return exercises

    except Exception as e:
        return {"error": f"Error generating practice lessons: {str(e)}"}
