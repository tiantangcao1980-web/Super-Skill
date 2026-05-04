# everything-claude-code and Superpowers Analysis

This pass studied:

- `affaan-m/everything-claude-code`
- `obra/superpowers`

The goal was not to import them wholesale. The useful pattern is to turn their engineering lessons into Super Skill native surfaces that improve LLM input quality, context quality, output quality, and verification quality.

## What Was Learned

### everything-claude-code

Strong ideas:

- Selective install should be profile/component driven, not all-or-nothing.
- A read-only install plan should exist before filesystem mutation.
- Capabilities should land on the smallest useful surface: rule, skill, CLI, MCP, or direct API.
- External ideas should be adapted into local naming and validation rules instead of shipped as upstream-branded wrappers.
- Security posture belongs in the repository lifecycle: install scripts, hooks, MCP config, and secrets all need scanable contracts.

Applied in Super Skill:

- Added `manifests/install-profiles.json`.
- Added `manifests/install-components.json`.
- Added `bin/super-skill plan`.
- Added `bin/super-skill audit`.
- Added `selective-install-planning`.

### obra/superpowers

Strong ideas:

- Workflows are mandatory only when they are tied to evidence.
- TDD applies to code and to skill evolution: prove the failure, make the minimal change, verify again.
- Debugging should start with reproduction and root cause, not patches.
- Completion requires fresh verification evidence.
- Plans should be small enough for independent execution and review.

Applied in Super Skill:

- Added `test-driven-development`.
- Strengthened `debugging` with root-cause phases.
- Strengthened `skill-authoring-system` with a skill evolution loop.
- Kept `verification-loop` as the completion gate.

## Reinterpreted For LLM I/O Quality

The combined lesson is that AI-agent work needs an explicit I/O contract:

- input starts with user expectation, not prompt text alone
- context is curated into a compact working set instead of dumped wholesale
- execution is staged and evidence-driven
- output is judged against the user's desired outcome
- long sessions preserve decisions, risks, and current state rather than raw chronology

Applied in Super Skill:

- Added `intent-contract`.
- Added `context-engineering`.
- Added `output-quality-gate`.
- Added `token-budgeting`.

## De-Duplication Decisions

- Did not vendor either external repository into `skills/`.
- Did not add a second `systematic-debugging` skill because `debugging` already owned that trigger surface.
- Did not add a second `writing-skills` skill because `skill-authoring-system` already owned authoring and packaging.
- Kept Cowork under `vendor/cowork/` because its duplicate names are domain-source material, not flat installable skills.

## Compatibility Decisions

- DesignDNA compatibility symlinks remain part of the checked audit contract.
- Installable skills keep a unique flat namespace for Codex, Claude, and similar runtimes.
- Profiles remain lifecycle-stage based so existing users can keep using `core`, `dev`, `design`, and `all`.

## Security and Reliability Decisions

- `validate` remains structural: frontmatter, links, references, duplicate installable names.
- `audit` is broader: manifests, compatibility symlinks, executable entrypoints, secret-like values, and risky shell/documentation patterns.
- Risky command patterns are reported as findings rather than automatic failures because some are intentionally documented as warnings or examples.
- Hardcoded secret-like values, broken compatibility links, invalid manifests, and missing executable entrypoints fail the audit.
