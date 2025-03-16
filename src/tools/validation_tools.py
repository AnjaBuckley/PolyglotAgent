from typing import Dict
from langdetect import detect, detect_langs
import re


def analyze_language_confidence(text: str) -> Dict:
    """
    Analyzes the input text to determine if it's a language learning request
    and calculates confidence score.

    Args:
        text: Input text to analyze

    Returns:
        Dict containing analysis results
    """
    try:
        # Common greetings and phrases in different languages
        common_phrases = {
            "guten tag": "de",
            "guten morgen": "de",
            "wie geht": "de",
            "buenos días": "es",
            "cómo estás": "es",
            "bonjour": "fr",
            "comment allez": "fr",
            "ciao": "it",
            "come stai": "it",
        }

        # Language learning keywords with weights
        language_keywords = {
            "translate": 0.4,
            "meaning": 0.4,
            "say": 0.3,
            "speak": 0.3,
            "learn": 0.3,
            "word": 0.3,
            "phrase": 0.3,
            "language": 0.3,
            "vocabulary": 0.4,
            "grammar": 0.4,
            "pronunciation": 0.4,
            "deutsch": 0.4,
            "español": 0.4,
            "français": 0.4,
            "italiano": 0.4,
            "bedeutet": 0.4,  # German for "means"
            "dice": 0.3,  # Spanish for "say"
            "parle": 0.3,  # French for "speak"
            "song": 0.3,
            "poem": 0.3,
            "music": 0.3,
            "lyrics": 0.3,
            "find": 0.2,  # Common with song/poem requests
            "german": 0.3,
            "deutsche": "de",
            "auf deutsch": "de",
            "spanish": 0.3,
            "en español": "es",
            "french": 0.3,
            "francais": "fr",
            "english": "en",
            "englisch": "en",
            "inglés": "en",
            "italienne": "it",
        }

        text_lower = text.lower()

        # Initialize confidence components
        keyword_score = 0.0
        question_score = 0.0
        language_score = 0.0

        # Check for common phrases
        for phrase, lang in common_phrases.items():
            if phrase in text_lower:
                language_score = max(language_score, 0.3)

        # Check for language learning keywords with weights
        for keyword, weight in language_keywords.items():
            if keyword in text_lower:
                keyword_score += weight
        keyword_score = min(0.4, keyword_score)  # Cap at 0.4

        # Cultural content patterns (songs, poems)
        cultural_patterns = [
            r"find .*(song|poem|music)",
            r"(song|poem|music) .*(in|about)",
            r"teach me .*(song|poem)",
            r"learn .*(song|poem)",
        ]

        if any(re.search(pattern, text_lower) for pattern in cultural_patterns):
            keyword_score = max(keyword_score, 0.3)
            question_score = 0.3

        # Enhanced question detection for language learning
        question_patterns = [
            r"how.+say",
            r"what.+mean",
            r"translate",
            r"bedeutet",  # German
            r"¿cómo se dice",  # Spanish
            r"comment dit-on",  # French
            r"was heißt",  # German
        ]

        is_question = "?" in text or any(
            re.search(pattern, text_lower) for pattern in question_patterns
        )

        if is_question:
            # Add question score if it seems language-related
            if keyword_score > 0 or any(
                word in text_lower for word in ["in", "to", "from", "auf", "en", "auf"]
            ):
                question_score = 0.3

        # Detect mentioned languages with common variations
        common_languages = {
            "german": "de",
            "deutsch": "de",
            "deutsche": "de",
            "auf deutsch": "de",
            "spanish": "es",
            "español": "es",
            "espanol": "es",
            "en español": "es",
            "french": "fr",
            "français": "fr",
            "francais": "fr",
            "en français": "fr",
            "english": "en",
            "englisch": "en",
            "inglés": "en",
            "italian": "it",
            "italiano": "it",
            "italienne": "it",
        }

        mentioned_languages = []
        for lang, code in common_languages.items():
            if lang in text_lower:
                mentioned_languages.append(code)
                language_score = max(language_score, 0.4)

        # Detect foreign language text
        try:
            if len(text.strip()) > 3:  # Ignore very short texts
                detected_langs = detect_langs(text)
                foreign_langs = [
                    lang
                    for lang in detected_langs
                    if lang.lang != "en" and lang.prob > 0.5
                ]

                if foreign_langs:
                    # Only add high-probability languages
                    for lang in foreign_langs:
                        if lang.prob > 0.8:  # Increased threshold
                            language_score = max(language_score, 0.4)
                            mentioned_languages.append(lang.lang)
        except:
            pass

        # Boost score for clear language learning patterns
        if (
            ("how" in text_lower and "say" in text_lower)
            or ("what" in text_lower and "mean" in text_lower)
            or ("translate" in text_lower)
            or ("bedeutet" in text_lower)
            or ("¿cómo se dice" in text_lower)
        ):
            keyword_score = max(keyword_score, 0.4)
            question_score = 0.3

        # Calculate final confidence score
        confidence_score = keyword_score + question_score + language_score

        # Additional checks for false positives
        if len(text.strip()) < 2:  # Very short input
            confidence_score = 0.0
        elif len(set(text)) < 3:  # Repeated characters
            confidence_score = 0.0
        elif not any(c.isalpha() for c in text):  # No letters
            confidence_score = 0.0
        elif (
            len(text.split()) < 2 and "?" not in text
        ):  # Single word without question mark
            confidence_score = min(confidence_score, 0.3)

        # Reduce score for non-language learning content
        non_language_patterns = [
            r"joke",
            r"weather",
            r"time",
            r"pizza",
            r"order",
        ]
        if any(re.search(pattern, text_lower) for pattern in non_language_patterns):
            confidence_score = min(confidence_score, 0.3)

        # Round the confidence score
        confidence_score = round(min(1.0, confidence_score), 2)

        # If it's a cultural request (song/poem) with a language, boost the score
        if ("song" in text_lower or "poem" in text_lower) and mentioned_languages:
            confidence_score = max(confidence_score, 0.8)

        return {
            "is_language_question": confidence_score >= 0.8,
            "confidence_score": confidence_score,
            "detected_languages": list(set(mentioned_languages)),
            "analysis": {
                "has_question": is_question,
                "keyword_matches": sum(1 for k in language_keywords if k in text_lower),
                "foreign_text_detected": bool(mentioned_languages),
                "keyword_score": round(keyword_score, 2),
                "question_score": round(question_score, 2),
                "language_score": round(language_score, 2),
                "is_cultural_request": "song" in text_lower or "poem" in text_lower,
            },
        }

    except Exception as e:
        return {"is_language_question": False, "confidence_score": 0.0, "error": str(e)}
