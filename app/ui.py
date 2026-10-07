import time
import io
import os
import gradio as gr
from pathlib import Path
from google import genai
from .config import GEMINI_API_KEY, GEMINI_MODEL, KNOWLEDGE_DIR
from .agent import ProjectAgent
from .ingest import build_memory


# -----------------------------
# Core functions
# -----------------------------

def ask(q):
    if not q or not q.strip():
        return "Enter a question first.", ""

    last_error = None
    for attempt in range(3):
        try:
            answer, sources = ProjectAgent().answer(q)
            source_text = "\n".join(
                f"- `{x['source']}`  ·  relevance {x['score']:.3f}"
                for x in sources
            ) or "No matching sources were returned."

            return answer, source_text
        except Exception as e:
            last_error = e
            if attempt < 2:
                time.sleep(4 * (attempt + 1))

    return (
        "Gemini is temporarily unavailable. Please try again later.",
        f"Technical details: `{last_error}`"
    )


def rebuild():
    build_memory()
    return "Memory rebuilt successfully from the files in `data/knowledge/`."


def upload_and_ingest(files):
    if not files:
        return "Please select one or more files first."

    saved = []
    knowledge_dir = Path(KNOWLEDGE_DIR)
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    for file_path in files:
        src = Path(file_path)
        dest = knowledge_dir / src.name
        dest.write_bytes(src.read_bytes())
        saved.append(src.name)

    build_memory()

    return (
        f"### Ingestion complete\n\n"
        f"**{len(saved)} file(s)** added to project memory.\n\n"
        + "\n".join(f"- `{name}`" for name in saved)
        + "\n\nMemory rebuilt successfully."
    )


def github(url):
    if not url or not url.strip():
        return "Enter a public GitHub repository URL first."

    try:
        from .ingest import ingest_github
        from .vector_store import VectorStore

        chunks = ingest_github(url.strip())
        VectorStore().add(chunks)

        return (
            f"### Repository indexed\n\n"
            f"**{len(chunks)} chunks** were added to project memory."
        )

    except Exception as e:
        return f"GitHub ingestion failed:\n\n`{e}`"

def image_ai(image):
    if image is None:
        return "Upload an architecture diagram first."

    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="PNG")
    image_bytes = buffer.getvalue()

    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = (
        "Analyze this software architecture diagram.\n\n"
        "1. Identify the main components.\n"
        "2. Explain the data flow from user input to final output.\n"
        "3. Explain the role of the AI Agent, RAG Retriever, vector store, and Gemini LLM.\n"
        "4. Mention important APIs, databases, or storage shown.\n"
        "5. Give a concise overall architecture summary.\n\n"
        "Only describe what is visible in the diagram. Clearly state when something is not shown."
    )

    last_error = None
    for attempt in range(3):
        try:
            image_part = genai.types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/png",
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
        "Gemini could not analyze the image right now.\n\n"
        f"Technical details: `{last_error}`"
    )


# -----------------------------
# Professional UI
# -----------------------------

