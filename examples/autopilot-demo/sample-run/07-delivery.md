## Delivery Plan (stub)
- Dockerfile sketch:
  FROM python:3.11-slim
  WORKDIR /app
  COPY . .
  CMD ["python", "-m", "candidate"]
- CI workflow outline (.github/workflows/ci.yml):
  jobs.test runs `python -m unittest discover` on push and PR; deploy
  job gated on test job and only fires on tags `v*`.
- Feature flag + kill switch:
  env-var DELIVERY_KILL=1 short-circuits the entry point so a runaway
  release can be turned off without redeploy.
- Observability hooks:
  structured JSON logs to stdout; counter for matched-vs-rejected;
  error log carries the trace id from earlier phases.
- Rollback plan:
  previous container tag stays warm; revert by re-pointing the alias.
- Release notes (draft): "Initial MVP slice. See run.json trace stub-8289d02ae1."
- Trace: stub-8289d02ae1

