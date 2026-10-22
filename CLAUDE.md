# canvas_bot

A study assistant over Canvas LMS, using the `canvas` MCP server (canvas-mcp, see `README.md`).
The server runs in student mode: it can read Canvas but never submit, post, or message.

## Reading Canvas files (PDFs, slides, etc.)

- Don't use `read_course_file`. It returns the whole file as base64, which is unreadable and
  overflows context even for small PDFs.
- Use `download_course_file` with `save_directory` set to
  `/Users/alexrowe/Desktop/canvas_bot/downloads`, then open the file from disk with the Read tool
  (it handles PDFs; pass `pages` for long ones).
- Find file IDs with `get_course_structure` or `list_module_items`: a module item of type `File`
  has the file ID in `content_id`. `list_course_files` may return "unauthorized" when an instructor
  hides the course Files tab, but files linked from modules still download.
- The tool refuses to overwrite. If the file is already in `downloads/`, read the existing copy.
