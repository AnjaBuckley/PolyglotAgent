import asyncio
from dotenv import load_dotenv
import os
from openai import OpenAI


async def test_agent():
    client = OpenAI()

    # Test with one request
    request = "Can you find a german poem about love?"

    print("\n📝 Testing with request:", request)

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """
                You are a helpful language learning assistant. When users ask about:
                - Songs: Find and explain lyrics
                - Poems: Provide and analyze poems
                - Vocabulary: Give relevant word lists with translations
                Always include translations and explanations.
                """,
                },
                {"role": "user", "content": request},
            ],
        )
        print("\n🤖 Agent Response:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: Please set your OPENAI_API_KEY in the .env file")
        exit(1)

    print("🚀 Starting Language Learning Agent Test...")
    asyncio.run(test_agent())
