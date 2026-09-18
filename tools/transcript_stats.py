#!/usr/bin/env python3
"""Stream the memories gateway export and write anonymized stats.

Never prints or writes message content, reasoning, titles, cwds, or names.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import sys
from pathlib import Path


def utc(ts) -> str:
    try:
        return dt.datetime.fromtimestamp(float(ts), dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
    except (TypeError, ValueError, OSError):
        return "unknown"


def median(nums: list[int]) -> int:
    if not nums:
        return 0
    s = sorted(nums)
    return s[len(s) // 2]


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line_no, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                yield {"__bad__": True, "__line__": line_no}


def resolve_conversations(memories: Path | None, conversations: Path | None) -> Path:
    if conversations:
        return conversations
    if memories:
        return memories / "hades-v2" / "conversations"
    here = Path(__file__).resolve()
    sibling = here.parents[2] / "hades-v2-memories" / "hades-v2" / "conversations"
    return sibling


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--memories", type=Path, help="Path to hades-v2-memories clone")
    p.add_argument(
        "--conversations",
        type=Path,
        help="Path to conversations/ (overrides --memories)",
    )
    p.add_argument("--out", type=Path, default=Path("docs/transcripts-stats.md"))
    p.add_argument("--out-stats", type=Path, help="Alias for --out")
    p.add_argument("--out-schema", type=Path, default=Path("docs/transcripts-schema.md"))
    p.add_argument("--max-message-files", type=int, default=0, help="0 = all shards")
    args = p.parse_args()

    out_stats = args.out_stats or args.out
    conv = resolve_conversations(args.memories, args.conversations)
    sessions_path = conv / "sessions.jsonl"
    if not sessions_path.is_file():
        print(f"missing {sessions_path}", file=sys.stderr)
        return 1

    sources = collections.Counter()
    models = collections.Counter()
    end_reasons = collections.Counter()
    chat_types = collections.Counter()
    user_id_set = collections.Counter()
    msg_counts: list[int] = []
    tool_counts: list[int] = []
    starts: list[float] = []
    ends: list[float] = []
    session_keys: set[str] = set()
    session_field_keys: set[str] = set()
    n_sessions = 0
    n_session_bad = 0
    titles_nonempty = 0

    for row in iter_jsonl(sessions_path):
        if row.get("__bad__"):
            n_session_bad += 1
            continue
        n_sessions += 1
        session_field_keys.update(row.keys())
        sid = row.get("id")
        if sid:
            session_keys.add(str(sid))
        sources[str(row.get("source") or "null")] += 1
        models[str(row.get("model") or "null")] += 1
        end_reasons[str(row.get("end_reason") or "null")] += 1
        chat_types[str(row.get("chat_type") or "null")] += 1
        user_id_set["set" if row.get("user_id") else "null"] += 1
        msg_counts.append(int(row.get("message_count") or 0))
        tool_counts.append(int(row.get("tool_call_count") or 0))
        if row.get("title"):
            titles_nonempty += 1
        if row.get("started_at") is not None:
            try:
                starts.append(float(row["started_at"]))
            except (TypeError, ValueError):
                pass
        if row.get("ended_at") is not None:
            try:
                ends.append(float(row["ended_at"]))
            except (TypeError, ValueError):
                pass

    shards = sorted(conv.glob("messages-*.jsonl"))
    if args.max_message_files:
        shards = shards[: args.max_message_files]

    roles = collections.Counter()
    finishes = collections.Counter()
    n_msg = 0
    n_msg_bad = 0
    n_with_reasoning = 0
    n_with_tools = 0
    content_lens: list[int] = []
    msg_sessions: set[str] = set()
    msg_field_keys: set[str] = set()
    shard_rows: list[tuple[str, int]] = []

    for shard in shards:
        count = 0
        for row in iter_jsonl(shard):
            if row.get("__bad__"):
                n_msg_bad += 1
                continue
            n_msg += 1
            count += 1
            msg_field_keys.update(k for k in row.keys() if not k.startswith("__"))
            roles[str(row.get("role") or "null")] += 1
            finishes[str(row.get("finish_reason") or "null")] += 1
            if row.get("reasoning") or row.get("reasoning_content"):
                n_with_reasoning += 1
            if row.get("tool_calls") or row.get("tool_name"):
                n_with_tools += 1
            content = row.get("content")
            if isinstance(content, str):
                content_lens.append(len(content))
            sid = row.get("session_id")
            if sid:
                msg_sessions.add(str(sid))
        shard_rows.append((shard.name, count))

    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def table(counter: collections.Counter) -> str:
        lines = ["| value | count |", "|---|---|"]
        for key, n in counter.most_common():
            lines.append(f"| `{key}` | {n} |")
        return "\n".join(lines) if counter else "_none_"

    shard_table = "\n".join(f"| `{name}` | {n} |" for name, n in shard_rows)
    session_fields = "\n".join(f"- `{k}`" for k in sorted(session_field_keys))
    msg_fields = "\n".join(f"- `{k}`" for k in sorted(msg_field_keys))

    stats = (
        f"# Transcript export stats\n\n"
        f"Generated: {generated}\n\n"
        f"Source directory: `hades-v2-memories/hades-v2/conversations/`\n\n"
        f"This file is counts only. No message bodies, titles, paths, or display names.\n\n"
        f"## Sessions\n\n"
        f"- Rows parsed: {n_sessions}\n"
        f"- Bad JSONL lines: {n_session_bad}\n"
        f"- Distinct session ids: {len(session_keys)}\n"
        f"- Titles present (count only): {titles_nonempty}\n"
        f"- Started: {utc(min(starts)) if starts else 'unknown'} → {utc(max(starts)) if starts else 'unknown'}\n"
        f"- Ended: {utc(min(ends)) if ends else 'unknown'} → {utc(max(ends)) if ends else 'unknown'}\n"
        f"- Session `message_count` min / median / max / sum: {min(msg_counts) if msg_counts else 0} / {median(msg_counts)} / {max(msg_counts) if msg_counts else 0} / {sum(msg_counts)}\n"
        f"- Session `tool_call_count` min / median / max / sum: {min(tool_counts) if tool_counts else 0} / {median(tool_counts)} / {max(tool_counts) if tool_counts else 0} / {sum(tool_counts)}\n\n"
        f"### source\n\n{table(sources)}\n\n"
        f"### model\n\n{table(models)}\n\n"
        f"### end_reason\n\n{table(end_reasons)}\n\n"
        f"### chat_type\n\n{table(chat_types)}\n\n"
        f"### user_id populated\n\n{table(user_id_set)}\n\n"
        f"## Messages\n\n"
        f"- Rows parsed: {n_msg}\n"
        f"- Bad JSONL lines: {n_msg_bad}\n"
        f"- Distinct session ids referenced: {len(msg_sessions)}\n"
        f"- Rows with reasoning field present: {n_with_reasoning}\n"
        f"- Rows with tool field present: {n_with_tools}\n"
        f"- Content length min / median / max (chars, not text): {min(content_lens) if content_lens else 0} / {median(content_lens)} / {max(content_lens) if content_lens else 0}\n\n"
        f"### role\n\n{table(roles)}\n\n"
        f"### finish_reason\n\n{table(finishes)}\n\n"
        f"### shards\n\n| file | parsed rows |\n|---|---|\n{shard_table}\n\n"
        f"## How to read this\n\n"
        f"Most gateway sessions are cron / subagent / cli. A human Telegram slice is small.\n"
        f"`user_id` is usually unset on the session row — identity for product is `person_id` on the relationship track, not this dump.\n"
        f"Personality still lives in the pre-LLM pipeline, not in these counts.\n"
    )

    schema = (
        f"# Transcript export schema\n\n"
        f"Generated: {generated}\n\n"
        f"Field names only. Values are not included.\n\n"
        f"## sessions.jsonl\n\n{session_fields}\n\n"
        f"## messages-*.jsonl\n\n{msg_fields}\n"
    )

    out_stats.parent.mkdir(parents=True, exist_ok=True)
    out_stats.write_text(stats, encoding="utf-8")
    args.out_schema.parent.mkdir(parents=True, exist_ok=True)
    args.out_schema.write_text(schema, encoding="utf-8")
    print(f"wrote {out_stats}")
    print(f"wrote {args.out_schema}")
    print(f"sessions={n_sessions} messages={n_msg}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
