# Bowei Xia - Public Profile

Evidence-backed public profile, printable resume, and static portfolio for
[subway-jack.github.io/resume](https://subway-jack.github.io/resume/).

## Architecture

`data/profile.json` is the canonical public fact set. The build produces two
interfaces from that source:

- Human: portfolio HTML and a one-page PDF resume.
- Agents: `profile.json`, `resume.md`, `llms.txt`, and
  `.well-known/agent-profile.json`.

Private repositories, phone numbers, addresses, government identifiers, and
third-party personal information are intentionally excluded.

## Commands

```bash
make build
make check
make serve
```

The local preview is served at `http://localhost:4173`.

## Updating Facts

1. Edit `data/profile.json` and keep an evidence URL or source path with every
   publication, project, contribution, and award.
2. Update `resume-src/bowei-xia-resume.tex` when the printable selection changes.
3. Run `make build` and `make check`.

See `AGENTS.md` for the public-data and agent-editing contract.
