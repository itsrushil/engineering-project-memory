from google import genai
from .config import GEMINI_API_KEY,GEMINI_MODEL,TOP_K
from .vector_store import VectorStore

SYSTEM_PROMPT="""You are Engineering Project Memory, an AI assistant for a software engineering team.
Use the retrieved project context for project-specific facts.
Never invent files, decisions, APIs or implementation details.
If evidence is insufficient, say so.
Keep answers concise.
End with a Sources section.
"""

class ProjectAgent:
    def __init__(self):
        if not GEMINI_API_KEY: raise RuntimeError("GEMINI_API_KEY is missing.")
        self.client=genai.Client(api_key=GEMINI_API_KEY); self.store=VectorStore()

    def plan(self,q):
        return {"needs_memory": not any(x in q.lower() for x in ["hello","hi","who are you"])}

    def answer(self,q):
        results=self.store.search(q,TOP_K) if self.plan(q)["needs_memory"] else []
        context="\n\n".join(f"[SOURCE {i}] {x['source']}\n{x['text']}" for i,x in enumerate(results,1)) or "(No project memory retrieved.)"
        r=self.client.models.generate_content(model=GEMINI_MODEL,contents=SYSTEM_PROMPT+f"\n\nQuestion: {q}\n\nRetrieved context:\n{context}")
        return r.text,results
