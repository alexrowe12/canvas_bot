# canvas_bot

Ask Claude questions about your Canvas courses (what's due, grades, missing work,
announcements, syllabi, modules) through the [canvas-mcp](https://github.com/vishalsachdev/canvas-mcp)
MCP server, running locally with your own Canvas token.

The server runs in **student mode**: 48 tools, none of which can submit, post, or
message anything in Canvas. The only tool that writes anything is `download_course_file`,
which saves course files (e.g. PDFs from modules) to `downloads/` on this machine.

**Claude Code is the recommended client.** It can download a PDF and then read it from
disk. Claude Desktop can download files too, but it can only read them if you connect the
`downloads/` folder to the chat (＋ → Add folder).

## Setup

1. Install the server into a project virtualenv:

   ```bash
   python3 -m venv .venv
   .venv/bin/pip install canvas-mcp
   ```

2. Create `.env` in this folder (it is gitignored):

   ```bash
   CANVAS_API_TOKEN=<your token: Canvas → Account → Settings → New Access Token>
   CANVAS_API_URL=https://<your-school>.instructure.com/api/v1   # must end in /api/v1
   CANVAS_ROLE=student
   ALLOWED_WRITE_TOOLS=download_course_file
   ENABLE_DATA_ANONYMIZATION=false
   LOG_REDACT_PII=true
   ACCESSIBILITY_CHECKERS=none
   ```

3. Check the connection:

   ```bash
   .venv/bin/canvas-mcp-server --test
   ```

4. Add the server to Claude Desktop's config at
   `~/Library/Application Support/Claude/claude_desktop_config.json`, alongside any keys
   already there:

   ```json
   {
     "mcpServers": {
       "canvas": {
         "command": "/Users/alexrowe/Desktop/canvas_bot/.venv/bin/canvas-mcp-server"
       }
     }
   }
   ```

   Then fully quit Claude Desktop (⌘Q) and reopen it.

The server finds `.env` by searching upward from its install location, so it has to
stay in a `.venv` inside this folder. If you move the project, update the path in the
Claude Desktop config.

## Using it from Claude Code

`.mcp.json` registers the server for this project. Run `claude` in this folder, approve
the `canvas` server when prompted, and check it with `/mcp`. `CLAUDE.md` tells Claude to
save downloads to `downloads/` and read PDFs from there.

## Updating

```bash
.venv/bin/pip install --upgrade canvas-mcp
```

Then restart Claude Desktop.

## Allowing writes later (optional)

To let Claude mark planner items done or create planner notes, list those tools in
both `STUDENT_WRITE_TOOLS` and `ALLOWED_WRITE_TOOLS` in `.env`. See the
[env.template](https://github.com/vishalsachdev/canvas-mcp/blob/main/env.template) upstream.
Some of these write immediately without a confirmation step.

## Layout

- `.env` — Canvas credentials and server settings (not committed)
- `.venv/` — the installed server (not committed)
- `.mcp.json` — registers the server with Claude Code for this project
- `CLAUDE.md` — instructions for Claude (how to fetch and read course files)
- `downloads/` — files downloaded from Canvas (not committed)
- `archive/` — the original proof-of-concept scripts
