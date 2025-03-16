import asyncio
from dotenv import load_dotenv
import os
from openai_agents import Agent, Runner


async def try_agent():
    # First create the agent
    agent = Agent(
        name="Language Learning Assistant",
        instructions="""
        You are a language learning assistant that helps students learn languages.
        For song requests: Find lyrics and provide translations.
        For poem requests: Find poems and provide analysis.
        For vocabulary requests: Provide relevant vocabulary lists.
        """,
    )

    # Example requests to test
    requests = [
        "Can you find me a German song about Luftballons?",
        "Find me a German poem about nature",
        "Give me 10 German words about food",
        "What's the weather like?",  # This should trigger the confidence check failure
    ]

    print("🤖 Language Learning Agent Demo\n")

    for request in requests:
        print("\n" + "=" * 50)
        print(f"📝 User Request: {request}")
        print("=" * 50)

        try:
            result = await Runner.run(agent, input=request, max_turns=10)
            print(f"\n🤖 Agent Response:\n{result.final_output}")
        except Exception as e:
            print(f"\n❌ Error occurred: {str(e)}")


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set your OPENAI_API_KEY in the .env file")
        exit(1)

    print("🚀 Starting Language Learning Agent...")
    asyncio.run(try_agent())
