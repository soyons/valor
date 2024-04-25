from valor.embedder.ollama import OllamaEmbedder

embedder = OllamaEmbedder(model="phi3")
embeddings = embedder.get_embedding("Embed me")

print(f"Embeddings: {embeddings}")
print(f"Dimensions: {len(embeddings)}")
