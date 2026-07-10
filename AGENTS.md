# Public Profile Repository

This repository publishes Bowei Xia's evidence-backed public profile.

## Source Of Truth

- `data/profile.json` is the canonical public profile.
- `resume-src/bowei-xia-resume.tex` is the printable resume source.
- `scripts/build_site.py` generates human and agent outputs under `site/`.

## Agent Contract

1. Read `data/profile.json` before editing prose.
2. Keep evidence URLs attached to every publication, project, or contribution.
3. Never add phone numbers, street addresses, government identifiers, private repository details, or third-party personal information.
4. Do not turn an open pull request into a merged contribution.
5. Run `python3 scripts/build_site.py --check` before committing.
6. Treat generated files under `site/` as outputs; update the canonical profile first.

## Public Endpoints

- `/profile.json`: structured public profile
- `/resume.md`: plain-text resume for agents
- `/llms.txt`: concise discovery document
- `/.well-known/agent-profile.json`: machine-discoverable profile metadata
- `/bowei-xia-resume.pdf`: human-readable PDF
