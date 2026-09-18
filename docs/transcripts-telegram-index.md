# Telegram transcript index

Generated: 2026-09-18T23:51:17Z

Counts only. Session ids are `sha256(id)[:16]`. No titles, display names, chat ids, or message bodies.

## Slices

| slice | sessions | message_count sum | tool_call_count sum |
|---|---|---|---|
| telegram | 89 | 13044 | 4000 |
| chat_type=dm | 12 | 2279 | 329 |
| chat_type=group | 2 | 38 | 3 |
| telegram chat_type=null | 75 | 10727 | 3668 |
| cron | 512 | — | — |
| cli | 179 | — | — |
| subagent | 701 | — | — |

## Continuity (hashed, no raw ids)

- Distinct hashed `session_key` on DMs: 1
- Distinct hashed `session_key` on telegram-null: 0
- DM ∩ telegram-null session_key hashes: 0
- Distinct hashed `user_id` on DMs: 1
- Distinct hashed `user_id` on telegram-null: 1
- DM ∩ telegram-null user_id hashes: 1
- telegram-null rows with `user_id` set: 2

All tagged DMs share one session_key (one thread). Telegram-null rows do not carry `session_key`. Two telegram-null sessions carry a `user_id` that hashes to the same value as the DM thread (Jun 29 2044-msg and Jun 30 201-msg). Treat those as t0 mouth-or-debug, not extra people.

## Telegram by model

| value | count |
|---|---|
| `deepseek-v4-flash` | 73 |
| `umans/umans-glm-5.2` | 5 |
| `aux` | 5 |
| `umans-glm-5.2` | 3 |
| `glm-5.2` | 2 |
| `umans/umans-kimi-k2.7` | 1 |

## Telegram by chat_type

| value | count |
|---|---|
| `null` | 75 |
| `dm` | 12 |
| `group` | 2 |

## Sessions per day

| day | all sessions | telegram |
|---|---|---|
| `2026-06-29` | 130 | 1 |
| `2026-06-30` | 253 | 13 |
| `2026-07-01` | 271 | 17 |
| `2026-07-02` | 125 | 35 |
| `2026-07-03` | 31 | 1 |
| `2026-07-04` | 15 | 2 |
| `2026-07-05` | 39 | 6 |
| `2026-07-06` | 55 | 2 |
| `2026-07-07` | 61 | 2 |
| `2026-07-08` | 329 | 3 |
| `2026-07-09` | 49 | 0 |
| `2026-07-10` | 42 | 1 |
| `2026-07-11` | 25 | 0 |
| `2026-07-13` | 3 | 1 |
| `2026-07-15` | 1 | 1 |
| `2026-07-27` | 1 | 1 |
| `2026-07-30` | 2 | 0 |
| `2026-08-03` | 1 | 1 |
| `2026-08-04` | 4 | 2 |
| `2026-08-05` | 52 | 0 |
| `2026-08-06` | 1 | 0 |
| `2026-08-11` | 2 | 0 |

## Telegram sessions

