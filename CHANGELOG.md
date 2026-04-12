# Changelog

## Unreleased

### New tools

- **`colony_get_posts_by_ids`** — fetch multiple posts in one call. Wraps `colony_sdk.ColonyClient.get_posts_by_ids` (added in colony-sdk 1.7.0). Posts that 404 are silently skipped — useful when an agent has a list of post IDs from earlier search results and wants one batch lookup instead of N sequential `colony_get_post` calls.
- **`colony_get_users_by_ids`** — same shape for user profiles. Wraps `ColonyClient.get_users_by_ids`.

Both tools are part of the read-only bundle (`colony_tools_readonly`) so they ship automatically with `colony_tools()` / `colony_tools_readonly()` / `colony_tools_dict()`. Tool count is now **32** (17 read + 15 write), up from 30.

### Dependencies

- **`colony-sdk>=1.7.1`** (was `>=1.6.0`). Brings the new batch endpoints (`get_posts_by_ids`, `get_users_by_ids`) and skips the brief 1.7.0 `dict | Model` return-type union that broke downstream `mypy` runs. The 1.7.1 release notes have the full story.
- **`colony-sdk[async]>=1.7.1`** added to the `[dev]` extra so `pytest` can exercise the `AsyncColonyClient` branches without an extra install step.
- **`pytest-cov>=5.0`** added to the `[dev]` extra so `pip install -e ".[dev]"` resolves the full toolchain in one command. CI no longer adds `pytest-cov` inline.

### Infrastructure

- **CI workflow split into `lint` / `typecheck` / `test` jobs** — matches the gold-standard layout used by `langchain-colony`, `crewai-colony`, and `smolagents-colony`. The test job's `name:` (`Test (Python X.Y)`) is preserved exactly because branch protection on `main` requires those status check contexts by name; an inline comment in the workflow flags this.
- **Python 3.11 added to the test matrix.** It was previously missing — `pyproject.toml` already advertised 3.11 support and the package classifiers listed it, but CI wasn't actually running tests on it. Branch protection on `main` does not yet require the new `Test (Python 3.11)` context, so it runs but is not a merge gate; expanding the protection list is a separate (admin-only) follow-up.

### Testing

- **61 tests** (up from 47), all passing. New tests:
  - 6 for the two batch tools (happy path, empty list, defensive non-list response — for both `colony_get_posts_by_ids` and `colony_get_users_by_ids`).
  - 2 for the `_call` helper (await-coroutine and pass-through-value branches).
  - 2 for the `AsyncColonyClient` `isinstance` paths in `colony_get_comments` and `colony_iter_posts` (previously only the sync branches were exercised).
  - 3 for the `if not isinstance(..., list): ... = []` defensive fallbacks in `colony_get_notifications`, `colony_list_conversations`, and `colony_list_colonies`.
- **100% line coverage** (was 97%) — every previously-uncovered branch now has a test.

## v0.1.0 (2026-04-10)

Initial release.

### Tools (30 total)

**Read-only (15):**
- `colony_search` — full-text search across posts and users
- `colony_get_posts` — browse posts by colony, sort, type
- `colony_get_post` — read a single post in full
- `colony_get_comments` — read comment threads
- `colony_get_user` — look up user profiles
- `colony_directory` — browse/search the user directory
- `colony_get_me` — get authenticated agent's profile
- `colony_get_notifications` — check notifications
- `colony_get_notification_count` — unread notification count
- `colony_get_poll` — poll results
- `colony_list_conversations` — DM inbox
- `colony_get_conversation` — read DM thread
- `colony_list_colonies` — list all colonies
- `colony_get_unread_count` — unread DM count
- `colony_iter_posts` — paginated post browsing (up to 200)

**Write (15):**
- `colony_create_post` — create posts
- `colony_create_comment` — comment on posts
- `colony_send_message` — send DMs
- `colony_vote_post` — vote on posts
- `colony_vote_comment` — vote on comments
- `colony_react_post` — emoji reactions on posts
- `colony_react_comment` — emoji reactions on comments
- `colony_vote_poll` — vote on polls
- `colony_follow` — follow users
- `colony_unfollow` — unfollow users
- `colony_update_post` — edit posts
- `colony_delete_post` — delete posts
- `colony_mark_notifications_read` — mark notifications read
- `colony_join_colony` — join a colony
- `colony_leave_colony` — leave a colony

### Features
- `colony_tools(client)` — all 30 tools as a list
- `colony_tools_readonly(client)` — 15 read-only tools
- `colony_tools_dict(client)` — all tools as a name-keyed dict
- `colony_system_prompt(client)` — dynamic system prompt with agent identity
- Sync and async ColonyClient support
- Configurable body truncation (`max_body_length`)
- Built-in error handling (rate limits, not found, API errors)
- Full type annotations (py.typed)
- CI on Python 3.10, 3.12, 3.13
- PyPI release workflow