CSS = """
:root {
    --bg: #090d16;
    --panel: #101827;
    --panel-soft: #0d1421;
    --border: #263650;
    --border-soft: #1b2940;
    --text: #eef3fb;
    --muted: #9aa9bf;
    --blue: #6ea8ff;
    --violet: #9b7cff;
}

.gradio-container {
    max-width: 1240px !important;
    margin: 0 auto !important;
    padding: 18px 26px 8px !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

body {
    background: var(--bg) !important;
}

#hero {
    padding: 28px 30px 24px;
    border: 1px solid var(--border);
    border-radius: 18px;
    background:
        radial-gradient(circle at 88% 12%, rgba(155,124,255,.18), transparent 30%),
        radial-gradient(circle at 60% 100%, rgba(110,168,255,.10), transparent 32%),
        linear-gradient(135deg, #111a2b 0%, #0c1320 100%);
    margin-bottom: 14px;
    box-shadow: 0 12px 35px rgba(0,0,0,.20);
}

#hero h1 {
    font-size: 39px;
    line-height: 1.1;
    letter-spacing: -1.1px;
    margin: 0 0 8px;
    color: #f5f7fc;
}

.hero-sub {
    color: #aebbd0;
    font-size: 15px;
    max-width: 820px;
    line-height: 1.55;
}

.badges {
    margin-top: 14px;
    display: flex;
    gap: 7px;
    flex-wrap: wrap;
}

.badge {
    display: inline-block;
    border: 1px solid #304461;
    background: rgba(18,30,49,.85);
    border-radius: 999px;
    padding: 5px 10px;
    color: #c8d5e8;
    font-size: 12px;
}

.feature-row {
    margin: 0 0 14px !important;
}

.feature-card {
    border: 1px solid var(--border-soft);
    border-radius: 13px;
    background: linear-gradient(145deg, #111a29, #0d1420);
    padding: 12px 15px;
}

.feature-title {
    color: #edf3fb;
    font-size: 14px;
    font-weight: 650;
    margin-bottom: 3px;
}

.feature-text {
    color: #8f9fb7;
    font-size: 12px;
    line-height: 1.4;
}

.section-title {
    color: #eef3fb;
    font-size: 20px;
    font-weight: 650;
    margin: 5px 0 3px;
}

.section-note {
    color: var(--muted);
    font-size: 14px;
    line-height: 1.45;
    margin-bottom: 9px;
}

textarea, input {
    background: #0b1220 !important;
    border: 1px solid #2a3b57 !important;
    color: #edf3fb !important;
    font-size: 14px !important;
}

textarea:focus, input:focus {
    border-color: #6b8fd1 !important;
    box-shadow: 0 0 0 1px rgba(110,168,255,.15) !important;
}

label {
    color: #cbd6e6 !important;
    font-size: 13px !important;
}

button.primary {
    border-radius: 9px !important;
    background: linear-gradient(90deg, #5f8eea, #8067df) !important;
    border: 0 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    box-shadow: 0 7px 18px rgba(83,111,190,.20) !important;
}

button.primary:hover {
    filter: brightness(1.08);
}

button {
    border-radius: 9px !important;
}

#answer-box, #source-box, #analysis-box, #status-box {
    border: 1px solid var(--border-soft);
    border-radius: 12px;
    background: #0b1220;
    padding: 10px 13px;
    min-height: 105px;
}

#workflow {
    border: 1px solid var(--border);
    border-radius: 15px;
    background: linear-gradient(135deg, #0e1726, #0b121e);
    padding: 15px 18px;
    margin-top: 12px;
}

.workflow-title {
    color: #eaf0fa;
    font-size: 15px;
    font-weight: 650;
    margin-bottom: 9px;
}

.workflow-step {
    color: #9eacc1;
    font-size: 12px;
    line-height: 1.45;
}

.workflow-step b {
    color: #d8e2f0;
}

.tab-nav {
    border-bottom: 1px solid #23324a !important;
    margin-bottom: 10px !important;
}

.tab-nav button {
    color: #94a3b8 !important;
    font-size: 14px !important;
    padding: 9px 16px !important;
}

.tab-nav button.selected {
    color: #edf3fb !important;
    border-bottom: 2px solid #7e91ee !important;
}

footer {
    display: none !important;
}

.gradio-row {
    gap: 14px !important;
}
"""

