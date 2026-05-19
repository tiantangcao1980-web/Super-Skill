# Spec: Promote `dev-tool-adapter` from wrapper-gen to runtime contract

- Status: **draft**
- Owner: super-skill maintainers
- Last-updated: 2026-05-19
- Tracked-by: `skills/90-codex-patterns/dev-tool-adapter/SKILL.md`, `bin/super-skill adapt`

## Problem

`bin/super-skill adapt --tool <cursor|trae|windsurf|opencode|claude-code|codex|hermes>` is a one-shot wrapper-code generator. It cannot detect whether the target CLI is installed, negotiate capabilities, or stream tool calls. open-design's `AgentAdapter` interface is the proven design we should converge on.

## Goal

Land a TypeScript reference interface inside `skills/90-codex-patterns/dev-tool-adapter/references/agent-adapter.d.ts`, plus a Python protocol shim in `scripts/super_skill_adapters/`, that downstream tools can implement.

## Interface (v1, mirrors open-design)

```ts
interface AgentAdapter {
  readonly id: string;
  readonly displayName: string;
  detect(): Promise<AgentDetection | null>;
  capabilities(): AgentCapabilities;
  run(params: AgentRunParams): AsyncIterable<AgentEvent>;
  cancel(runId: string): Promise<void>;
  resume?(runId: string, message: string): AsyncIterable<AgentEvent>;
}
```

## Non-goals

- Implementing real adapters for all 7 tools in this PR. We ship the interface + a `null-adapter` reference + `claude-code-adapter` proof-of-concept.
- Replacing `bin/super-skill adapt` codegen; it stays as a fallback for tools that don't implement the interface yet.

## Plan

- [ ] Land the TS type file.
- [ ] Land a Python `super_skill_adapters/protocol.py` mirror.
- [ ] Implement `null-adapter` (always returns `detection=None`).
- [ ] Implement `claude-code-adapter` PATH-scan detection.
- [ ] Add `bin/super-skill adapt --runtime <id> --detect-only` to call the adapter's `detect()` + report.
- [ ] Document the precedence: native adapter > codegen wrapper fallback.

## Acceptance

- `bin/super-skill adapt --runtime claude-code --detect-only --json` returns `{id, version, configDir, skillsDir, authState}` if Claude Code is installed, else returns `null` with a recommendation.
- TS interface compiles with `tsc --noEmit` against the packaged file.
