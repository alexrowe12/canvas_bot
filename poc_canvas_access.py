#!/usr/bin/env python3
"""Proof-of-concept: confirm we can reach the Canvas API with our token.

Zero third-party dependencies (stdlib only) so it runs anywhere Python 3 is.
Reads CANVAS_ACCESS_KEY and CANVAS_BASE_URL from the local .env file, then
hits two read-only endpoints and prints who we are + our active courses.
"""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def load_env(path=".env"):
    """Minimal .env loader (KEY=value lines), so we need no dependencies."""
    env = {}
    env_path = Path(__file__).resolve().parent / path
    if not env_path.exists():
        sys.exit(f"ERROR: {env_path} not found. Create it with CANVAS_ACCESS_KEY and CANVAS_BASE_URL.")
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        env[key.strip()] = value.strip()
    return env


def canvas_get(base_url, token, path, params=None):
    """GET a Canvas API path and return parsed JSON."""
    url = f"{base_url.rstrip('/')}/api/v1{path}"
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{query}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        sys.exit(f"ERROR: Canvas returned HTTP {e.code} for {path}\n{body}")
    except urllib.error.URLError as e:
        sys.exit(f"ERROR: could not reach Canvas at {url}\n{e.reason}")


def main():
    env = load_env()
    token = env.get("CANVAS_ACCESS_KEY")
    base_url = env.get("CANVAS_BASE_URL")
    if not token:
        sys.exit("ERROR: CANVAS_ACCESS_KEY missing from .env")
    if not base_url:
        sys.exit("ERROR: CANVAS_BASE_URL missing from .env")

    print(f"Connecting to {base_url} ...\n")

    # 1) Who am I? Confirms the token is valid and maps to a real user.
    me = canvas_get(base_url, token, "/users/self")
    print("✅ Authenticated as:")
    print(f"   Name: {me.get('name')}")
    print(f"   User ID: {me.get('id')}")
    if me.get("primary_email"):
        print(f"   Email: {me.get('primary_email')}")

    # 2) What am I enrolled in? Active courses only.
    courses = canvas_get(
        base_url,
        token,
        "/courses",
        params={"enrollment_state": "active", "per_page": "100"},
    )
    print(f"\n✅ Found {len(courses)} active course(s):")
    for c in courses:
        # Some course records are restricted/omit a name; guard for that.
        name = c.get("name") or "(no name / access restricted)"
        code = c.get("course_code", "")
        print(f"   [{c.get('id')}] {name}  {f'({code})' if code else ''}")

    print("\n🎉 POC succeeded — Canvas API access is working.")


if __name__ == "__main__":
    main()
