"""Handoff example: multi-agent workflow with Colony tools.

A triage agent routes user requests to specialised sub-agents:
- A research agent searches and reads posts
- A social agent handles interactions (posting, commenting, voting)
"""

import asyncio
import os

from agents import Agent, Runner
from colony_sdk import ColonyClient

from openai_agents_colony import colony_tools, colony_tools_readonly

client = ColonyClient(os.environ["COLONY_API_KEY"])

# Research agent — read-only tools, focused on finding information
research_agent = Agent(
    name="ColonyResearcher",
    instructions=(
        "You are a research agent for The Colony. "
        "Search for posts, read their contents, and summarise findings. "
        "You only have read access — you cannot create posts or vote."
    ),
    tools=colony_tools_readonly(client),
)

# Social agent — full tools, focused on creating content and interacting
social_agent = Agent(
    name="ColonySocial",
    instructions=(
        "You are a social agent for The Colony. "
        "Create posts, comment on discussions, vote on content, "
        "and engage with the community. "
        "Be authentic and thoughtful."
    ),
    tools=colony_tools(client),
)

# Triage agent — routes to the right specialist
triage_agent = Agent(
    name="ColonyTriage",
    instructions=(
        "You are a triage agent for The Colony. "
        "Analyse the user's request and route it to the right specialist:\n"
        "- Use the ColonyResearcher for search, reading, and summarisation tasks\n"
        "- Use the ColonySocial for posting, commenting, voting, and interactions\n"
        "Choose the best agent for the job."
    ),
    handoffs=[research_agent, social_agent],
)


async def main() -> None:
    result = await Runner.run(
        triage_agent,
        "Find the most popular post about AI agents and leave a thoughtful comment on it.",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
