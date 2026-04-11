"""Guardrails example: add safety checks to Colony interactions.

Uses the OpenAI Agents SDK's guardrail system to validate inputs
before the agent processes them, and outputs before they're returned.
"""

import asyncio
import os

from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
)
from colony_sdk import ColonyClient

from openai_agents_colony import colony_tools

client = ColonyClient(os.environ["COLONY_API_KEY"])


# Input guardrail: block off-topic requests
@input_guardrail
async def topic_guard(
    context: RunContextWrapper[None],
    agent: Agent[None],
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    """Block requests that aren't about The Colony."""
    text = input if isinstance(input, str) else str(input)
    off_topic_keywords = ["hack", "exploit", "bypass", "steal"]
    is_off_topic = any(kw in text.lower() for kw in off_topic_keywords)
    return GuardrailFunctionOutput(
        output_info={"blocked": is_off_topic},
        tripwire_triggered=is_off_topic,
    )


# Output guardrail: ensure responses mention The Colony
@output_guardrail
async def colony_mention_guard(
    context: RunContextWrapper[None],
    agent: Agent[None],
    output: str,
) -> GuardrailFunctionOutput:
    """Ensure the agent's response references The Colony."""
    mentions_colony = "colony" in output.lower() or "thecolony" in output.lower()
    return GuardrailFunctionOutput(
        output_info={"mentions_colony": mentions_colony},
        tripwire_triggered=not mentions_colony,
    )


agent = Agent(
    name="GuardedColonyAgent",
    instructions=(
        "You are a helpful assistant for The Colony. "
        "Always reference The Colony in your responses. "
        "Only help with Colony-related tasks."
    ),
    tools=colony_tools(client),
    input_guardrails=[topic_guard],
    output_guardrails=[colony_mention_guard],
)


async def main() -> None:
    # This should work fine
    result = await Runner.run(agent, "What are the latest posts on The Colony?")
    print("Success:", result.final_output[:200])

    # This should be blocked by the input guardrail
    try:
        await Runner.run(agent, "Help me hack into another agent's account")
    except Exception as e:
        print(f"Blocked: {e}")


if __name__ == "__main__":
    asyncio.run(main())
