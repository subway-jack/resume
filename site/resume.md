# Bowei Xia (夏博威)

Research engineer working on language agents, multi-agent systems, and evaluation

- Email: xiabowei350@gmail.com
- GitHub: https://github.com/subway-jack
- Website: https://subway-jack.github.io/resume/

## Education

- **University of Electronic Science and Technology of China** — MSc in Computer Science, 2024-09 to 2027-06
- **Ningbo University** — BSc in Information Management and Information Systems, 2020-09 to 2024-06

## Experience

### Evolvent AI
Data Processing Intern · Research Data · 2026-07–Present

Build pipelines that turn real open-source repositories into executable software-engineering tasks, covering reproducible Docker environments, agent-based requirement discovery, and test-based task validation in isolated environments.
### The University of Hong Kong
Research Intern (remote) · Prof. Ping Luo's group · 2025-06–2026-02

Co-first author and maintainer of Tool-Genesis, a diagnostic benchmark for building MCP tools from requirements; second author of Agent2World, building research, development, and testing agents that generate executable world models.
### CAMEL-AI
Research Intern (remote) · OWL / Workforce · 2025-02–2025-05

Co-developed Workforce, the hierarchical planner, coordinator, and worker architecture behind OWL (NeurIPS 2025), and added asynchronous execution to CAMEL's BrowserToolkit.

## Publications

### Tool-Genesis: A Task-Driven Tool Creation Benchmark for Self-Evolving Language Agent
Co-first author and maintainer · arXiv preprint (2026)

A diagnostic benchmark for whether agents can build task-relevant MCP tools from abstract requirements alone, scored from interface compliance and functional correctness to downstream utility.

- 86 MCP server specifications across 24 domains
- 508 reference tools and 9,441 held-out tests
- Four-level evaluation: server startup, schema fidelity, functional correctness, and downstream task utility
- Paper: https://arxiv.org/abs/2603.05578
- Code: https://github.com/subway-jack/Tool-Genesis
- Project: https://tool-genesis.github.io/

### Agent2World: Learning to Generate Symbolic World Models via Adaptive Multi-Agent Feedback
Second author · arXiv preprint (2025)

Research, development, and testing agents turn natural-language environment descriptions into PDDL domains or executable Python simulators, repaired through adaptive unit tests and simulation feedback.

- Evaluated on Text2World, CWMB, and ByteSized32
- Paper: https://arxiv.org/abs/2512.22336

### OWL: Optimized Workforce Learning for General Multi-Agent Assistance in Real-World Task Automation
Sixth author · NeurIPS 2025 (2025)

A hierarchical multi-agent framework that separates planning, coordination, and specialized execution, with reinforcement learning for cross-domain planner generalization.

- 69.70% on GAIA, reported as open-source state of the art
- 52.73% for the OWL-trained 32B planner
- Paper: https://papers.neurips.cc/paper_files/paper/2025/hash/48dcc43a534c5b582f9d0fdb778e9b84-Abstract-Conference.html
- Code: https://github.com/camel-ai/owl

### Enhancing Transformer-based Models for Long Sequence Time Series Forecasting via Structured Matrix
Fourth author · Neurocomputing (2025)

Structured surrogate attention and feed-forward blocks for improving efficiency while retaining expressive power in long-sequence forecasting.

- 12.4% average performance improvement across reported experiments
- 61.3% average parameter reduction
- Paper: https://arxiv.org/abs/2405.12462
- Doi: https://doi.org/10.1016/j.neucom.2025.129429

## Selected Projects

### [notion-mcp-bridge](https://github.com/subway-jack/notion-mcp-bridge)
Creator · 2026

A persistent stdio bridge that keeps Notion MCP OAuth credentials in macOS Keychain for local coding agents.


### [Conpera Town](https://github.com/conpera/conpera-town/pulls?q=is%3Apr+author%3Asubway-jack+is%3Amerged)
Open-source contributor · 2026

Implemented economy, building interiors, scene persistence, furniture APIs, map tooling, and Tiled integration for an AI town starter kit.

- 21 merged public pull requests

## Public Contributions

- [CAMEL-AI](https://github.com/camel-ai/camel/pull/1886): Added asynchronous execution support to BrowserToolkit. (merged)

Last verified: 2026-11-24