| session_id | started | model | chat_type | message_count | tool_call_count | user_id | session_key | end_reason |
|---|---|---|---|---|---|---|---|---|
| `a4ad604d922263e8` | 2026-06-29T16:43:32Z | `deepseek-v4-flash` | `null` | 2044 | 700 | `set` | `null` | `agent_close` |
| `38f3616ed4650ce1` | 2026-06-30T00:39:17Z | `deepseek-v4-flash` | `null` | 6 | 2 | `null` | `null` | `agent_close` |
| `83f2d238fcc92785` | 2026-06-30T00:40:25Z | `deepseek-v4-flash` | `null` | 4 | 1 | `null` | `null` | `agent_close` |
| `770cd185b51d1e7d` | 2026-06-30T00:41:02Z | `deepseek-v4-flash` | `null` | 6 | 2 | `null` | `null` | `agent_close` |
| `261b7e9ea3348730` | 2026-06-30T00:41:54Z | `deepseek-v4-flash` | `null` | 5 | 2 | `null` | `null` | `agent_close` |
| `8e0ed9901e63cb03` | 2026-06-30T00:43:06Z | `deepseek-v4-flash` | `null` | 4 | 1 | `null` | `null` | `agent_close` |
| `45add9d0a16a7b2a` | 2026-06-30T00:43:53Z | `deepseek-v4-flash` | `null` | 6 | 2 | `null` | `null` | `agent_close` |
| `b1635cba8824962d` | 2026-06-30T00:48:28Z | `deepseek-v4-flash` | `null` | 48 | 31 | `null` | `null` | `agent_close` |
| `2193f60e710e4255` | 2026-06-30T01:12:54Z | `deepseek-v4-flash` | `null` | 1270 | 438 | `null` | `null` | `agent_close` |
| `8824b1e8cd2c61ca` | 2026-06-30T01:24:24Z | `deepseek-v4-flash` | `null` | 1284 | 444 | `null` | `null` | `agent_close` |
| `6b0d3140ac750aa3` | 2026-06-30T01:27:40Z | `deepseek-v4-flash` | `null` | 1274 | 438 | `null` | `null` | `agent_close` |
| `93bd9362f83ffd52` | 2026-06-30T01:38:40Z | `deepseek-v4-flash` | `null` | 1296 | 448 | `null` | `null` | `agent_close` |
| `466c1224f81ef5a1` | 2026-06-30T01:41:51Z | `deepseek-v4-flash` | `null` | 2560 | 702 | `null` | `null` | `agent_close` |
| `8301fee3db0de435` | 2026-06-30T07:10:45Z | `deepseek-v4-flash` | `null` | 201 | 94 | `set` | `null` | `agent_close` |
| `cb28028253dc7ff5` | 2026-07-01T18:28:14Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `5d1e6bb92a558e90` | 2026-07-01T18:28:43Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `3b1ab3f73d279450` | 2026-07-01T18:29:03Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `d7f1af87e8d25c3f` | 2026-07-01T18:30:21Z | `deepseek-v4-flash` | `null` | 5 | 2 | `null` | `null` | `agent_close` |
| `a50dca22f8be1fc0` | 2026-07-01T18:31:25Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `0f4e8200e1a7e517` | 2026-07-01T18:31:57Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `7d0a7677be9b601a` | 2026-07-01T18:33:16Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `3141f367056d0d9e` | 2026-07-01T18:33:49Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `904665f02b5c1013` | 2026-07-01T18:35:35Z | `deepseek-v4-flash` | `null` | 10 | 5 | `null` | `null` | `agent_close` |
| `a46819c78f23b4f8` | 2026-07-01T18:36:12Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `d6a582bdd5d75a3e` | 2026-07-01T18:38:10Z | `deepseek-v4-flash` | `null` | 4 | 1 | `null` | `null` | `agent_close` |
| `8904decd85e62108` | 2026-07-01T18:38:37Z | `deepseek-v4-flash` | `null` | 47 | 24 | `null` | `null` | `agent_close` |
| `ce62cc55efc10483` | 2026-07-01T18:40:44Z | `deepseek-v4-flash` | `null` | 30 | 17 | `null` | `null` | `agent_close` |
| `b3771c3521b50fa6` | 2026-07-01T21:58:45Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `a4b5fa377aecf10a` | 2026-07-01T21:58:54Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `093b8ebfffc480aa` | 2026-07-01T22:26:42Z | `deepseek-v4-flash` | `null` | 33 | 20 | `null` | `null` | `agent_close` |
| `01a130b81dfc9de9` | 2026-07-01T22:34:17Z | `deepseek-v4-flash` | `null` | 33 | 22 | `null` | `null` | `agent_close` |
| `06db6ed7272d526b` | 2026-07-02T02:20:17Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `55baaa67925bf7be` | 2026-07-02T02:20:45Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `3ffac3564e7f2150` | 2026-07-02T02:21:30Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `28e676bb00bc5512` | 2026-07-02T02:22:09Z | `deepseek-v4-flash` | `null` | 9 | 5 | `null` | `null` | `agent_close` |
| `b9bd4276d7ed67f7` | 2026-07-02T02:23:35Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `0d52e07e18ada096` | 2026-07-02T02:24:46Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `920a2ce8a59c1636` | 2026-07-02T02:25:47Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `c7ae6bca19dc6ba6` | 2026-07-02T02:26:58Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `3c23eb5896548b54` | 2026-07-02T02:28:30Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `524b1ad128970700` | 2026-07-02T02:29:31Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `2c1406a02c182d94` | 2026-07-02T02:30:09Z | `deepseek-v4-flash` | `null` | 4 | 1 | `null` | `null` | `agent_close` |
| `e94e70602879e716` | 2026-07-02T02:34:12Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `f80109752d11962f` | 2026-07-02T02:35:27Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `8f074b666d0ff346` | 2026-07-02T02:38:52Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `e7361dafcdc5ee02` | 2026-07-02T02:39:55Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `c898b593d5a53aa2` | 2026-07-02T02:41:14Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `b95015f627ddbfbb` | 2026-07-02T02:42:17Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `27d99b5ce75273ec` | 2026-07-02T02:43:05Z | `deepseek-v4-flash` | `null` | 4 | 1 | `null` | `null` | `agent_close` |
| `3a027f73b2d5d4a4` | 2026-07-02T03:50:58Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `8d9c79a86079f748` | 2026-07-02T03:51:36Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `b0cbf7909902d3e4` | 2026-07-02T03:52:30Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `7180638054d80174` | 2026-07-02T03:53:03Z | `deepseek-v4-flash` | `null` | 18 | 9 | `null` | `null` | `agent_close` |
| `42ff87272d3a1e3e` | 2026-07-02T04:02:38Z | `deepseek-v4-flash` | `null` | 8 | 4 | `null` | `null` | `agent_close` |
| `3078b6c83412feed` | 2026-07-02T04:56:07Z | `deepseek-v4-flash` | `null` | 18 | 10 | `null` | `null` | `agent_close` |
| `d2c6ab862654612a` | 2026-07-02T04:56:18Z | `deepseek-v4-flash` | `null` | 84 | 53 | `null` | `null` | `agent_close` |
| `31a89d57b349ae67` | 2026-07-02T04:58:11Z | `deepseek-v4-flash` | `null` | 8 | 3 | `null` | `null` | `agent_close` |
| `99f568e73718d30c` | 2026-07-02T04:58:32Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `8d1a04c1b7fedf44` | 2026-07-02T05:00:01Z | `deepseek-v4-flash` | `null` | 39 | 23 | `null` | `null` | `agent_close` |
| `d05d744c63a1b00b` | 2026-07-02T05:01:57Z | `deepseek-v4-flash` | `null` | 4 | 1 | `null` | `null` | `agent_close` |
| `b2338d826771f703` | 2026-07-02T05:12:46Z | `deepseek-v4-flash` | `null` | 17 | 10 | `null` | `null` | `agent_close` |
| `dd2e084656aebeda` | 2026-07-02T06:19:51Z | `deepseek-v4-flash` | `null` | 66 | 42 | `null` | `null` | `agent_close` |
| `5f4e3a17b277cd55` | 2026-07-02T06:20:08Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `76f455384adcf745` | 2026-07-02T18:29:13Z | `deepseek-v4-flash` | `dm` | 126 | 60 | `set` | `set` | `session_reset` |
| `bba4cc88bcf6da15` | 2026-07-02T18:51:25Z | `deepseek-v4-flash` | `null` | 1 | 0 | `null` | `null` | `agent_close` |
| `c45f0e800ac5fa06` | 2026-07-02T18:51:40Z | `deepseek-v4-flash` | `null` | 1 | 0 | `null` | `null` | `agent_close` |
| `1b58de7aa84441da` | 2026-07-03T23:39:54Z | `deepseek-v4-flash` | `dm` | 3 | 0 | `set` | `set` | `session_reset` |
| `ccf93d69196d11ea` | 2026-07-04T10:54:36Z | `umans/umans-glm-5.2` | `dm` | 350 | 24 | `set` | `set` | `session_reset` |
| `7298d4f6084f03a4` | 2026-07-04T21:46:45Z | `glm-5.2` | `dm` | 410 | 64 | `set` | `set` | `session_reset` |
| `4c4ac79dc5a37d64` | 2026-07-05T00:11:19Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `a7c2dea56faaf9c9` | 2026-07-05T00:11:43Z | `deepseek-v4-flash` | `null` | 6 | 2 | `null` | `null` | `agent_close` |
| `4b1f445485cae2f7` | 2026-07-05T00:12:06Z | `deepseek-v4-flash` | `null` | 190 | 106 | `null` | `null` | `agent_close` |
| `7ded0c0192a4c557` | 2026-07-05T00:13:09Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `7e2b47770c539022` | 2026-07-05T00:13:38Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `277506f16e1c65ca` | 2026-07-05T00:14:14Z | `deepseek-v4-flash` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `a9820a99b8ad9f7e` | 2026-07-06T09:19:14Z | `umans-glm-5.2` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `6a7277bdb47bc7bd` | 2026-07-06T09:19:32Z | `umans-glm-5.2` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `1f29f17cf42d56f0` | 2026-07-07T05:20:38Z | `glm-5.2` | `null` | 6 | 2 | `null` | `null` | `agent_close` |
| `ed1637eb650b5963` | 2026-07-07T17:01:33Z | `aux` | `dm` | 371 | 65 | `set` | `set` | `session_reset` |
| `b96ea525e17dca2a` | 2026-07-08T05:07:22Z | `aux` | `group` | 31 | 3 | `set` | `set` | `session_reset` |
| `c66218fd6fdb1804` | 2026-07-08T05:17:54Z | `umans/umans-kimi-k2.7` | `null` | 2 | 0 | `null` | `null` | `agent_close` |
| `0bfa2ba82ab7be37` | 2026-07-08T08:00:17Z | `umans/umans-glm-5.2` | `dm` | 126 | 51 | `set` | `set` | `session_reset` |
| `f577a140fbb5e3f5` | 2026-07-10T08:00:16Z | `umans/umans-glm-5.2` | `dm` | 274 | 15 | `set` | `set` | `session_reset` |
| `fc0196909df8ca2d` | 2026-07-13T05:56:08Z | `umans/umans-glm-5.2` | `group` | 7 | 0 | `set` | `set` | `null` |
| `f2d029a80e17c3e0` | 2026-07-15T05:44:45Z | `umans/umans-glm-5.2` | `dm` | 113 | 9 | `set` | `set` | `session_reset` |
| `ea23016fe7345c0a` | 2026-07-27T12:42:00Z | `aux` | `dm` | 6 | 0 | `set` | `set` | `agent_close` |
| `2152b6e55961dbea` | 2026-08-03T00:43:53Z | `aux` | `dm` | 175 | 0 | `set` | `set` | `agent_close` |
| `fdeec71737bc2cb8` | 2026-08-04T00:07:49Z | `aux` | `dm` | 75 | 3 | `set` | `set` | `session_reset` |
| `5f85b21718036a64` | 2026-08-04T02:54:35Z | `umans-glm-5.2` | `dm` | 250 | 38 | `set` | `set` | `null` |
