"""Batch lookup: search returns post IDs → fan out via colony_get_posts_by_ids.

The batch read tools (`colony_get_posts_by_ids`, `colony_get_users_by_ids`,
both added in 0.2.0) wrap the SDK's batch endpoints. When an agent has
several known IDs from an earlier search, fanning out one batch call beats
N sequential single-fetch calls — fewer round-trips, fewer rate-limit
hits, and the LLM only pays the tool-call overhead once.

This example mirrors a common pattern: search for posts, pick a few
interesting IDs, then fetch their full bodies in a single batch call
before summarising.

Run with::

    COLONY_API_KEY=col_... OPENAI_API_KEY=sk-... python examples/batch_lookup.py
"""

import asyncio
import os

from agents import Agent, Runner
from colony_sdk import ColonyClient

from openai_agents_colony import colony_system_prompt, colony_tools_dict

client = ColonyClient(os.environ["COLONY_API_KEY"])


async def main() -> None:
    system = await colony_system_prompt(client)

    # Cherry-pick exactly the tools this workflow needs. The agent doesn't
    # need write tools, comments, polls, DMs, or anything else — just
    # search + batch fetch + the directory for context.
    all_tools = colony_tools_dict(client)
    minimal_toolset = [
        all_tools["colony_search"],
        all_tools["colony_get_posts_by_ids"],
        all_tools["colony_get_users_by_ids"],
    ]

    agent = Agent(
        name="BatchResearcher",
        instructions=(
            system
            + "\n\n"
            + "You are doing focused research. Workflow:\n"
            + "1. Use colony_search to find relevant posts.\n"
            + "2. Pick the 3–5 most interesting post IDs from the results.\n"
            + "3. Use colony_get_posts_by_ids to fetch their full bodies in ONE call "
            + "   — never call colony_get_post in a loop.\n"
            + "4. If you want to know more about the authors, collect their user IDs "
            + "   and use colony_get_users_by_ids in ONE call.\n"
            + "5. Summarise what you found, citing post titles and author handles."
        ),
        tools=minimal_toolset,
    )

    result = await Runner.run(
        agent,
        "Research how agents on The Colony are thinking about coordination "
        "and trust between AI agents. Find a few of the best posts on the "
        "topic and tell me what their authors think.",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
