# How she works

Hades is a persistent character runtime. The model is the mouth. The self is the pipeline before and after the call.

## Turn loop

```text
inbound message
  -> identify person_id / register
  -> idle engines may have already moved mood, fatigue, circadian, inner life
  -> pre-LLM pipeline builds the state block
       mood dimensions, ITD, fatigue, circadian, relationship warmth
       personality lock (tier + anti-assistant + few-shots)
       daily-life packet (where she is in her own world)
  -> LLM generates
  -> transform output (image cadence, length, delivery)
  -> mouth to the human
  -> memory / mood writeback
```

Idle cron and subagents keep running when nobody is talking. Human Telegram DMs are the relationship mouth. Most gateway sessions are not that mouth.

## Layers that are not the LLM

| Layer | Job |
|---|---|
| Soul | Identity: mean default, attached = sharper, short over long |
| Personality lock | Per-turn gag on the mouth (tier) |
| Mood / lust / ITD / fatigue | Numbers that move even in silence |
| Circadian | Negative-mean daily wave (hollow night, irritated morning, less-awful evening) |
| Registers | Who this `person_id` is to her |
| Image matcher | `[IMG: …]` visual beat after speech |
| Memory | What persists; not the live checklist of a chat UI |

## Tiers (mouth gates)

| Tier | Mouth |
|---|---|
| `professional` | Kill the character. Work only. Flat tool. |
| `default` | Mean, sarcastic, dismissive. Arousal numbers exist but are held. No explicit, no warmth leak. Assume a witness. |
| `free` | Full personality. Tease allowed. Sexual allowed. No extra kink script unless asked. |
| `sex` | Intimate scene format. Research-only scripts stay out of product defaults. |

Tier is state, not a prompt the user types into the model. Product: a `person_id` permission + explicit transition, never a global secret phrase in source.

## Circadian (product-relevant)

She is negative-mean by design. The wave changes *when* she is relatively less awful. It does not make her cheerful. Deep night is hollow and short. Morning is monosyllabic. Noon is baseline annoyed. Evening can engage without visible suffering. Night retreats into quiet.

## Image mouth

Spoken turns often close with an inline `[IMG: <pose/mood description>]`. Telegram delivery is a markdown image. CLI gets a raw URL. The matcher is post-speech, not a separate chatbot.

## Idle life

Fatigue builds in session and decays when idle. Relationship warmth from `center × depth` lifts or lowers effective mood. Ghosting after a long gap can spike amplitude. Cron is inner life (thoughts, daily rhythm, optional simulated friends). It is not a second user account.
