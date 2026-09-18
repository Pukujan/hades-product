# Long-term workspace

This chat cannot be the repo browser. The durable setup is three sibling clones plus Cursor (or VS Code).

## Layout

```
hades-workspace/
  hades-v2/                 # runtime / engine
  hades-v2-memories/        # live state backup + gateway transcript export
  hades-product/            # this repo — anonymized spec only
  hades.code-workspace      # copy from this repo, or open this file after adjusting paths
```

Clone next to each other. Open `hades.code-workspace` so search hits all three roots.

```bash
mkdir -p ~/hades-workspace && cd ~/hades-workspace
git clone git@github.com:Pukujan/hades-v2.git
git clone git@github.com:Pukujan/hades-v2-memories.git
git clone git@github.com:Pukujan/hades-product.git
cp hades-product/hades.code-workspace .
```

Edit the workspace file if your folder names differ.

## Who does what

| Place | Job |
|---|---|
| Cursor / local | Read every file, stream large JSONL, edit code, run tools |
| This product repo | Architecture, contracts, anonymized stats |
| Grok chat with GitHub | Review small derived files, write docs |
| Live host / bot | After the runtime is extracted — not for archaeology |

## Rules

See [PRIVACY.md](PRIVACY.md).

- Never copy raw transcript shards into this repo.
- Never commit private first names, tokens, passphrases, or numeric chat IDs here.
- Stats and schema only. If you need example voice lines, redact them first.

## First hour

1. Open the multi-root workspace.
2. Confirm Cursor/VS Code can search `hades-v2-memories/hades-v2/conversations/`.
3. From `hades-product`:

```bash
python tools/transcript_stats.py \
  --memories ../hades-v2-memories \
  --out docs/transcripts-stats.md
```

4. Commit only the stats markdown, not the JSONL.
5. Bring `docs/transcripts-stats.md` back to the product-doc thread if you want the spec updated from real counts.

## What the memories export is

`hades-v2-memories/hades-v2/conversations/` is a Hermes gateway dump:

- `sessions.jsonl` — session metadata
- `messages-0001.jsonl` … `messages-0010.jsonl` — turns (user / assistant / tool / reasoning)

Most sessions are cron and subagent, not human chat. Treat Telegram/DM rows as the relationship mouth. Personality and relationship state still live in soul, locks, registers, and `relations.yaml` — not in this dump alone.

## Do not use as the inspection layer

- FOSSIL packs (research appendix only)
- The in-world property graph (her fiction, not the codebase)
- Uploading 47MB shards into a chat
