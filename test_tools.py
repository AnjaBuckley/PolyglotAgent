import asyncio
from src.tools.audio_tools import generate_audio
from src.tools.search_tools import web_search, find_youtube_video, get_song_lyrics


def test_tools():
    print("Testing Audio Generation:")
    result = generate_audio("Hallo, wie geht es dir?", "german")
    print(f"Audio file generated: {result}\n")

    print("Testing Web Search:")
    result = web_search("99 Luftballons song meaning")
    print(f"Search results: {result}\n")

    print("Testing YouTube Search:")
    result = find_youtube_video("99 Luftballons Nena")
    print(f"Video found: {result}\n")

    print("Testing Lyrics Search:")
    result = get_song_lyrics("99 Luftballons", "Nena")
    print(f"Lyrics: {result}\n")


if __name__ == "__main__":
    test_tools()
