from langchain_community.llms import Ollama

llm = Ollama(model = "llama3.1")
print(llm.invoke("Tell me a short joke", stop = ['<|eot_id|>']))