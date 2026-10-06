import time
import io
import requests, gradio as gr
from pathlib import Path
from google import genai
from .config import GEMINI_API_KEY, GEMINI_MODEL, KNOWLEDGE_DIR
from .agent import ProjectAgent
from .ingest import build_memory


def ask(q):
    if not q or not q.strip():
        return "⚠️ Enter a question.", ""

    last_error = None
    # Gemini can temporarily return 503 during demand spikes. Retry automatically.
    for attempt in range(3):
        try:
            a, s = ProjectAgent().answer(q)
            sources = "\n".join(
                f"- {x['source']} (score={x['score']:.3f})" for x in s
            ) or "No sources."
            return a, sources
        except Exception as e:
            last_error = e
            if attempt < 2:
                time.sleep(4 * (attempt + 1))

    return (
        "⚠️ Gemini is temporarily unavailable. Please click **Ask AI** again in a few seconds.",
        f"Technical details: `{last_error}`"
    )


def rebuild():
    build_memory()
    return "Memory rebuilt successfully from the files in data/knowledge/."


def upload_and_ingest(files):
    if not files:
        return "Please select one or more files first."

    saved = []
    knowledge_dir = Path(KNOWLEDGE_DIR)
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    for file_path in files:
        src = Path(file_path)
        # Keep only the filename so uploads cannot create arbitrary paths.
        dest = knowledge_dir / src.name
        dest.write_bytes(src.read_bytes())
        saved.append(src.name)

    build_memory()
    return (
        f"### Ingestion complete\n"
        f"Uploaded: **{len(saved)} file(s)**\n\n"
        + "\n".join(f"- {name}" for name in saved)
        + "\n\n**Memory rebuilt successfully.**"
    )


def github(url):
    try:
        r = requests.post(
            "http://127.0.0.1:8000/ingest/github",
            json={"repo_url": url},
            timeout=120,
        )
        return (
            f"Added {r.json()['chunks_added']} chunks."
            if r.ok
            else r.text
        )
    except Exception as e:
        return f"GitHub ingestion error: {e}"


def image_ai(image):
    if image is None:
        return "⚠️ Upload an architecture diagram first."

    # Use Gradio/PIL image data directly instead of reopening the temporary
    # clipboard file. This avoids Windows PermissionError on clipboard.png.
    buffer = io.BytesIO()
    image = image.convert("RGB")
    image.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()
    mime_type = "image/png"
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = (
        "Analyze this software architecture diagram in detail.\n\n"
        "1. Identify the main components.\n"
        "2. Explain the data flow from user input to final output.\n"
        "3. Explain the role of the AI Agent, RAG Retriever, vector store, and Gemini LLM.\n"
        "4. Mention important APIs, databases, or storage shown.\n"
        "5. Give a concise overall architecture summary.\n\n"
        "Only describe what is visible in the diagram; clearly state if something is not shown."
    )

    last_error = None
    for attempt in range(3):
        try:
            image_part = genai.types.Part.from_bytes(
                data=image_bytes, mime_type=mime_type
            )
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[prompt, image_part],
            )
            return response.text
        except Exception as e:
            last_error = e
            if attempt < 2:
                time.sleep(4 * (attempt + 1))

    return (
        "⚠️ Gemini could not analyze the image after 3 attempts. "
        "Please try Analyze Architecture again in a few seconds.\n\n"
        f"Technical details: `{last_error}`"
    )


with gr.Blocks(title="Engineering Project Memory") as demo:
    gr.Markdown(
        "# 🧠 Engineering Project Memory\n"
        "### AI knowledge assistant for software engineering projects"
    )

    with gr.Tab("💬 Ask Project Memory"):
        q = gr.Textbox(
            label="Ask a project question",
            placeholder="Why did we choose PostgreSQL?",
        )
        b = gr.Button("Ask AI")
        a = gr.Markdown()
        s = gr.Markdown()
        b.click(ask, q, [a, s], show_progress="minimal", api_name="ask_project")

    with gr.Tab("🐙 GitHub"):
        u = gr.Textbox(label="Public GitHub repository URL")
        b2 = gr.Button("Ingest Repository")
        st = gr.Markdown()
        b2.click(github, u, st)

    with gr.Tab("🖼️ Multimodal AI"):
        im = gr.Image(type="pil", label="Architecture diagram")
        b3 = gr.Button("Analyze Architecture")
        out = gr.Markdown()
        b3.click(image_ai, im, out)

    with gr.Tab("📚 Knowledge"):
        gr.Markdown(
            "Upload project documents or source files. They will be copied to "
            "`data/knowledge/`, chunked, embedded, and added to the local vector memory."
        )
        files = gr.File(
            label="Upload project files",
            file_count="multiple",
            file_types=[
                ".pdf", ".md", ".txt", ".py", ".js", ".ts",
                ".java", ".cpp", ".c", ".h", ".json", ".yaml", ".yml"
            ],
            type="filepath",
        )
        ingest_btn = gr.Button("📥 Upload & Ingest Files")
        ingest_status = gr.Markdown()
        ingest_btn.click(upload_and_ingest, files, ingest_status)

        gr.Markdown("---")
        rebuild_btn = gr.Button("🔄 Build / Rebuild Memory")
        rebuild_status = gr.Markdown()
        rebuild_btn.click(rebuild, outputs=rebuild_status)


if __name__ == "__main__":
    demo.queue(max_size=20)
    demo.launch()
