from fastapi import FastAPI,UploadFile,File,HTTPException
from pydantic import BaseModel
from pathlib import Path
import shutil
from .agent import ProjectAgent
from .ingest import build_memory,ingest_github
from .vector_store import VectorStore
from .config import KNOWLEDGE_DIR

app=FastAPI(title="Engineering Project Memory API")
class Question(BaseModel): question:str
class GitHubRequest(BaseModel): repo_url:str

@app.get("/")
def root(): return {"project":"Engineering Project Memory","status":"running"}

@app.post("/ask")
def ask(x:Question):
    try:
        a,s=ProjectAgent().answer(x.question)
        return {"answer":a,"sources":[{"source":z["source"],"score":round(z["score"],4)} for z in s]}
    except Exception as e: raise HTTPException(500,str(e))

@app.post("/ingest")
def ingest(): build_memory(); return {"status":"success"}

@app.post("/ingest/github")
def github(x:GitHubRequest):
    try:
        c=ingest_github(x.repo_url); VectorStore().add(c); return {"status":"success","chunks_added":len(c)}
    except Exception as e: raise HTTPException(500,str(e))

@app.post("/upload")
async def upload(file:UploadFile=File(...)):
    p=Path(KNOWLEDGE_DIR)/file.filename; p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("wb") as f: shutil.copyfileobj(file.file,f)
    return {"saved":str(p)}
