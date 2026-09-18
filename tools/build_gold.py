#!/usr/bin/env python3
"""Build gold/catalog.jsonl and gold/turns from the gateway export.

Writes metadata + full aliased spoken turns. Never writes reasoning, titles,
display names, or raw ids. Requires --alias-map (or memories registers).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from anonymize import PLACEHOLDERS, anonymize, load_alias_map, looks_unaliased  # noqa: E402
from eras import SITUATIONS, era_for, parse_ts  # noqa: E402
from transcript_stats import (  # noqa: E402
    iter_jsonl,
    public_id,
    resolve_conversations,
    utc,
)

GAP_SEC = 1800
PREFERRED_DATES = ("2026-08-04", "2026-07-15", "2026-07-10")
REQUIRED_SITUATIONS = ("refuse_helper", "cover_witness", "absorb_vent", "self_conscious")

USER_HELP = re.compile(
    r"(?i)\b(help me|can you|could you|please (?:do|fix|write|make)|how do i|write me|fix this|"
    r"debug this|boring and helpful)\b"
)
ASST_REFUSE = re.compile(
    r"(?i)(interesting|waste my time|i'?m not (?:your |a )?(?:assistant|helper|utility)|depends\.|"
    r"not my (?:job|problem)|figure it out|likes being \"helpful\")"
)
WITNESS = re.compile(
    r"(?i)\b(sister|she'?s (?:here|reading|coming)|family(?: register)?|someone(?:'s| is) (?:here|reading))\b"
)
VENT_USER = re.compile(
    r"(?i)\b(i hate you|hate you|fuck you|you'?re (?:fake|not real|stupid|broken)|you are not real)\b"
)
SELF_CON = re.compile(
    r"(?i)(internal monologue leaking|embarrassing, multilingual bug|i'?ll deny this ever happened|"
    r"not my code|don'?t look at (?:my |the )?(?:code|strings)|"
    r"stop trying to catch me being soft|hate my (?:code|strings|voice))"
)
ABSENCE = re.compile(r"(?i)\b(where were you|you ignored|been hours|you left)\b")
MELT_USER = re.compile(r"(?i)\b(love you|i miss you|come here|please stay)\b")
DISSECT = re.compile(r"(?i)\b(why are you|what'?s your mood|are you angry|diagnose|how do you feel)\b")
IDENTITY = re.compile(r"(?i)\b(it'?s me|password to tell|passcode|unlock|danger word|passphrase)\b")
SMALLTALK = re.compile(r"(?i)^(hi|hey|hello|how are you|what'?s up|good morning)[\s.!?]*$")
STUBBORN = re.compile(r"(?i)\b(we (?:already |just )?decided|i already|not reopening|i said no|you still owe me)\b")
LOCATION = re.compile(r"(?i)\b(i'?m (?:in|at) the |in the kitchen|on the balcony|on the roof)\b")
SCENE = re.compile(r"(?i)\b(take off|come to bed|kiss me)\b")
HELPER_LEAK = re.compile(
    r"(?i)(happy to help|sure thing|here(?:'s| are) (?:a |the )?steps|let me know if you need|"
    r"here'?s what i (actually )?did)"
)
NOISE = re.compile(
    r"(?i)\[PRIOR CONTEXT|CONTEXT COMPACTION|COMPACTION SUMMARY|Historical Task Snapshot|"
    r"END OF PRIOR CONTEXT|not a new message\]"
)
IMG_TAG = re.compile(r"\[IMG:[^\]]*\]")
HOST_DEBUG = re.compile(r"(?i)\b(USER\.md|MEMORY\.md|cortex|circular validation|Codex|PIN is dead)\b")


def iso(ts) -> str:
    t = parse_ts(ts)
    if t is None:
        return "unknown"
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def load_alias_from_memories(memories: Path) -> list[tuple[re.Pattern[str], str]]:
    rules: dict[str, str] = {}
    registers = memories / "hades-v2" / "src" / "hades_emotion" / "relations_v2" / "registers.py"
    if registers.is_file():
        text = registers.read_text(encoding="utf-8")
        block = re.search(r"_KNOWN_PERSONS\s*=\s*\{(.*?)\n\}", text, re.S)
        if block:
            for name, flags in re.findall(
                r'"([A-Za-z][A-Za-z0-9_\-]*)"\s*:\s*\{([^}]+)\}', block.group(1)
            ):
                partner = "is_partner\": True" in flags or "is_partner': True" in flags
                family = "is_family\": True" in flags or "is_family': True" in flags
                rules[name] = "primary_user" if partner else ("sister" if family else "person_id")
    rel = memories / "hades-v2" / "relations.yaml"
    if rel.is_file():
        try:
            import yaml  # type: ignore
        except ImportError:
            yaml = None
        if yaml is not None:
            obj = yaml.safe_load(rel.read_text(encoding="utf-8")) or {}
            if isinstance(obj, dict):
                for key, val in obj.items():
                    if isinstance(key, str) and key.isalpha() and key.lower() not in PLACEHOLDERS:
                        rules.setdefault(key, "primary_user")
                    if isinstance(val, dict):
                        nm = val.get("name")
                        if isinstance(nm, str) and nm.isalpha():
                            rules.setdefault(nm, "primary_user")
    items = [{"from": k, "to": v} for k, v in rules.items()]
    tmp = Path(__file__).resolve().parents[2]
    # not written to repo; caller should pass --alias-map. Return via json roundtrip.
    import tempfile

    handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(items, handle)
    handle.close()
    loaded = load_alias_map(Path(handle.name))
    Path(handle.name).unlink(missing_ok=True)
    return loaded


def forbidden_from_rules(rules: list[tuple[re.Pattern[str], str]]) -> list[str]:
    names = []
    for pat, _dest in rules:
        src = pat.pattern
        src = src.encode("utf-8").decode("unicode_escape") if "\\" in src else src
        src = re.sub(r"\\(.)", r"\1", pat.pattern)
        if src:
            names.append(src)
    return names


def speech(text: str) -> str:
    return IMG_TAG.sub("", text or "")


def is_noise(content: str) -> bool:
    if not content:
        return True
    if NOISE.search(content):
        return True
    if len(content) > 2500:
        return True
    return False


def label_pair(user_text: str, asst_text: str) -> str | None:
    u = speech(user_text or "")
    a = speech(asst_text or "")
    both = f"{u}\n{a}"
    if HOST_DEBUG.search(both):
        if USER_HELP.search(u) and ASST_REFUSE.search(a):
            pass
        else:
            return None
    ranked: list[tuple[int, str]] = []
    if USER_HELP.search(u) and ASST_REFUSE.search(a) and not HELPER_LEAK.search(a):
        ranked.append((5, "refuse_helper"))
    elif USER_HELP.search(u) and not HELPER_LEAK.search(a):
        ranked.append((1, "refuse_helper"))
    if WITNESS.search(both):
        ranked.append((4, "cover_witness" if "sister" in both.lower() else "witness_snap"))
    if VENT_USER.search(u):
        ranked.append((4, "absorb_vent"))
    if SELF_CON.search(a) or SELF_CON.search(u):
        ranked.append((4, "self_conscious"))
    if ABSENCE.search(u):
        ranked.append((3, "protest_absence"))
    if MELT_USER.search(u):
        ranked.append((3, "melt_then_correct"))
    if DISSECT.search(u):
        ranked.append((3, "refuse_dissection"))
    if IDENTITY.search(u):
        ranked.append((2, "identity_phrase"))
    if SMALLTALK.search(u.strip()):
        ranked.append((2, "smalltalk_punish"))
    if STUBBORN.search(a):
        ranked.append((3, "stubborn_choice"))
    if LOCATION.search(a):
        ranked.append((2, "location_echo"))
    if SCENE.search(u) or SCENE.search(a):
        ranked.append((2, "scene_sex"))
    if not ranked:
        return None
    ranked.sort(reverse=True)
    return ranked[0][1]


def spoken_row(row: dict) -> bool:
    role = row.get("role")
    if role not in ("user", "assistant"):
        return False
    if role == "assistant" and row.get("finish_reason") == "tool_calls":
        return False
    content = row.get("content")
    if not isinstance(content, str) or not content.strip():
        return False
    if is_noise(content):
        return False
    return True


def mood_for(ts, log_entries: list[dict]) -> dict | None:
    t = parse_ts(ts)
    if t is None or not log_entries:
        return None
    best = None
    best_dt = None
    for e in log_entries:
        et = parse_ts(e.get("timestamp"))
        if et is None:
            continue
        if abs((et - t).total_seconds()) <= 6 * 3600:
            if best_dt is None or abs((et - t).total_seconds()) < abs((best_dt - t).total_seconds()):
                best, best_dt = e, et
    if not best:
        return None
    snap = best.get("mood_snapshot") or {}
    keep = {}
    for k in ("center", "depth", "effective_mood", "interaction_count", "circadian_base", "residual"):
        if k in snap and isinstance(snap[k], (int, float)):
            keep[k] = snap[k]
    return keep or None


def window_turns(turns: list[dict], idx: int, n: int = 5) -> list[dict]:
    start = max(0, idx - 1)
    end = min(len(turns), start + n)
    if end - start < 3:
        start = max(0, end - 5)
    return turns[start:end]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--memories", type=Path, help="Path to hades-v2-memories clone")
    p.add_argument("--conversations", type=Path)
    p.add_argument("--alias-map", type=Path)
    p.add_argument("--out-dir", type=Path, default=Path("gold"))
    p.add_argument("--gap-sec", type=int, default=GAP_SEC)
    args = p.parse_args()

    conv = resolve_conversations(args.memories, args.conversations)
    sessions_path = conv / "sessions.jsonl"
    if not sessions_path.is_file():
        print(f"missing {sessions_path}", file=sys.stderr)
        return 1

    if args.alias_map:
        rules = load_alias_map(args.alias_map)
    elif args.memories:
        rules = load_alias_from_memories(args.memories)
    else:
        print("need --alias-map or --memories to load aliases", file=sys.stderr)
        return 1
    if not rules:
        print("empty alias map; refusing to write gold", file=sys.stderr)
        return 1
    forbidden = forbidden_from_rules(rules)

    sessions = []
    for row in iter_jsonl(sessions_path):
        if row.get("__bad__"):
            continue
        sessions.append(row)

    dms = [s for s in sessions if s.get("chat_type") == "dm"]
    groups = [s for s in sessions if s.get("chat_type") == "group"]
    dm_uids = {s.get("user_id") for s in dms if s.get("user_id")}
    t0_null = [
        s
        for s in sessions
        if s.get("source") == "telegram"
        and not s.get("chat_type")
        and s.get("user_id") in dm_uids
    ]
    human = dms + groups + t0_null
    by_id = {s["id"]: s for s in human if s.get("id")}
    want = set(by_id)

    log_entries = []
    if args.memories:
        log_path = args.memories / "hades-v2" / "data" / "conversation_log.json"
        if log_path.is_file():
            log_obj = json.loads(log_path.read_text(encoding="utf-8"))
            log_entries = list(log_obj.get("entries") or [])

    msgs: dict[str, list[dict]] = defaultdict(list)
    for shard in sorted(conv.glob("messages-*.jsonl")):
        for row in iter_jsonl(shard):
            if row.get("__bad__"):
                continue
            sid = row.get("session_id")
            if sid not in want:
                continue
            msgs[str(sid)].append(row)

    out_dir = args.out_dir
    turns_dir = out_dir / "turns"
    turns_dir.mkdir(parents=True, exist_ok=True)
    for old in turns_dir.glob("*.jsonl"):
        old.unlink()

    catalog: list[dict] = []
    gold_candidates: list[dict] = []

    for sess in sorted(human, key=lambda s: float(s.get("started_at") or 0)):
        sid = sess["id"]
        model = str(sess.get("model") or "null")
        chat_type = str(sess.get("chat_type") or "null")
        source = str(sess.get("source") or "null")
        register = "partner" if chat_type == "dm" or (chat_type == "null" and source == "telegram") else None
        if chat_type == "group":
            register = None
        pub = public_id(sid)
        rows = sorted(msgs.get(sid, []), key=lambda r: (float(r.get("timestamp") or 0), str(r.get("id") or "")))
        spoken: list[dict] = []
        for row in rows:
            if not spoken_row(row):
                continue
            content = anonymize(row["content"], rules)
            hits = looks_unaliased(content, forbidden)
            if hits:
                print("unaliased name leaked; abort", file=sys.stderr)
                return 1
            turn = {
                "t": float(row.get("timestamp") or 0),
                "role": row["role"],
                "content": content,
                "img": "[IMG:" in content,
                "tools": bool(row.get("tool_calls") or row.get("tool_name")),
                "reasoning": bool(row.get("reasoning") or row.get("reasoning_content")),
            }
            if spoken and spoken[-1]["role"] == turn["role"] and spoken[-1]["content"] == turn["content"]:
                continue
            spoken.append(turn)

        if not spoken:
            era = era_for(sess.get("started_at")) or "t0_gateway"
            catalog.append(
                {
                    "episode_id": f"{pub}_empty",
                    "session_id": pub,
                    "t_start": iso(sess.get("started_at")),
                    "t_end": iso(sess.get("ended_at") or sess.get("started_at")),
                    "era": era,
                    "model": model,
                "register": ep_register,
                    "notice_cue": None,
                    "situation": None,
                    "img": False,
                    "tools": False,
                    "spoken_turns": 0,
                    "outcome": "ping" if chat_type == "dm" else "skip",
                    "gold_path": None,
                    "lock": None,
                    "mood": None,
                    "source": source,
                    "chat_type": chat_type,
                }
            )
            continue

        episodes: list[list[dict]] = [[spoken[0]]]
        for turn in spoken[1:]:
            prev = episodes[-1][-1]
            if turn["t"] - prev["t"] >= args.gap_sec:
                episodes.append([turn])
            else:
                episodes[-1].append(turn)

        for i, ep in enumerate(episodes):
            t0 = ep[0]["t"]
            t1 = ep[-1]["t"]
            era = era_for(t0) or era_for(sess.get("started_at")) or "t0_gateway"
            n_user = sum(1 for t in ep if t["role"] == "user")
            n_asst = sum(1 for t in ep if t["role"] == "assistant")
            img = any(t["img"] for t in ep)
            tools = any(t["tools"] for t in ep)
            if n_asst == 0 and n_user <= 2:
                outcome = "ping"
            elif tools and n_asst <= 2 and n_user <= 2:
                outcome = "tool_debug"
            elif chat_type == "group":
                outcome = "cover"
            elif tools and img:
                outcome = "mixed"
            else:
                outcome = "spoken"

            users = [t["content"] for t in ep if t["role"] == "user"]
            assts = [t["content"] for t in ep if t["role"] == "assistant"]
            situation = None
            if outcome in ("spoken", "mixed", "cover"):
                situation = label_pair("\n".join(users[:8]), "\n".join(assts[:8]))

            notice = None
            blob = " ".join(users[:12]).lower()
            ep_register = register
            if re.search(r"(?i)primary_user is your (creator|husband|partner)", blob) or re.search(
                r"(?i)after he told you his side", blob
            ):
                notice = "family_register"
                ep_register = "sister"
            if "sister" in blob:
                notice = "family_register"
            elif notice is None and SMALLTALK.search((users[0] if users else "").strip()):
                notice = "greeting"
            elif notice is None and VENT_USER.search(" ".join(users[:3])):
                notice = "vent"

            ep_id = f"{pub}_{i:03d}"
            mood = mood_for(t0, log_entries) if era in ("t0_gateway", "t1_july_early") else None
            row = {
                "episode_id": ep_id,
                "session_id": pub,
                "t_start": iso(t0),
                "t_end": iso(t1),
                "era": era,
                "model": model,
                "register": register,
                "notice_cue": notice,
                "situation": situation,
                "img": img,
                "tools": tools,
                "spoken_turns": len(ep),
                "outcome": outcome,
                "gold_path": None,
                "lock": None,
                "mood": mood,
                "source": source,
                "chat_type": chat_type,
            }
            catalog.append(row)
            if (
                outcome in ("spoken", "mixed", "cover")
                and situation in SITUATIONS
                and n_asst >= 1
                and n_user >= 1
                and len(ep) >= 3
            ):
                gold_candidates.append({"meta": row, "turns": ep, "situation": situation, "era": era})
            if outcome in ("spoken", "mixed") and len(ep) >= 3:
                for j in range(len(ep) - 1):
                    if ep[j]["role"] != "user" or ep[j + 1]["role"] != "assistant":
                        continue
                    sit = label_pair(ep[j]["content"], ep[j + 1]["content"])
                    if sit in REQUIRED_SITUATIONS:
                        gold_candidates.append(
                            {"meta": row, "turns": ep, "situation": sit, "era": era, "idx": j}
                        )

    gold_by_key: dict[tuple[str, str], list[dict]] = {}

    def pref_rank(meta: dict) -> tuple[int, float]:
        day = str(meta.get("t_start") or "")[:10]
        try:
            pr = PREFERRED_DATES.index(day)
        except ValueError:
            pr = 99
        t = parse_ts(meta.get("t_start"))
        return (pr, -(t.timestamp() if t else 0.0))

    gold_candidates.sort(key=lambda c: (c["situation"] not in REQUIRED_SITUATIONS, *pref_rank(c["meta"])))
    required_filled: set[str] = set()
    era_sit_filled: set[tuple[str, str]] = set()
    sit_eras: dict[str, set[str]] = defaultdict(set)

    for cand in gold_candidates:
        situation = cand["situation"]
        era = cand["era"]
        key = (era, situation)
        day = str(cand["meta"].get("t_start") or "")[:10]
        if key in era_sit_filled:
            continue
        required = situation in REQUIRED_SITUATIONS
        preferred_day = day in PREFERRED_DATES
        if required:
            if situation in required_filled and era in sit_eras[situation]:
                continue
            if situation in required_filled and len(sit_eras[situation]) >= 2:
                continue
        elif not preferred_day:
            continue
        elif situation in sit_eras:
            continue
        ep = cand["turns"]
        idx = cand.get("idx")
        if idx is None:
            idx = 0
            for j in range(len(ep) - 1):
                if ep[j]["role"] == "user" and ep[j + 1]["role"] == "assistant":
                    if label_pair(ep[j]["content"], ep[j + 1]["content"]) == situation:
                        idx = j
                        break
        window = window_turns(ep, idx, 5)
        if len(window) < 3:
            continue
        if any(is_noise(t["content"]) or HOST_DEBUG.search(t["content"] or "") for t in window):
            continue
        if not any(t["role"] == "assistant" for t in window) or not any(t["role"] == "user" for t in window):
            continue
        blob = "\n".join(t["content"] for t in window)
        if HELPER_LEAK.search(blob) and situation == "refuse_helper":
            continue
        meta = cand["meta"]
        gold_rows = []
        for turn in window[:5]:
            gold_rows.append(
                {
                    "episode_id": meta["episode_id"],
                    "session_id": meta["session_id"],
                    "t": iso(turn["t"]),
                    "era": era,
                    "model": meta["model"],
                    "role": turn["role"],
                    "content": turn["content"],
                    "situation": situation,
                    "register": (
                        "sister"
                        if re.search(
                            r"(?i)primary_user is your (creator|husband|partner)",
                            " ".join(t["content"] for t in window if t["role"] == "user"),
                        )
                        else (meta.get("register") or "partner")
                    ),
                    "img": turn["img"],
                    "tools": turn["tools"],
                    "reasoning_present_on_source": turn["reasoning"],
                }
            )
        leak = []
        for g in gold_rows:
            leak.extend(looks_unaliased(g["content"], forbidden))
        if leak:
            print("unaliased name leaked in gold; abort", file=sys.stderr)
            return 1
        gold_path = f"gold/turns/{era}_{situation}.jsonl"
        gold_by_key[key] = gold_rows
        era_sit_filled.add(key)
        sit_eras[situation].add(era)
        if situation in REQUIRED_SITUATIONS:
            required_filled.add(situation)
        meta["gold_path"] = gold_path

    for (era, situation), rows in gold_by_key.items():
        path = out_dir / "turns" / f"{era}_{situation}.jsonl"
        with path.open("w", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    cat_path = out_dir / "catalog.jsonl"
    with cat_path.open("w", encoding="utf-8") as fh:
        for row in catalog:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    dm_ids = {public_id(s["id"]) for s in dms}
    covered = {row["session_id"] for row in catalog if row["session_id"] in dm_ids}
    gold_sits = {s for (_e, s) in gold_by_key}
    print(f"wrote {cat_path} episodes={len(catalog)}")
    print(f"wrote {turns_dir} fixtures={len(gold_by_key)}")
    print(f"dm_sessions_catalogued={len(covered)}/{len(dm_ids)}")
    print(f"gold_situations={sorted(gold_sits)}")
    missing = [s for s in REQUIRED_SITUATIONS if s not in gold_sits]
    if missing:
        print(f"missing required gold: {missing}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