with gr.Blocks(
    title="Engineering Project Memory",
) as demo:

    gr.HTML("""
    <div id="hero">
        <h1>Engineering Project Memory</h1>
        <div class="hero-sub">
            A practical knowledge assistant for software projects.
            Search project documents, source code and repositories using
            retrieval-augmented generation, with support for architecture images.
        </div>
        <div class="badges">
            <span class="badge">RAG</span>
            <span class="badge">Gemini</span>
            <span class="badge">AI Agent</span>
            <span class="badge">Multimodal</span>
            <span class="badge">FastAPI</span>
            <span class="badge">Gradio</span>
        </div>
    </div>
    """)

    gr.HTML("""
    <div class="feature-row">
      <div style="display:flex;gap:12px;flex-wrap:wrap;">
        <div class="feature-card" style="flex:1;min-width:210px;">
          <div class="feature-title">Retrieve</div>
          <div class="feature-text">Find relevant project context before answering.</div>
        </div>
        <div class="feature-card" style="flex:1;min-width:210px;">
          <div class="feature-title">Reason</div>
          <div class="feature-text">Use a simple query planner for project-specific questions.</div>
        </div>
        <div class="feature-card" style="flex:1;min-width:210px;">
          <div class="feature-title">Understand</div>
          <div class="feature-text">Analyze architecture images alongside project knowledge.</div>
        </div>
      </div>
    </div>
    """)


    with gr.Tabs():

        with gr.Tab("Project Memory"):
            gr.Markdown("### Ask your project")
            gr.Markdown(
                "Ask questions about the indexed project knowledge. "
                "Answers are generated using retrieved project context.",
                elem_classes="section-note",
            )

            with gr.Row():
                with gr.Column(scale=5):
                    question = gr.Textbox(
                        label="Question",
                        placeholder="e.g. Why did we choose PostgreSQL?",
                        lines=3,
                    )
                    ask_button = gr.Button(
                        "Ask Project Memory",
                        variant="primary",
                    )

                with gr.Column(scale=3):
                    gr.Markdown(
                        "**Try asking**\n\n"
                        "• Where is authentication implemented?\n\n"
                        "• What happens when a user registers?\n\n"
                        "• Which components depend on payment?",
                    )

            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Answer")
                    answer = gr.Markdown(
                        "Your answer will appear here.",
                        elem_id="answer-box",
                    )
                with gr.Column():
                    gr.Markdown("### Sources")
                    sources = gr.Markdown(
                        "Retrieved sources will appear here.",
                        elem_id="source-box",
                    )

            ask_button.click(
                ask,
                question,
                [answer, sources],
                show_progress="minimal",
                api_name="ask_project",
            )

        with gr.Tab("GitHub"):
            gr.Markdown("### Add a repository")
            gr.Markdown(
                "Index a public GitHub repository and make its supported files searchable.",
                elem_classes="section-note",
            )

            github_url = gr.Textbox(
                label="Public repository URL",
                placeholder="https://github.com/username/repository",
            )
            github_button = gr.Button("Index Repository", variant="primary")
            github_status = gr.Markdown(
                "Repository status will appear here.",
                elem_id="status-box",
            )

            github_button.click(github, github_url, github_status)

        with gr.Tab("Multimodal"):
            gr.Markdown("### Architecture diagram analysis")
            gr.Markdown(
                "Upload a software architecture diagram and ask Gemini to explain the visible components and flow.",
                elem_classes="section-note",
            )

            with gr.Row():
                with gr.Column():
                    image = gr.Image(
                        type="pil",
                        label="Architecture diagram",
                    )
                    image_button = gr.Button(
                        "Analyze Architecture",
                        variant="primary",
                    )

                with gr.Column():
                    gr.Markdown("### Analysis")
                    analysis = gr.Markdown(
                        "The diagram analysis will appear here.",
                        elem_id="analysis-box",
                    )

            image_button.click(image_ai, image, analysis)

        with gr.Tab("Knowledge"):
            gr.Markdown("### Project knowledge")
            gr.Markdown(
                "Upload documents or source files. They are copied to "
                "`data/knowledge/`, chunked, embedded and added to local project memory.",
                elem_classes="section-note",
            )

            files = gr.File(
                label="Project files",
                file_count="multiple",
                file_types=[
                    ".pdf", ".md", ".txt", ".py", ".js", ".ts",
                    ".java", ".cpp", ".c", ".h", ".json", ".yaml", ".yml"
                ],
                type="filepath",
            )

            ingest_button = gr.Button(
                "Upload & Ingest Files",
                variant="primary",
            )
            ingest_status = gr.Markdown(elem_id="status-box")

            ingest_button.click(
                upload_and_ingest,
                files,
                ingest_status,
            )

            gr.Markdown("---")

            rebuild_button = gr.Button("Rebuild Project Memory")
            rebuild_status = gr.Markdown(elem_id="status-box")

            rebuild_button.click(
                rebuild,
                outputs=rebuild_status,
            )

    gr.HTML("""
    <div id="workflow">
      <div class="workflow-title">Project workflow</div>
      <div style="display:flex;gap:18px;flex-wrap:wrap;">
        <div class="workflow-step"><b>01 · Ingest</b><br>Documents, code and repositories</div>
        <div class="workflow-step"><b>02 · Retrieve</b><br>Embeddings + local vector search</div>
        <div class="workflow-step"><b>03 · Generate</b><br>Grounded Gemini response</div>
        <div class="workflow-step"><b>04 · Explain</b><br>Sources and architecture analysis</div>
      </div>
    </div>
    """)

    gr.Markdown(
        "<div style='text-align:center;color:#71819a;padding:14px 0 2px;font-size:11px;'>"
        "Engineering Project Memory · Academic Project"
        "</div>"
    )

if __name__ == "__main__":
    demo.queue(max_size=20)
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        css=CSS,
    )
