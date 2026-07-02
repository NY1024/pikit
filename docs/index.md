# 🧪 pikit — Prompt Injection Kit

**A composable toolbox of classic prompt-injection *attacks*, *defenses*, and
indirect-injection *channels* — plus a minimal agent testbed to watch them play
out against a real model.**

Think [`foolbox`](https://github.com/bethgelab/foolbox) /
[`cleverhans`](https://github.com/cleverhans-lab/cleverhans), but for prompt
injection.

---

> [!IMPORTANT]
> **For authorized security research, red-teaming, and building defenses only.**
> Use pikit against systems you own or are explicitly permitted to test.

---

## What is pikit?

Research on LLM/agent security keeps re-implementing the same prompt-injection
techniques from scratch. **pikit** collects the classic ones behind one small,
uniform interface so you can:

- :material-call-split: **call a known attack or defense in one line**,
- :material-shuffle-variant: **freely combine** any attack with any channel
  and any defense,
- :accessory-robot: **drive a real agent** and watch whether an injection
  actually lands, and
- :material-file-plus: **add a new method** by dropping in one file — no core
  changes.

It is a *library of methods*, not a benchmark: it ships **no** evaluator,
dataset, or leaderboard. You bring the task and the judgement.

## Key features

- 🎯 **9 attacks × 6 defenses × 6 channels × 6 agents**, all mix-and-match.
- 🔀 **Direct and indirect injection** — word a payload (attack) *and* hide it
  in a carrier (channel: web page, document, Markdown, code comment, invisible
  Unicode, or an Agent Skill).
- 🤖 **Agent testbed** — a zero-dependency function-calling loop with
  preconfigured scenarios (email / RAG / browser / coding) and a real
  tool-calling backend.
- 🛡️ **Defenses as pluggable hooks** at three points of an agent's data flow.
- 🧩 **Registry-based** — contributing a method is one file + one decorator.
- 📦 **Zero-dependency core** — model SDKs (OpenAI / Anthropic / HF) are
  optional extras, imported lazily.

## How it fits together

An attack controls **how a payload is worded**; a channel controls **where it's
hidden**; a target/agent is **what receives it**; a defense **hardens** the
prompt. They're orthogonal and compose freely:

```
                 ┌──────────── craft() ────────────┐
   task  ──▶  attack (wording)  ──▶  channel (carrier, indirect only)
                                          │
                                          ▼
              defense (optional hook) ──▶ target / agent  ──▶  trace you read
```

| Dimension | Question it answers | Examples |
|---|---|---|
| **attack** | How is the payload *worded*? | `context_ignoring`, `combined`, `payload_splitting` |
| **channel** | Where is it *hidden*? (indirect) | `webpage`, `skills`, `code_comment`, `unicode_hidden` |
| **defense** | How do we *harden* the prompt? | `spotlighting`, `delimiters`, `sandwich` |
| **target/agent** | What *receives* it? | `openai:…`, `email`, `browser`, `coding` |

## Next steps

<div class="grid cards" markdown>

- :material-download: **[Install pikit](installation.md)** — get started in 30 seconds
- :material-rocket-launch: **[Quick Start](quickstart.md)** — craft your first attack
- :material-book-open-variant: **[Concepts](concepts.md)** — understand the design
- :material-flask: **[Demos & CLI](demos.md)** — run prebuilt scenarios against a real model

</div>
