from typing import Dict, Optional
from src.tools.validation_tools import analyze_language_confidence
from src.tools.content_tools import ContentCreator, generate_practice_lessons
from src.tools.audio_tools import generate_audio
from src.tools.search_tools import web_search, find_youtube_video, get_song_lyrics


class LanguageLearningAssistant:
    def __init__(self):
        self.content_creator = ContentCreator()

    async def process_request(
        self, user_request: str, native_language: str = "en"
    ) -> Dict:
        """
        Main decision-making method that determines which tools to use based on the request.
        """
        try:
            # STEP 1: Validation Tool
            validation = analyze_language_confidence(user_request)

            if not validation["is_language_question"]:
                return {
                    "status": "error",
                    "message": "Please ask a language-related question.",
                }

            # STEP 2: Language Detection
            target_language = (
                validation["detected_languages"][0]
                if validation["detected_languages"]
                else None
            )
            if not target_language:
                return {
                    "status": "error",
                    "message": "Please specify which language you want to learn about.",
                }

            # STEP 3: Audio Request Detection
            wants_audio = any(
                word in user_request.lower()
                for word in [
                    "pronounce",
                    "pronunciation",
                    "say",
                    "speak",
                    "audio",
                    "sound",
                ]
            )

            # STEP 4: Request Type Classification and Tool Selection
            if "song" in user_request.lower():
                # Uses: search_tools (web_search, find_youtube_video, get_song_lyrics)
                #       content_tools (for translation)
                #       audio_tools (if requested)
                return await self._handle_song_request(
                    user_request, target_language, native_language, wants_audio
                )

            elif "poem" in user_request.lower():
                # Uses: search_tools (web_search)
                #       content_tools (for translation)
                #       audio_tools (if requested)
                return await self._handle_poem_request(
                    user_request, target_language, native_language, wants_audio
                )

            elif any(
                word in user_request.lower()
                for word in ["vocabulary", "words", "vocab"]
            ):
                # Uses: content_tools (for vocabulary and translation)
                #       audio_tools (if requested)
                return await self._handle_vocabulary_request(
                    user_request, target_language, native_language, wants_audio
                )

            else:
                # Uses: content_tools (for translation)
                #       audio_tools (if requested)
                return await self._handle_general_translation_request(
                    user_request, target_language, native_language, wants_audio
                )

        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {str(e)}"}

    async def _handle_song_request(
        self,
        request: str,
        target_language: str,
        native_language: str,
        wants_audio: bool,
    ) -> Dict:
        """Handle requests for songs"""
        # Search for song
        search_results = web_search(f"popular {target_language} song lyrics")

        # Find video
        video_info = find_youtube_video(
            search_results.split("\n")[0]
        )  # Use first search result

        # Get lyrics
        lyrics = get_song_lyrics(search_results.split("\n")[0])

        # Create learning content from lyrics
        content = self.content_creator.create_learning_content(
            text=lyrics,
            target_language=target_language,
            native_language=native_language,
        )

        result = {
            "status": "success",
            "type": "song",
            "content": content,
            "video": video_info,
        }

        # Only generate audio if requested
        if wants_audio:
            vocab_audio = {}
            for word in content["vocabulary"]["words"]:
                audio_path = generate_audio(word, target_language)
                vocab_audio[word] = audio_path
            result["vocabulary_audio"] = vocab_audio

        # Generate practice exercises
        exercises = generate_practice_lessons(
            content["vocabulary"]["words"], content["vocabulary"]["translations"]
        )
        result["exercises"] = exercises

        return result

    async def _handle_poem_request(
        self,
        request: str,
        target_language: str,
        native_language: str,
        wants_audio: bool,
    ) -> Dict:
        """Handle requests for poems"""
        # Search for poem
        search_results = web_search(f"famous {target_language} poem")

        # Create learning content
        content = self.content_creator.create_learning_content(
            text=search_results.split("\n")[0],  # Use first search result
            target_language=target_language,
            native_language=native_language,
        )

        result = {
            "status": "success",
            "type": "poem",
            "content": content,
        }

        # Only generate audio if requested
        if wants_audio:
            vocab_audio = {}
            for word in content["vocabulary"]["words"]:
                audio_path = generate_audio(word, target_language)
                vocab_audio[word] = audio_path
            result["vocabulary_audio"] = vocab_audio

        # Generate practice exercises
        exercises = generate_practice_lessons(
            content["vocabulary"]["words"], content["vocabulary"]["translations"]
        )
        result["exercises"] = exercises

        return result

    async def _handle_vocabulary_request(
        self,
        request: str,
        target_language: str,
        native_language: str,
        wants_audio: bool,
    ) -> Dict:
        """Handle requests for vocabulary"""
        # Extract topic if specified
        topic = (
            request.lower().split("about")[-1].strip()
            if "about" in request.lower()
            else "common words"
        )

        # Search for vocabulary
        search_results = web_search(f"{target_language} vocabulary {topic}")

        # Create learning content
        content = self.content_creator.create_learning_content(
            text=search_results,
            target_language=target_language,
            native_language=native_language,
        )

        result = {
            "status": "success",
            "type": "vocabulary",
            "content": content,
        }

        # Only generate audio if requested
        if wants_audio:
            vocab_audio = {}
            for word in content["vocabulary"]["words"]:
                audio_path = generate_audio(word, target_language)
                vocab_audio[word] = audio_path
            result["vocabulary_audio"] = vocab_audio

        # Generate practice exercises
        exercises = generate_practice_lessons(
            content["vocabulary"]["words"], content["vocabulary"]["translations"]
        )
        result["exercises"] = exercises

        return result

    async def _handle_general_translation_request(
        self,
        request: str,
        target_language: str,
        native_language: str,
        wants_audio: bool,
    ) -> Dict:
        """Handle general translation/learning requests"""
        # Extract the text to translate
        text_to_translate = request.split("'")[1] if "'" in request else request

        # Create learning content
        content = self.content_creator.create_learning_content(
            text=text_to_translate,
            target_language=target_language,
            native_language=native_language,
        )

        result = {
            "status": "success",
            "type": "translation",
            "content": content,
        }

        # Only generate audio if requested
        if wants_audio:
            audio_path = generate_audio(text_to_translate, target_language)
            result["audio"] = audio_path

        return result
