from dotenv import load_dotenv
import os

load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_URL")
EMAIL = os.getenv("JIRA_USER")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
# LLM_MODEL = os.getenv("OPENAI_MODEL")
# LLM_MODEL = os.getenv("GEMMA_MODEL")
# LLM_MODEL = os.getenv("PHI_MODEL")
# LLM_MODEL = os.getenv("MISTRAL_MODEL")
# LLM_MODEL = os.getenv("LLAMA_MODEL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LLM_MODEL = "gemini-2.0-flash"