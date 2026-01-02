from langchain_ollama.llms import OllamaLLM

my_ollama_model = "llama4:scout"  # "llama3.2"

llm_client = OllamaLLM(
    model=my_ollama_model,
    base_url="http://localhost:11434",
    headers={"Content-Type": "application/json"},
    stream=True,
)

llm_client
