import asyncio
from dotenv import load_dotenv
from agents.orchestrator import orchestrator


async def main():
    # Example usage
    test_requests = [
        "Can you find me a German song about Luftballons?",
        "Find me a German poem about nature",
        "Give me 10 German words about food",
    ]

    for request in test_requests:
        print(f"\nProcessing request: {request}")
        result = await Runner.run(orchestrator, input=request, max_turns=10)
        print(result.final_output)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
