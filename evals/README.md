# Super Skill Capability Evals

These validation projects test whether Super Skill still supports the original goal: a full lifecycle, AI-agent-ready skill collection that improves LLM input/output quality, supports multiple developer tools, keeps memory durable but controlled, and closes the harness engineering loop.

Run:

```bash
bin/super-skill evals --json
```

The projects are intentionally small and deterministic. They do not claim a model will always produce a perfect final app; they verify that the required skills, policies, plugin surfaces, and repeatable checks exist for an agent to execute the workflow.
