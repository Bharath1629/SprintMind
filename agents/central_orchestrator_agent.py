from google.adk.agents import LlmAgent

central_orchestrator_agent = LlmAgent(
    name="central_orchestrator_agent",
    description=" Central Orchestrator Agent",
    instruction="",
    model="LLM_MODEL",
    tools=[],
    output_key="central_orchestrator_agent_result"
)