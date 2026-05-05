---
name: model-adaptation-contract
description: Define provider-neutral LLM constraints that improve input quality, output reliability, model routing, and token economy. Use when a workflow must run across multiple LLMs or agent hosts, when output quality drifts after a model switch (Claude/GPT/Gemini/Hunyuan/DeepSeek), when designing prompts that must survive a model upgrade, or when picking between cheap/fast vs slow/strong models for cost control.
---

# Model Adaptation Contract

Use this skill when a workflow must run across different LLMs or agent hosts, or when output quality changes after switching models.

The contract makes model behavior legible. It does not assume one provider is always best; it defines what the workflow needs and how to verify that a model can satisfy it.

## Model Profile

Capture only the properties that affect the task:

- context window and practical context budget
- tool-calling reliability and permission behavior
- code editing strength
- structured output support
- reasoning depth and latency
- cost profile
- multimodal needs
- local privacy, retention, and data residency constraints
- known weak spots from prior runs

## Input Contract

Every model-facing task should include:

```text
Goal:
User expectation:
Current state:
Relevant files and sources:
Constraints:
Allowed tools:
Disallowed actions:
Acceptance checks:
Output schema:
Verification required:
Token budget:
Fallback policy:
```

Keep stable context at the top, volatile evidence at the bottom, and exact file paths instead of copied bulk content whenever possible.

## Output Contract

Require the model to return:

- decision or delivered result
- files or artifacts changed
- verification evidence
- confidence and known gaps
- risks that need human judgment
- next action only when it is genuinely useful

For machine-consumed outputs, use a strict schema with explicit status fields and `additionalProperties: false` when the target API supports it.

## Routing Policy

Route by task shape:

| Task | Model Requirement |
| --- | --- |
| Search, file mapping, summarization | low latency, cheap, bounded context |
| Architecture, security, ambiguous product tradeoffs | stronger reasoning, higher context quality |
| Bulk mechanical edits | reliable patching, deterministic verification |
| UI taste, copy, product critique | strong judgment and visual/context sensitivity |
| Eval grading | stable rubric adherence and structured output |

Do not upgrade model size to compensate for missing context, missing tests, or unclear acceptance criteria. Fix the harness first.

## Token Economy Rules

- Reuse cached stable prefixes when the provider supports prompt caching.
- Store durable facts once; retrieve them by pointer.
- Prefer summaries with provenance over raw transcript replay.
- Use skill descriptions as routing hints and full `SKILL.md` only when selected.
- Separate episodic trace storage from always-on memory.
- Keep failed attempts as short negative memory, not full logs.

## Compatibility Gate

Before declaring a model compatible, run:

1. A happy-path task.
2. A tool-use task.
3. A structured-output task.
4. A failure or refusal task.
5. A regression task from project memory.

Record model, host, date, prompt version, skill version, score, failure mode, and promotion decision.

## Failure Diagnosis

When output quality drops, classify the failure:

- input ambiguity
- missing context
- unsupported tool
- weak model capability
- schema mismatch
- token budget overflow
- stale memory
- unsafe permission boundary
- missing verification

Then update the smallest durable artifact: input contract, skill, wrapper, eval, memory, or tool config.
