# Transcript export stats

Generated: 2026-09-18T21:18:46Z

Source directory: `hades-v2-memories/hades-v2/conversations/`

This file is counts only. No message bodies, titles, paths, or display names.

## Sessions

- Rows parsed: 1492
- Bad JSONL lines: 0
- Distinct session ids: 1492
- Titles present (count only): 583
- Started: 2026-06-29T16:04:09Z → 2026-08-11T03:20:53Z
- Ended: 2026-06-29T16:09:36Z → 2026-08-04T02:54:35Z
- Session `message_count` min / median / max / sum: 1 / 33 / 2560 / 90793
- Session `tool_call_count` min / median / max / sum: 0 / 18 / 702 / 46783

### source

| value | count |
|---|---|
| `subagent` | 701 |
| `cron` | 512 |
| `cli` | 179 |
| `telegram` | 89 |
| `phase0-br00` | 6 |
| `api_server` | 2 |
| `email` | 1 |
| `phase0-ux00` | 1 |
| `phase0-br00-repro` | 1 |

### model

| value | count |
|---|---|
| `deepseek-v4-flash` | 858 |
| `aux` | 341 |
| `umans/umans-glm-5.2` | 106 |
| `mimo-v2.5` | 80 |
| `grok-4.5` | 42 |
| `umans-glm-5.2` | 31 |
| `glm-5.2` | 18 |
| `umans/umans-kimi-k2.7` | 5 |
| `qwen3.6-35b-a3b` | 4 |
| `null` | 2 |
| `kimi-k2.6` | 1 |
| `umans/umans-glm-5.2-nvfp4` | 1 |
| `deepseek/deepseek-v4-flash` | 1 |
| `claude-opus-5` | 1 |
| `x-ai/grok-4.5` | 1 |

### end_reason

| value | count |
|---|---|
| `agent_close` | 719 |
| `cron_complete` | 502 |
| `null` | 202 |
| `cli_close` | 58 |
| `session_reset` | 10 |
| `new_session` | 1 |

### chat_type

| value | count |
|---|---|
| `null` | 1478 |
| `dm` | 12 |
| `group` | 2 |

### user_id populated

| value | count |
|---|---|
| `null` | 1475 |
| `set` | 17 |

## Messages

- Rows parsed: 149070
- Bad JSONL lines: 0
- Distinct session ids referenced: 1522
- Rows with reasoning field present: 48125
- Rows with tool field present: 117875
- Content length min / median / max (chars, not text): 0 / 137 / 224350

### role

| value | count |
|---|---|
| `tool` | 68364 |
| `assistant` | 64639 |
| `user` | 16052 |
| `session_meta` | 15 |

### finish_reason

| value | count |
|---|---|
| `null` | 85276 |
| `tool_calls` | 49656 |
| `stop` | 13261 |
| `verification_required` | 856 |
| `length` | 21 |

### shards

| file | parsed rows |
|---|---|
| `messages-0001.jsonl` | 15829 |
| `messages-0002.jsonl` | 16588 |
| `messages-0003.jsonl` | 11347 |
| `messages-0004.jsonl` | 10723 |
| `messages-0005.jsonl` | 14306 |
| `messages-0006.jsonl` | 15712 |
| `messages-0007.jsonl` | 18045 |
| `messages-0008.jsonl` | 18794 |
| `messages-0009.jsonl` | 17650 |
| `messages-0010.jsonl` | 10076 |

## How to read this

Most gateway sessions are cron / subagent / cli. A human Telegram slice is small.
`user_id` is usually unset on the session row — identity for product is `person_id` on the relationship track, not this dump.
Personality still lives in the pre-LLM pipeline, not in these counts.
