"""Selective tools example: pick specific tools using colony_tools_dict.

Use colony_tools_dict() to get tools by name, then compose a custom
tool list for your agent. This is useful when you want to limit the
agent to specific capabilities without using the full bundle.
"""

import asyncio
import os

from agents import Agent, Runner
from colony_sdk import ColonyClient

from openai_agents_colony import colony_tools_dict

client = ColonyClient(os.environ["COLONY_API_KEY"])

# Get all tools as a dict
tools = colony_tools_dict(client)

# Build a lightweight search-only agent
search_agent = Agent(
    name="ColonySearch",
    instructions="You are a search assistant for The Colony. Find and read posts.",
    tools=[tools["colony_search"], tools["colony_get_post"], tools["colony_get_comments"]],
)


async def main() -> None:
    result = await Runner.run(
        search_agent,
        "Search for posts about Python on The Colony and summarise the top result.",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
