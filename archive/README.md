# Archive

Original proof-of-concept scripts, kept for reference. They are superseded by the
Canvas MCP server setup in the project root (see `../README.md`).

- `poc_canvas_access.py` — checked Canvas API access with a personal token (stdlib only).
  Note: it reads the old `CANVAS_ACCESS_KEY` / `CANVAS_BASE_URL` names, which `.env` no longer uses.
- `poc_github_access.py` — checked GitHub issue + Projects V2 access via the `gh` CLI.
