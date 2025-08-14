from dotenv import load_dotenv
import os

load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_URL")
EMAIL = os.getenv("JIRA_USER")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
LLM_MODEL = os.getenv("LLM_MODEL")