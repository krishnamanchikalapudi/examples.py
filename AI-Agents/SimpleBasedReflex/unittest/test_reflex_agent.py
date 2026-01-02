from reflex_agent import ReflexAgent

def main():
    reflex_agent = ReflexAgent()
    query = "What is the meaning of life?"
    state = reflex_agent.run(query)
    print(f"Query: {state.query}")
    print(f"Response: {state.response}")

if __name__ == "__main__":
    main()