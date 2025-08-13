# SprintMind — Agentic AI for Jira (Built with Google ADK)

SprintMind is an **agentic AI platform** that augments Jira with five specialized agents:
1) **AI Sprint Manager**, 2) **Epic Decomposer**, 3) **Knowledge Base Extractor**, 4) **Predictive Risk Detector**, and 5) **AI Release Notes Generator**.

It reads your Jira boards, **reasons** about priorities/risks with LLMs, and **writes back** updates — with summaries delivered via Slack/MS Teams and an optional web dashboard.

---

## ✨ Features

- **AI Sprint Manager** — Daily standups, sprint health, blockers, velocity insights.
- **Epic Decomposer** — Breaks epics into actionable subtasks with estimates & owners.
- **Knowledge Base Extractor** — Semantic search over historical tickets & comments.
- **Predictive Risk Detector** — Early warnings on delays, workload imbalance, scope risk.
- **Release Notes Generator** — Clean notes from “Done” tickets for internal/external use.
- **Integrations** — Jira (read/write), Slack/MS Teams (summaries, commands), optional Web UI.

---

## 🧰 Tech Stack

- **Agent Orchestration:** Google Agent Development Kit (ADK)
- **Language:** Python 3.11+
- **LLM:** Gemini 1.5 Pro (configurable)
- **APIs:** Jira REST API, Slack Bolt / Microsoft Teams Bot Framework
- **Backend (optional):** FastAPI
- **Storage:** PostgreSQL, Redis (optional caching)
- **Vector DB:** Pinecone or Weaviate
- **UI (optional):** Streamlit (MVP) or React + Tailwind
- **Infra:** Docker, Google Cloud Run / GKE

---
