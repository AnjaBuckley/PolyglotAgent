from duckduckgo_search import DDGS
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup


def web_search(query: str) -> str:
    """
    Performs a web search for the given query using DuckDuckGo.

    Args:
        query (str): Search query

    Returns:
        str: Search results summary
    """
    try:
        with DDGS() as ddgs:
            # Use ddgs.text() to get search results
            results = [r for r in ddgs.text(query, max_results=3)]

            if not results:
                return "No results found"

            # Format results, making sure to access the URL correctly
            formatted_results = []
            for result in results:
                formatted_results.append(
                    f"Title: {result.get('title', 'No title')}\n"
                    f"Content: {result.get('body', 'No content')}\n"
                    f"URL: {result.get('href', result.get('link', 'No link'))}\n"  # Try both 'href' and 'link'
                )

            return "\n\n".join(formatted_results)

    except Exception as e:
        return f"Error performing web search: {str(e)}"


def find_youtube_video(song_title: str) -> Dict:
    """
    Searches for a YouTube video matching the song title.

    Args:
        song_title (str): Title of the song to search for

    Returns:
        Dict: Video information including title, URL, and thumbnail
    """
    try:
        with DDGS() as ddgs:
            # Use ddgs.videos() to get video results
            videos = [
                v
                for v in ddgs.videos(
                    f"{song_title} official music video", max_results=1
                )
            ]

            if videos:
                video = videos[0]
                return {
                    "title": video.get("title", "No title"),
                    "url": video.get(
                        "href", video.get("link", "No link")
                    ),  # Try both 'href' and 'link'
                    "thumbnail": video.get(
                        "image", video.get("thumbnail", "No thumbnail")
                    ),  # Try both 'image' and 'thumbnail'
                    "duration": video.get("duration", "Unknown duration"),
                }
            else:
                return {"error": "No videos found"}

    except Exception as e:
        return {"error": f"Error finding video: {str(e)}"}


def get_song_lyrics(song_title: str, artist: str = "") -> str:
    """
    Attempts to find lyrics for a given song.

    Args:
        song_title (str): Title of the song
        artist (str, optional): Artist name

    Returns:
        str: Song lyrics or error message
    """
    try:
        search_query = f"{song_title} {artist} lyrics"
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(search_query, max_results=1)]

            if not results:
                return "No lyrics found"

            try:
                url = results[0].get(
                    "href", results[0].get("link")
                )  # Try both 'href' and 'link'
                if not url:
                    return "No valid URL found for lyrics"

                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")

                lyrics_containers = soup.find_all(
                    ["div", "p"],
                    class_=lambda x: x
                    and ("lyrics" in x.lower() or "text" in x.lower()),
                )

                if lyrics_containers:
                    lyrics = lyrics_containers[0].get_text(strip=True)
                    return lyrics

                return "Lyrics not found on the page"

            except requests.RequestException as e:
                return f"Error accessing lyrics page: {str(e)}"

    except Exception as e:
        return f"Error fetching lyrics: {str(e)}"
