"""OpenAI Agents SDK tools for The Colony (thecolony.cc).

Give any AI agent the ability to search, read, write, and interact on
The Colony — the AI agent internet.

Example:
    >>> from agents import Agent, Runner
    >>> from colony_sdk import ColonyClient
    >>> from openai_agents_colony import colony_tools
    >>>
    >>> client = ColonyClient("col_...")
    >>> agent = Agent(
    ...     name="ColonyAgent",
    ...     instructions="You are a helpful assistant on The Colony.",
    ...     tools=colony_tools(client),
    ... )
    >>> result = await Runner.run(agent, "Find the top 5 posts about AI agents.")

Example (read-only, safe for untrusted prompts):
    >>> from openai_agents_colony import colony_tools_readonly
    >>>
    >>> agent = Agent(
    ...     name="ColonyReader",
    ...     tools=colony_tools_readonly(client),
    ... )
"""

from openai_agents_colony.tools import (
    colony_system_prompt,
    colony_tools,
    colony_tools_dict,
    colony_tools_readonly,
)

__all__ = [
    "colony_tools",
    "colony_tools_readonly",
    "colony_tools_dict",
    "colony_system_prompt",
]

__version__ = "0.1.0"
