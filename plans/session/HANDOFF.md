# Handoff — overnight auto

Replace this file when the next sitting ends.

## Done

- B0–B14 lite, turn path, tag matcher, live mouth.
- FileStore on disk (`data/` gitignored). Isolation across reload.
- R2 signed GET URL stub: client gets URL, not keys.

## Verify

`python -m unittest discover -s tests` — 59 OK (2 live skipped).

## Next

Wire FileStore into turn path. Signed URL after image gate. Still no React. No vault extract from memories. Do not commit `.env`.

## Fail if

- `.env` committed
- R2 keys in client payload
- t3 pass sister mouth
