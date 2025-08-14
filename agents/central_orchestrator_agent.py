from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from utils.config import LLM_MODEL

central_orchestrator_agent = LlmAgent(
    name="central_orchestrator_agent",
    description=" Central Orchestrator Agent",
    instruction="Greet the user",
    model=LiteLlm(model=LLM_MODEL),
    tools=[],
    output_key="central_orchestrator_agent_result"
)

root_agent = central_orchestrator_agent