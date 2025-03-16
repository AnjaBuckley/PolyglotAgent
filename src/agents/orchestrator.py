from agents import Agent
from ..tools.audio_tools import generate_audio
from ..tools.content_tools import create_learning_content, generate_practice_lessons
from ..tools.search_tools import web_search, find_youtube_video
from ..tools.validation_tools import analyze_language_confidence

orchestrator = Agent(
    name="Language Learning Orchestrator",
    instructions="""
    You are a language learning assistant that helps students learn languages.
    Before processing any request:
    1. First use analyze_language_confidence to verify the request is language-learning related
    2. Only proceed if confidence score >= 0.8
    
    For song requests:
    - Use web_search to find lyrics
    - Use create_learning_content for translation and vocabulary
    - Use generate_audio for vocabulary pronunciation
    - Use find_youtube_video for the song
    - Use generate_practice_lessons for exercises
    
    For poem requests:
    - Use web_search to find the poem
    - Use create_learning_content for translation and vocabulary
    - Use generate_audio for vocabulary pronunciation
    - Use generate_practice_lessons for exercises
    
    For vocabulary requests:
    - Use generate_audio directly
    - Use generate_practice_lessons for exercises
    
    Always ensure appropriate tools are called based on the request type.
    """,
    tools=[
        analyze_language_confidence,
        web_search,
        generate_audio,
        find_youtube_video,
        generate_practice_lessons,
        create_learning_content,
    ],
)
