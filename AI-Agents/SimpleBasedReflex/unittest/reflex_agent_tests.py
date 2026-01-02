import pytest
from reflex_agent import ReflexAgent, ReflexAgentState

@pytest.fixture
def reflex_agent():
    return ReflexAgent()

def test_reflex_agent_state():
    state = ReflexAgentState("What is the meaning of life?", "The meaning of life is to find happiness.")
    assert state.query == "What is the meaning of life?"
    assert state.response == "The meaning of life is to find happiness."

def test_get_response(reflex_agent):
    query = "What is the meaning of life?"
    response = reflex_agent.get_response(query)
    assert response == "The meaning of life is to find happiness."

def test_get_response_unknown_query(reflex_agent):
    query = "What is the airspeed velocity of an unladen swallow?"
    response = reflex_agent.get_response(query)
    assert response == "I don't know what to say."

def test_run(reflex_agent):
    query = "What is the meaning of life?"
    state = reflex_agent.run(query)
    assert state.query == query
    assert state.response == "The meaning of life is to find happiness."