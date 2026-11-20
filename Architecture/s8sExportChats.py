#!/usr/bin/env python3
"""Refresh project chat transcripts from local Codex message records."""

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import tempfile
from zoneinfo import ZoneInfo


ARCHITECTURE = Path(__file__).resolve().parent
LEGACY = {
    "01a1c299-1c30-7eb0-bee5-c977ee11572f": (
        "Initialize Architecture project from…",
        "s8sChatLog-2026-11-19-project-initialization.md",
    ),
    "01a1db23-3229-73b2-bef8-a7cc517a5b84": (
        "Draft context description and drawing",
        "2026-11-14-context-description-and-drawing-chat.md",
    ),
    "01a1f06f-adec-7562-90b1-8b7d0c62da26": (
        "Create requirements branch",
        "2026-11-18-week-2-requirements-chat.md",
    ),
}
CONTEXT_PREFIXES = (
    "# AGENTS.md instructions for ",
    "<environment_context>",
    "<external_codex_apps_",
)


def read_records(path):
    """Ignore only an unfinished last record while the app is writing."""
    lines = path.read_bytes().splitlines(keepends=True)
    records = []
    for number, line in enumerate(lines):
        try:
            records.append(json.loads(line))
        except (json.JSONDecodeError, UnicodeDecodeError):
            if number == len(lines) - 1 and not line.endswith(b"\n"):
                break
            raise
    return records


def transcript(records, zone):
    messages = []
    for record in records:
        item = record.get("payload", {})
        if (record.get("type") != "response_item"
                or item.get("type") != "message"
                or item.get("role") not in ("user", "assistant")):
            continue
        blocks = item.get("content", [])
        body = "".join(block.get("text", "") for block in blocks)
        if item["role"] == "user" and body.startswith(CONTEXT_PREFIXES):
            continue
        if any("text" not in block for block in blocks):
            raise ValueError("Nontext message content requires an explicit attachment export")
        if not body:
            continue
        stamp = record.get("timestamp")
        if not stamp:
            raise ValueError("Missing message timestamp; refusing to invent one")
        parsed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("Message timestamp has no timezone")
        label = "User" if item["role"] == "user" else "Assistant"
        if item.get("phase") == "commentary":
            label += " (progress update)"
        messages.append((parsed.astimezone(zone), label, body))
    return messages


def export(path, destination, zone):
    records = read_records(path)
    meta = next((r["payload"] for r in records if r.get("type") == "session_meta"), None)
    if not meta or not meta.get("cwd"):
        return None
    cwd = Path(meta["cwd"]).resolve()
    if cwd != ARCHITECTURE.parent and not cwd.is_relative_to(ARCHITECTURE):
        return None
    ident = meta["id"]
    if not re.fullmatch(r"[0-9a-f-]{36}", ident):
        raise ValueError("Invalid chat ID")
    messages = transcript(records, zone)
    if not messages:
        return None
    title, filename = LEGACY.get(ident, (
        "SPE-800-Sensor conversation",
        f"s8sChatLog-{messages[0][0]:%Y-%m-%d}-{ident}.md",
    ))
    target = destination / filename
    preface = (
        f"# {title}\n\nChat ID: `{ident}`\n\n"
        "Timestamps are recorded message timestamps converted to America/New_York, "
        "with milliseconds and UTC offset. Message bodies are verbatim, including "
        "original whitespace and spelling. Includes user prompts, assistant progress "
        "updates, and final responses through the last recorded message. App-injected "
        "context, system/developer instructions, internal reasoning, and tool calls/results "
        "are omitted. Historical statements describe the state at the time.\n\n"
        f"Last included message: {messages[-1][0].isoformat(timespec='milliseconds')}. "
        "The active turn may still be in progress.\n\n"
        f"<!-- s8s-chat-messages: {len(messages)} -->\n\n"
    )
    pieces = [preface]
    spans = []
    offset = len(preface)
    for stamp, label, body in messages:
        heading = f"## {stamp.isoformat(timespec='milliseconds')} · {label}\n\n"
        offset += len(heading)
        spans.append((offset, offset + len(body), body))
        pieces.extend((heading, body, "\n\n"))
        offset += len(body) + 2
    result = "".join(pieces)
    if target.exists():
        old = target.read_text()
        count = re.search(r"<!-- s8s-chat-messages: (\d+) -->", old)
        if count and int(count[1]) > len(messages):
            raise ValueError(f"Refusing to shorten existing transcript: {target.name}")
        if old == result:
            return (target.name, len(messages), "unchanged")
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="",
                                     dir=destination, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(result)
    try:
        with temporary.open(encoding="utf-8", newline="") as stream:
            written = stream.read()
        for start, end, body in spans:
            if written[start:end] != body:
                raise ValueError("Export text differs from source message")
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)
    return (target.name, len(messages), "updated")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-dir", type=Path,
                        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")))
    parser.add_argument("--output", type=Path, default=ARCHITECTURE / "docs/chats")
    args = parser.parse_args()
    roots = [args.codex_dir / "sessions", args.codex_dir / "archived_sessions"]
    if not any(root.exists() for root in roots):
        parser.error("No local Codex session directories are available")
    failures = 0
    exported = 0
    zone = ZoneInfo("America/New_York")
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.jsonl")):
            try:
                outcome = export(path, args.output, zone)
                if outcome:
                    exported += 1
                    print(f"{outcome[2]}: {outcome[0]} ({outcome[1]} messages)")
            except (ValueError, KeyError, OSError) as error:
                failures += 1
                print(f"ERROR: {path.name}: {error}")
    print(f"{exported} project chats; {failures} errors")
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
