from pathlib import Path
import re, requests
from pypdf import PdfReader
from .models import Chunk
from .vector_store import VectorStore
from .config import KNOWLEDGE_DIR, GITHUB_TOKEN

EXTENSIONS={".md",".txt",".py",".js",".ts",".java",".cpp",".c",".h",".json",".yaml",".yml"}

def split_text(text, size=1200, overlap=200):
    text=re.sub(r"\n{3,}","\n\n",text).strip()
    out=[]; start=0
    while start<len(text):
        end=min(len(text),start+size); piece=text[start:end]
        if end<len(text):
            b=max(piece.rfind("\n\n"),piece.rfind("\n"),piece.rfind(". "))
            if b>size*.5: end=start+b+1; piece=text[start:end]
        if piece.strip(): out.append(piece.strip())
        start=max(end-overlap,end)
    return out

def read_file(p):
    if p.suffix.lower()==".pdf":
        return "\n".join(x.extract_text() or "" for x in PdfReader(str(p)).pages)
    return p.read_text(encoding="utf-8",errors="ignore")

def ingest_local():
    chunks=[]
    for p in Path(KNOWLEDGE_DIR).rglob("*"):
        if not p.is_file() or p.name.startswith("."): continue
        if p.suffix.lower() not in EXTENSIONS and p.suffix.lower()!=".pdf": continue
        for n,t in enumerate(split_text(read_file(p))):
            chunks.append(Chunk(t,str(p),"code" if p.suffix.lower() in {".py",".js",".ts",".java",".cpp",".c",".h"} else "document",{"chunk":n}))
    return chunks

def ingest_github(url):
    parts=url.rstrip("/").split("/")
    owner,repo=parts[-2],parts[-1]
    headers={"Authorization":f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    r=requests.get(f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1",headers=headers,timeout=30)
    r.raise_for_status(); chunks=[]
    for item in r.json().get("tree",[]):
        path=item.get("path","")
        if item.get("type")!="blob" or Path(path).suffix.lower() not in EXTENSIONS: continue
        rr=requests.get(f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{path}",timeout=20)
        if rr.status_code!=200: continue
        for n,t in enumerate(split_text(rr.text)):
            chunks.append(Chunk(t,f"github:{owner}/{repo}/{path}","github_code",{"chunk":n}))
        if len(chunks)>=1000: break
    return chunks

def build_memory():
    s=VectorStore(); s.clear(); c=ingest_local(); s.add(c); print(f"Indexed {len(c)} chunks.")

if __name__=="__main__": build_memory()
