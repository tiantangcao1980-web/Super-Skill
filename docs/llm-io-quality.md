# LLM Input and Output Quality

LLM quality is shaped more by input contracts, context selection, and verification loops than by prompt length.

## Better Inputs

Use `intent-contract` to convert user language into:

- desired outcome
- audience
- constraints
- output shape
- acceptance checks
- evidence requirements

Use `context-engineering` to provide:

- exact files and source pointers
- current project state
- decisions already made
- open unknowns
- what to ignore

Use `model-adaptation-contract` to provide:

- model profile and routing reason
- allowed tools and disallowed actions
- structured output schema when downstream code consumes the answer
- fallback policy when the model cannot satisfy the task
- compatibility evals before switching default models

## Better Outputs

Use `output-quality-gate` to check:

- Does this satisfy the user's actual expectation?
- Is the result actionable?
- Are tests, commands, links, or inspection evidence included?
- Are risks and gaps explicit?
- Is the answer concise enough for the user to absorb?

Use `dev-tool-adapter` to check:

- whether the runtime uses `SKILL.md`, project rules, agent config, or plugin packaging
- whether tool permissions and memory policies survived conversion
- whether the wrapper points back to the canonical skill

## More Context, Fewer Tokens

Use `token-budgeting` to:

- search before reading
- summarize stable facts
- reference large artifacts by path
- preserve current decisions instead of full chronology
- keep command evidence compact

Use `agent-memory-dream-loop` to:

- store raw traces outside always-on context
- promote only verified lessons into durable memory
- keep negative memory short
- replay failures offline before changing skills or model routes
- delete or expire memories that no longer improve output quality

## Recommended Prompt Shape

```text
Goal:
User expectation:
Current state:
Relevant files/sources:
Constraints:
Acceptance checks:
Output format:
Verification required:
Token budget:
Runtime adapter:
Model profile:
Memory policy:
```

## Recommended Final Shape

```text
Delivered:
Changed files:
Verification:
Known gaps:
Remote/PR/deployment:
```

The final answer should be short unless the user explicitly asks for a full report. The work can be deep; the delivery should be clear.
