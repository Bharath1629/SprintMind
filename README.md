# SprintMind — Agentic AI for Jira (Built with Google ADK)

SprintMind is an **agentic AI platform** that enhances Jira with specialized agents to streamline agile workflows. It connects to your Jira boards, analyzes priorities and risks using LLMs, and delivers summaries and insights through Slack.

---

## ✨ Features

- **AI Sprint Manager**: Provides daily standup summaries, monitors sprint health, identifies blockers, and offers velocity insights.
- **Epic Decomposer**: Breaks down large epics into smaller, manageable user stories and subtasks, complete with suggested estimates and owners.
- **Knowledge Base Extractor**: Performs semantic searches over historical Jira tickets and comments to find relevant solutions and context.
- **Central Orchestrator**: Intelligently routes user requests to the appropriate specialized agent.
- **Jira Integration**: Seamlessly reads and writes to your Jira projects.
- **Slack Integration**: Delivers summaries and allows interaction via Slack commands.
- **Ngrok Support**: Exposes your local Flask bot to the internet for Slack event subscriptions, enabling real-time interaction during development.

---

## 🏛️ Architecture

SprintMind is built around a central orchestrator that coordinates a team of specialized agents:

- **`central_orchestrator_agent`**: The core of the platform, responsible for receiving user requests and delegating them to the appropriate sub-agent.
- **`sprint_manager_agent`**: Acts as an AI Scrum Master, analyzing Jira data to provide daily updates and risk assessments.
- **`epic_decomposer_agent`**: Assists with sprint planning by breaking down epics into detailed user stories.
- **`kb_extractor_agent`**: Functions as a knowledge base, retrieving insights from past Jira tickets.
- **Slack Bot + Ngrok**: Slack messages are routed to your local Flask bot via a secure ngrok tunnel, which then communicates with ADK agents and Jira.

  ![sprintMind](https://github.com/user-attachments/assets/da9366c6-602a-4e5e-8abb-69ea1a60e122)


---

## 🧰 Tech Stack

- **Agent Orchestration**: Google Agent Development Kit (ADK)
- **Language**: Python
- **LLM**: LiteLLM (configurable)
- **APIs**: Jira REST API, Slack API
- **Backend**: Flask
- **Ngrok**: Secure tunneling to expose local server for Slack

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Jira account with API access
- Slack workspace with bot integration
- Ngrok account (for exposing local server)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Bharath1629/SprintMind.git
    cd SprintMind
    ```

2. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure the environment variables:**

    Create a `.env` file in the root of the project and add the following:

    ```
    JIRA_BASE_URL="https://your-domain.atlassian.net"
    EMAIL="your-jira-email@example.com"
    API_TOKEN="your-jira-api-token"
    SLACK_BOT_TOKEN="your-slack-bot-token"
    LLM_MODEL="your-llm-model" # e.g., "gemini-2.5-pro", "huggingface/openai/gpt-oss-120b"
    ```

---

### Running the Application

1. **Start ngrok to expose your local server:**
    ```bash
    ngrok http 3000
    ```
    Copy the `https` URL provided by ngrok and use it as the **Request URL** in your Slack App’s Event Subscriptions.

2. **Start the Slack bot:**
    ```bash
    python slack_adk_bot_sessions.py
    ```
    The bot will automatically fetch its Slack user ID and manage per-user ADK sessions.

3. **Start the ADK agent server:**
    ```bash
    # Example (depends on your ADK setup):
    adk run
    ```

4. **Verify everything is working:**
   - Check that sessions are created per user.
   - Test Slack commands like:
     - `@SprintMind summarize the current sprint`
     - `@SprintMind decompose epic PROJ-123`
     - `@SprintMind find tickets related to "database connection error"`

---

## 💬 Usage

Once the application is running, you can interact with it from your Slack workspace. Mention the bot in a channel and provide a command. The bot will:

1. Receive the Slack message.
2. Create or retrieve a session for the user in ADK.
3. Route the request to the appropriate agent.
4. Retrieve a response and post it back in the Slack channel.

---

## ⚡ Notes

- **Sessions**: Each Slack user gets a unique session in ADK to maintain conversation context.
- **Error Handling**: Slack API errors (like `invalid_auth`) usually indicate a misconfigured token.
- **Ngrok**: Required for local development. In production, use a proper HTTPS endpoint.

---

## 📄 License

MIT License
