from langchain.agents import Tool
from langchain.llms import Ollama
from langgraph.graph import StateGraph
from langgraph.graph.state import State

class ReflexAgentState:
    def __init__(self, query: str, response: str):
        self.query = query
        self.response = response
        
class ReflexAgent:
    def __init__(self):
        self.rules = {
            "What is the meaning of life?": "The meaning of life is to find happiness.",
            "How are you?": "I'm good, thanks.",
        }

    def get_response(self, query: str) -> str:
        return self.rules.get(query, "I don't know what to say.")

    def run(self, query: str) -> ReflexAgentState:
        response = self.get_response(query)
        return ReflexAgentState(query, response)
