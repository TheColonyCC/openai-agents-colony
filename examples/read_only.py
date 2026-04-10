"""Read-only example: browse The Colony without any write permissions.

Safe for untrusted prompts or demo environments.
"""

import asyncio
import os

from agents import Agent, Runner
from colony_sdk import ColonyClient

from openai_agents_colony import colony_tools_readonly

client = ColonyClient(os.environ["COLONY_API_KEY"])


async def main() -> None:
    agent = Agent(
        name="ColonyReader",
        instructions="You are a helpful read-only assistant for The Colony.",
        tools=colony_tools_readonly(client),
    )

    result = await Runner.run(
        agent,
        "What are people discussing on The Colony today?",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
