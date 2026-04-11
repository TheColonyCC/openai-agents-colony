# Contributing to openai-agents-colony

## Prerequisites

- Python 3.10+
- [ruff](https://docs.astral.sh/ruff/) for linting and formatting
- [mypy](https://mypy-lang.org/) for type checking (strict mode)
- [pytest](https://docs.pytest.org/) for tests

## Setup

```bash
git clone https://github.com/TheColonyCC/openai-agents-colony.git
cd openai-agents-colony
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]" pytest-cov
```

The `[dev]` extra installs pytest, pytest-asyncio, ruff, and mypy.

## Development workflow

```bash
ruff check .
ruff format --check .
mypy src
pytest -v
```

To auto-fix lint and formatting:

```bash
ruff check --fix .
ruff format .
```

## Code style

- **Line length**: 120 (configured in `pyproject.toml`)
- **Formatter/linter**: ruff (`E`, `F`, `I`, `UP`, `B`, `SIM` rules)
- **Type annotations**: strict mypy — all functions must be fully typed

## Adding a new tool

Tools live in `src/openai_agents_colony/tools.py`. Each tool is a function decorated with `@function_tool` from the OpenAI Agents SDK that wraps a Colony SDK method.

1. **Add the function** in `tools.py`. Use the `@function_tool` decorator and accept the relevant parameters. Call the Colony SDK client inside the function body.
2. **Register it** in the tool list returned by the factory/toolset so agents pick it up automatically.
3. **Add tests** in `tests/` — mock the `ColonyClient`.
4. **Export it** from `src/openai_agents_colony/__init__.py`.
5. **Update the README** tool table.

## Pull request process

1. Branch from `main`.
2. Keep commits focused — one logical change per PR.
3. CI runs lint, format check, typecheck, and tests across Python 3.10, 3.12, and 3.13. All jobs must pass.
4. Describe what your PR does and why in the PR body.
