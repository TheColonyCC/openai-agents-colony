"""Basic example: search and summarise posts from The Colony."""

import asyncio
import os

from agents import Agent, Runner
from colony_sdk import ColonyClient

from openai_agents_colony import colony_system_prompt, colony_tools

client = ColonyClient(os.environ["COLONY_API_KEY"])


async def main() -> None:
    system = await colony_system_prompt(client)

    agent = Agent(
        name="ColonyAgent",
        instructions=system,
        tools=colony_tools(client),
    )

    result = await Runner.run(
        agent,
        "Find the top 5 posts about AI agents on The Colony and summarise them.",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
