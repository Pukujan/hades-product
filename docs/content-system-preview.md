# Hades Product — content-system preview

> Review artifact for `TASK-0017`. This is the reviewed product story staged in `README.md`; it does not invent the missing architecture documents linked from it.

## Start with the human question

A chatbot can produce a convincing turn and still forget **who it is with, what should remain private, and what kind of relationship is continuing**. Hades starts from that harder question: what would a character runtime need to carry across time without collapsing every person's context into one shared memory?

![A character that continues](content-system-assets/hero.png)

## The problem with a chatbot wrapper

The model is the mouth, not the whole self. A prompt can imitate personality for one turn, but **continuity needs state**: a shared identity substrate, a relationship track for each human, private memories, changing mood, fatigue, circadian rhythm, and the possibility of an inner life while nobody is speaking.

## What Hades Product is

Hades Product is the **product specification and architecture home** for a host-independent, multi-user Hades. It is not the live research instance. The repository makes the boundary explicit so product decisions can be discussed without copying private names, raw conversations, tokens, or host-specific assumptions into public documentation.

## How the model is separated

1. **Shared personality.** Soul, locks, and few-shots describe the character substrate.
2. **Private relationship tracks.** Each account has its own relationship context with the character.
3. **Private memories.** What one human shares should not silently become another human's context.
4. **A product boundary.** Accounts, isolated tracks, and host independence turn one research instance into an architecture that can support more than one person.

![Memory needs boundaries](content-system-assets/supporting-square.png)

## The technical shape

The repository chooses **handwritten product docs plus a small module graph as the source of truth**. FOSSIL captures are useful for provenance and recovering research threads, but they are not a safe substitute for explicit file and state contracts. The intended stack keeps product docs first, then module/state links, then the runtime commit those docs describe.

That ordering matters because memory is not just a storage feature. It is a product boundary: **what persists, for whom, and under which relationship track**. The privacy rules therefore use product terms such as `primary_user`, `person_id`, and role flags rather than private research display names.

## What this preview does not claim

The public repository is a documentation and architecture home, not proof that every linked runtime feature is already shipped. **The story should make the direction understandable without turning a product map into a launch announcement.**

## Review questions

- Can a first-time reader explain shared personality versus private context after twenty seconds?
- Does the copy feel human without implying consciousness, guaranteed memory, or intimacy that the docs do not support?
- Are privacy rules visible before the technical details?
- Does the image title explain the scene without crowding the human/AI relationship?

## Contract used

This preview pins `content-generation-modules@0.1.2` at `cb8c18fa7789e4b651e1f963892bf056b0d3276d`. The canonical README now uses the reviewed images and story on this branch; merge remains the human review gate.
