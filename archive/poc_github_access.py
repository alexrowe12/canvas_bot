#!/usr/bin/env python3
"""Proof-of-concept: confirm we can reach GitHub course data via the `gh` CLI.

We shell out to `gh` (already installed + authenticated via keyring), so there's
no separate token to manage here. Pulls the two things the study bot cares about:
  1. Open issues in the course repo that are assigned to us.
  2. Kanban board (Projects V2) items assigned to us, with their column status.

Projects V2 boards are GraphQL-only (not in GitHub's REST API), which is exactly
why `gh` is the right tool — it handles both.
"""

import json
import subprocess
import sys

# --- Course config -----------------------------------------------------------
ORG = "Hawk-Center"
REPO = "Hawk-Center/st-alex-rowe"
PROJECT_NUMBER = 6
ME = "alexrowe12"
# -----------------------------------------------------------------------------


def gh_json(args):
    """Run a `gh` command that emits JSON and return the parsed result."""
    try:
        out = subprocess.run(
            ["gh", *args],
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError:
        sys.exit("ERROR: `gh` CLI not found. Install with `brew install gh`.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"ERROR: `gh {' '.join(args)}` failed:\n{e.stderr.strip()}")
    return json.loads(out.stdout)


def main():
    print(f"Fetching GitHub course data as {ME} ...\n")

    # 1) Open issues assigned to us in the course repo.
    issues = gh_json([
        "issue", "list",
        "--repo", REPO,
        "--assignee", ME,
        "--state", "open",
        "--json", "number,title,labels,url",
        "--limit", "100",
    ])
    print(f"✅ Open issues assigned to me in {REPO}: {len(issues)}")
    for i in issues:
        labels = ", ".join(l["name"] for l in i.get("labels", []))
        print(f"   #{i['number']}  {i['title']}" + (f"  [{labels}]" if labels else ""))

    # 2) Kanban board items assigned to us (Projects V2 → GraphQL under the hood).
    board = gh_json([
        "project", "item-list", str(PROJECT_NUMBER),
        "--owner", ORG,
        "--format", "json",
        "--limit", "500",
    ])
    all_items = board.get("items", [])
    mine = [it for it in all_items if ME in (it.get("assignees") or [])]
    print(f"\n✅ Kanban board (project #{PROJECT_NUMBER}) items assigned to me: "
          f"{len(mine)} of {len(all_items)} total")
    for it in mine:
        print(f"   [{it.get('status', 'No status')}] {it.get('title', '(untitled)')}")

    print("\n🎉 POC succeeded — GitHub course access is working.")


if __name__ == "__main__":
    main()
