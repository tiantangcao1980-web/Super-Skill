# Super Skill Live Evals

Live evals are deterministic local validation projects. Each recipe creates a temporary project workspace, runs code-based graders, probes the memory hook, and then deletes the workspace unless `--keep` is used.

Run:

```bash
bin/super-skill live-evals --json
```

These are not model benchmarks yet. They are the executable harness layer that a later LLM pass can target.
