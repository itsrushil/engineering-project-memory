import json
from pathlib import Path
import numpy as np
from google import genai
from .config import GEMINI_API_KEY, EMBEDDING_MODEL, VECTOR_DIR

class VectorStore:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env.")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.path = Path(VECTOR_DIR)
        self.path.mkdir(parents=True, exist_ok=True)
        self.file = self.path / "index.json"
        self.data = json.loads(self.file.read_text()) if self.file.exists() else {"chunks":[],"embeddings":[]}

    def save(self):
        self.file.write_text(json.dumps(self.data))

    def embed(self, texts):
        out = []
        for text in texts:
            r = self.client.models.embed_content(model=EMBEDDING_MODEL, contents=text)
            out.append(r.embeddings[0].values)
        return out

    def clear(self):
        self.data = {"chunks":[],"embeddings":[]}
        self.save()

    def add(self, chunks):
        if not chunks: return
        for c, e in zip(chunks, self.embed([x.text for x in chunks])):
            self.data["chunks"].append(c.to_dict())
            self.data["embeddings"].append(e)
        self.save()

    def search(self, query, top_k=5):
        if not self.data["chunks"]: return []
        q = np.array(self.embed([query])[0], dtype=np.float32)
        m = np.array(self.data["embeddings"], dtype=np.float32)
        scores = m @ q / ((np.linalg.norm(m,axis=1)*(np.linalg.norm(q) or 1))+1e-8)
        ids = np.argsort(scores)[::-1][:top_k]
        return [{**self.data["chunks"][int(i)], "score":float(scores[int(i)])} for i in ids]
