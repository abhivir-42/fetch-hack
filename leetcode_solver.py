import requests
from uagents import Agent, Context
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the agent
agent = Agent(name="LeetCode_Solver", seed="leetcode_solver_secret_phrase")

def ask_asi1_mini(question: str) -> str:
    """
    Query ASI1 Mini model for coding solutions
    """
    url = "https://api.asi1.ai/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("ASI1_API_KEY")}'
    }

    prompt = f"""Provide the most optimal Python solution for this coding problem:
    
    {question}
    
    Include:
    1. Time and space complexity analysis
    2. Clean, production-quality code
    3. Brief explanation of the approach
    """

    payload = {
        "model": "asi1-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 0
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

    except requests.exceptions.RequestException as e:
        return f"API Request Error: {str(e)}"

    except json.JSONDecodeError:
        return "API Error: Unable to parse JSON response"

@agent.on_event("startup")
async def solve_leetcode_problem(ctx: Context):
    """
    On startup, fetch and solve a LeetCode problem
    """
    problem_statement = "Given an array of integers, return indices of the two numbers such that they add up to a specific target."

    ctx.logger.info(f"Solving LeetCode problem: {problem_statement}")

    solution = ask_asi1_mini(problem_statement)

    if "API Error" in solution:
        ctx.logger.error(f"Solution failed: {solution}")
    else:
        ctx.logger.info(f"Generated Solution:\n{solution}")

if __name__ == "__main__":
    agent.run()
