import requests
import json
from requests.auth import HTTPBasicAuth
from typing import Dict, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.config import JIRA_BASE_URL, EMAIL, API_TOKEN

BOARD_ID = "1"  # Your board ID

class JiraAPI:
    def __init__(self, base_url: str, email: str, api_token: str):
        """
        Initialize Jira API client
        
        Args:
            base_url: Your Jira instance URL (e.g., 'https://yourcompany.atlassian.net')
            email: Your Jira account email
            api_token: Your Jira API token (generate from Account Settings > Security > API tokens)
        """
        self.base_url = base_url.rstrip('/')
        self.auth = HTTPBasicAuth(email, api_token)
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def get_board_data(self, board_id: str) -> Dict:
        """
        Get board information
        
        Args:
            board_id: The ID of the board
            
        Returns:
            Dictionary containing board data
        """
        url = f"{self.base_url}/rest/agile/1.0/board/{board_id}"
        
        try:
            response = requests.get(url, auth=self.auth, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching board data: {e}")
            return {}
    
    def get_board_issues(self, board_id: str, max_results: int = 50, 
                        start_at: int = 0, jql: str = "") -> Dict:
        """
        Get issues from a specific board
        
        Args:
            board_id: The ID of the board
            max_results: Maximum number of results to return (default: 50)
            start_at: Starting index for pagination (default: 0)
            jql: JQL query to filter results (optional)
            
        Returns:
            Dictionary containing issues data
        """
        url = f"{self.base_url}/rest/agile/1.0/board/{board_id}/issue"
        
        params = {
            'maxResults': max_results,
            'startAt': start_at
        }
        
        if jql:
            params['jql'] = jql
            
        try:
            response = requests.get(url, auth=self.auth, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching board issues: {e}")
            return {}
    
    def get_all_boards(self, max_results: int = 50) -> List[Dict]:
        """
        Get all boards accessible to the user
        
        Args:
            max_results: Maximum number of results to return
            
        Returns:
            List of board dictionaries
        """
        url = f"{self.base_url}/rest/agile/1.0/board"
        params = {'maxResults': max_results}
        
        try:
            response = requests.get(url, auth=self.auth, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('values', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching boards: {e}")
            return []
    
    def get_sprints(self, board_id: str) -> List[Dict]:
        """
        Get sprints for a specific board
        
        Args:
            board_id: The ID of the board
            
        Returns:
            List of sprint dictionaries
        """
        url = f"{self.base_url}/rest/agile/1.0/board/{board_id}/sprint"
        
        try:
            response = requests.get(url, auth=self.auth, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get('values', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching sprints: {e}")
            return []
    
    def get_issue_details(self, issue_key: str) -> Dict:
        """
        Get detailed information about a specific issue
        
        Args:
            issue_key: The key of the issue (e.g., 'PROJ-123')
            
        Returns:
            Dictionary containing issue details
        """
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"
        
        try:
            response = requests.get(url, auth=self.auth, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching issue details: {e}")
            return {}
    
    def search_issues(self, jql: str, max_results: int = 50, fields: List[str] = None) -> Dict:
        """
        Search for issues using JQL
        
        Args:
            jql: JQL query string
            max_results: Maximum number of results to return
            fields: List of fields to include in response
            
        Returns:
            Dictionary containing search results
        """
        url = f"{self.base_url}/rest/api/3/search"
        
        payload = {
            'jql': jql,
            'maxResults': max_results,
            'startAt': 0
        }
        
        if fields:
            payload['fields'] = fields
        
        try:
            response = requests.post(url, auth=self.auth, headers=self.headers, 
                                   data=json.dumps(payload))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching issues: {e}")
            return {}

def format_issue_data(issues_data: Dict) -> None:
    """
    Pretty print issue data
    
    Args:
        issues_data: Dictionary containing issues from API response
    """
    if not issues_data or 'issues' not in issues_data:
        print("No issues found")
        return
    
    issues = issues_data['issues']
    print(f"Found {len(issues)} issues:")
    print("-" * 80)
    
    for issue in issues:
        key = issue['key']
        summary = issue['fields']['summary']
        status = issue['fields']['status']['name']
        assignee = issue['fields'].get('assignee')
        assignee_name = assignee['displayName'] if assignee else 'Unassigned'
        
        print(f"Key: {key}")
        print(f"Summary: {summary}")
        print(f"Status: {status}")
        print(f"Assignee: {assignee_name}")
        print("-" * 40)

# Example usage
if __name__ == "__main__":
    
    # Initialize Jira API client
    jira = JiraAPI(JIRA_BASE_URL, EMAIL, API_TOKEN)
    
    # Example 1: Get all available boards
    print("=== Available Boards ===")
    boards = jira.get_all_boards()
    for board in boards:
        print(f"ID: {board['id']}, Name: {board['name']}, Type: {board['type']}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Get board information
    print(f"=== Board Information (ID: {BOARD_ID}) ===")
    board_info = jira.get_board_data(BOARD_ID)
    if board_info:
        print(f"Name: {board_info.get('name', 'N/A')}")
        print(f"Type: {board_info.get('type', 'N/A')}")
        print(f"Location: {board_info.get('location', {}).get('displayName', 'N/A')}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Get issues from board
    print(f"=== Board Issues (ID: {BOARD_ID}) ===")
    issues = jira.get_board_issues(BOARD_ID, max_results=10)
    format_issue_data(issues)
    
    print("\n" + "="*50 + "\n")
    
    # Example 4: Search issues with JQL
    print("=== Search Issues (Open Issues) ===")
    jql_query = "status != Done ORDER BY created DESC"
    search_results = jira.search_issues(jql_query, max_results=5)
    format_issue_data(search_results)
    
    print("\n" + "="*50 + "\n")
    
    # Example 5: Get sprints for the board
    print(f"=== Sprints for Board (ID: {BOARD_ID}) ===")
    sprints = jira.get_sprints(BOARD_ID)
    for sprint in sprints:
        print(f"ID: {sprint['id']}, Name: {sprint['name']}, State: {sprint['state']}")