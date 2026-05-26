import streamlit as st
from pathlib import Path
import os
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FileForge",
    page_icon="🗂️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}
.stApp {
    background: #0a0a0f;
    color: #e8e4f0;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 2rem 4rem; max-width: 780px; }

/* ── Hero Banner ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #7c6af5;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-size: 3.6rem;
    font-weight: 800;
    line-height: 1.05;
    background: linear-gradient(135deg, #c8b8ff 0%, #7c6af5 45%, #4ecdc4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #6b6480;
    margin-top: 0.9rem;
    letter-spacing: 0.04em;
}
.hero-line {
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, #7c6af5, #4ecdc4);
    margin: 1.8rem auto 0;
    border-radius: 2px;
}

/* ── Operation Selector ── */
.op-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin: 2rem 0 1.5rem;
}
.op-card {
    background: #12111a;
    border: 1.5px solid #1e1c2e;
    border-radius: 14px;
    padding: 1.2rem 0.5rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}
.op-card:hover {
    border-color: #7c6af5;
    transform: translateY(-3px);
    box-shadow: 0 8px 28px rgba(124,106,245,0.18);
}
.op-card.active {
    border-color: #7c6af5;
    background: #1a1630;
    box-shadow: 0 0 0 1px #7c6af580, 0 8px 32px rgba(124,106,245,0.22);
}
.op-icon { font-size: 1.6rem; display: block; margin-bottom: 0.4rem; }
.op-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #8a85a0;
}
.op-card.active .op-label { color: #c8b8ff; }

/* ── Panel ── */
.panel {
    background: #0f0e18;
    border: 1.5px solid #1e1c2e;
    border-radius: 18px;
    padding: 2rem;
    margin-top: 0.5rem;
    position: relative;
}
.panel-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 1.6rem;
    padding-bottom: 1.1rem;
    border-bottom: 1px solid #1a1828;
}
.panel-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7c6af5, #4ecdc4);
    flex-shrink: 0;
}
.panel-title {
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #c8b8ff;
    margin: 0;
}

/* ── Toast messages ── */
.toast-success {
    background: linear-gradient(135deg, #0d2e1a, #0d2e2a);
    border: 1px solid #1a5c35;
    border-left: 4px solid #2de08a;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #2de08a;
    margin: 1rem 0;
}
.toast-error {
    background: linear-gradient(135deg, #2a0d0d, #2a1a0d);
    border: 1px solid #5c1a1a;
    border-left: 4px solid #f05252;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #f05252;
    margin: 1rem 0;
}
.toast-info {
    background: linear-gradient(135deg, #0d1a2e, #0d1a2a);
    border: 1px solid #1a3a5c;
    border-left: 4px solid #4ecdc4;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #4ecdc4;
    margin: 1rem 0;
}

/* ── File content viewer ── */
.file-viewer {
    background: #080810;
    border: 1px solid #1a1828;
    border-radius: 12px;
    padding: 1.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #b0a8d0;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 320px;
    overflow-y: auto;
    margin-top: 1rem;
}
.file-viewer::-webkit-scrollbar { width: 5px; }
.file-viewer::-webkit-scrollbar-track { background: #0f0e18; }
.file-viewer::-webkit-scrollbar-thumb { background: #2a2840; border-radius: 10px; }

/* ── Meta bar ── */
.meta-bar {
    display: flex;
    gap: 1.5rem;
    margin-top: 1rem;
    padding-top: 0.9rem;
    border-top: 1px solid #1a1828;
}
.meta-item {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #4a4660;
}
.meta-val { color: #7c6af5; }

/* ── Input overrides ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #0d0c16 !important;
    border: 1.5px solid #1e1c2e !important;
    border-radius: 10px !important;
    color: #e8e4f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
    padding: 0.65rem 1rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #7c6af5 !important;
    box-shadow: 0 0 0 3px rgba(124,106,245,0.12) !important;
}
.stTextInput label, .stTextArea label, .stRadio label, .stSelectbox label {
    font-size: 0.74rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #6b6480 !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #7c6af5, #5a4fd4) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 1.8rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 18px rgba(124,106,245,0.28) !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(124,106,245,0.42) !important;
    background: linear-gradient(135deg, #9880ff, #7c6af5) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* ── Radio as pill selector ── */
.stRadio > div {
    flex-direction: row !important;
    gap: 0.5rem !important;
    flex-wrap: wrap;
}
.stRadio > div > label {
    background: #12111a !important;
    border: 1.5px solid #1e1c2e !important;
    border-radius: 8px !important;
    padding: 0.45rem 1rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
    color: #8a85a0 !important;
}
.stRadio > div > label:hover { border-color: #7c6af5 !important; color: #c8b8ff !important; }

/* ── Divider ── */
.styled-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e1c2e 30%, #1e1c2e 70%, transparent);
    margin: 2rem 0;
}

/* ── Footer ── */
.footer {
    text-align: center;
    margin-top: 3.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #12111a;
}
.footer-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #2e2c40;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
.footer-accent { color: #7c6af5; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ─────────────────────────────────────────────────────
if "operation" not in st.session_state:
    st.session_state.operation = "Create"
if "message" not in st.session_state:
    st.session_state.message = None  # (type, text)
if "file_content" not in st.session_state:
    st.session_state.file_content = None
if "file_meta" not in st.session_state:
    st.session_state.file_meta = None

# ── Helpers ────────────────────────────────────────────────────────────────
def show_toast(type_: str, text: str):
    st.session_state.message = (type_, text)

def render_toast():
    if st.session_state.message:
        t, msg = st.session_state.message
        cls = {"success": "toast-success", "error": "toast-error", "info": "toast-info"}[t]
        icons = {"success": "✓", "error": "✗", "info": "◈"}
        st.markdown(f'<div class="{cls}">{icons[t]}  {msg}</div>', unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Python · File System Manager</div>
    <h1 class="hero-title">FileForge</h1>
    <p class="hero-sub">create · read · update · delete</p>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# ── Operation selector ──────────────────────────────────────────────────────
ops = {
    "Create": ("✦", "Create"),
    "Read":   ("◈", "Read"),
    "Update": ("⟳", "Update"),
    "Delete": ("⊗", "Delete"),
}

cols = st.columns(4)
for i, (op, (icon, label)) in enumerate(ops.items()):
    with cols[i]:
        active_cls = "active" if st.session_state.operation == op else ""
        st.markdown(f"""
        <div class="op-card {active_cls}" id="op_{op}">
            <span class="op-icon">{icon}</span>
            <span class="op-label">{label}</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button(label, key=f"btn_{op}", help=f"Switch to {op}"):
            st.session_state.operation = op
            st.session_state.message = None
            st.session_state.file_content = None
            st.rerun()

st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

# ── Active operation panel ─────────────────────────────────────────────────
op = st.session_state.operation

panel_titles = {
    "Create": "New File",
    "Read":   "Read File",
    "Update": "Update File",
    "Delete": "Delete File",
}

st.markdown(f"""
<div class="panel">
    <div class="panel-header">
        <div class="panel-dot"></div>
        <p class="panel-title">{panel_titles[op]}</p>
    </div>
</div>
""", unsafe_allow_html=True)

render_toast()

# ────────────────────────────────────────────────────────────────────────────
# CREATE
# ────────────────────────────────────────────────────────────────────────────
if op == "Create":
    filename = st.text_input("File Name", placeholder="e.g. notes.txt", key="c_name")
    content  = st.text_area("File Content", placeholder="Write anything…", height=160, key="c_content")

    if st.button("CREATE FILE", key="do_create"):
        if not filename.strip():
            show_toast("error", "Please enter a file name.")
        else:
            path = Path(filename.strip())
            if path.exists():
                show_toast("error", f'"{filename}" already exists.')
            else:
                try:
                    with open(path, "w") as f:
                        f.write(content)
                    size = path.stat().st_size
                    show_toast("success", f'"{filename}" created successfully  ·  {size} bytes written.')
                except Exception as e:
                    show_toast("error", str(e))
        st.rerun()

# ────────────────────────────────────────────────────────────────────────────
# READ
# ────────────────────────────────────────────────────────────────────────────
elif op == "Read":
    filename = st.text_input("File Name", placeholder="e.g. notes.txt", key="r_name")

    if st.button("READ FILE", key="do_read"):
        if not filename.strip():
            show_toast("error", "Please enter a file name.")
        else:
            path = Path(filename.strip())
            if not path.exists():
                show_toast("error", f'"{filename}" does not exist.')
                st.session_state.file_content = None
            else:
                try:
                    content = path.read_text()
                    stat = path.stat()
                    st.session_state.file_content = content
                    st.session_state.file_meta = {
                        "size": stat.st_size,
                        "lines": content.count("\n") + (1 if content else 0),
                        "chars": len(content),
                    }
                    st.session_state.message = ("info", f'Displaying contents of "{filename}"')
                except Exception as e:
                    show_toast("error", str(e))
        st.rerun()

    if st.session_state.file_content is not None:
        render_toast()
        st.session_state.message = None  # prevent double render
        meta = st.session_state.file_meta or {}
        st.markdown(f"""
        <div class="file-viewer">{st.session_state.file_content if st.session_state.file_content else "(empty file)"}</div>
        <div class="meta-bar">
            <span class="meta-item">SIZE <span class="meta-val">{meta.get("size",0)} B</span></span>
            <span class="meta-item">LINES <span class="meta-val">{meta.get("lines",0)}</span></span>
            <span class="meta-item">CHARS <span class="meta-val">{meta.get("chars",0)}</span></span>
        </div>
        """, unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────────
# UPDATE
# ────────────────────────────────────────────────────────────────────────────
elif op == "Update":
    filename = st.text_input("File Name", placeholder="e.g. notes.txt", key="u_name")
    action   = st.radio("Operation", ["Rename", "Append", "Overwrite"], horizontal=True, key="u_action")

    if action == "Rename":
        newname = st.text_input("New File Name", placeholder="e.g. renamed.txt", key="u_new")
        if st.button("RENAME FILE", key="do_rename"):
            if not filename.strip() or not newname.strip():
                show_toast("error", "Both current and new names are required.")
            else:
                path = Path(filename.strip())
                newpath = Path(newname.strip())
                if not path.exists():
                    show_toast("error", f'"{filename}" does not exist.')
                elif newpath.exists():
                    show_toast("error", f'"{newname}" already exists.')
                else:
                    try:
                        path.rename(newpath)
                        show_toast("success", f'Renamed "{filename}" → "{newname}"')
                    except Exception as e:
                        show_toast("error", str(e))
            st.rerun()

    elif action == "Append":
        extra = st.text_area("Content to Append", placeholder="New lines to add…", height=120, key="u_append")
        if st.button("APPEND TO FILE", key="do_append"):
            if not filename.strip():
                show_toast("error", "Please enter a file name.")
            else:
                path = Path(filename.strip())
                if not path.exists():
                    show_toast("error", f'"{filename}" does not exist.')
                else:
                    try:
                        with open(path, "a") as f:
                            f.write("\n" + extra)
                        show_toast("success", f'Content appended to "{filename}".')
                    except Exception as e:
                        show_toast("error", str(e))
            st.rerun()

    elif action == "Overwrite":
        new_content = st.text_area("New Content", placeholder="This will replace all existing content…", height=140, key="u_over")
        if st.button("OVERWRITE FILE", key="do_overwrite"):
            if not filename.strip():
                show_toast("error", "Please enter a file name.")
            else:
                path = Path(filename.strip())
                if not path.exists():
                    show_toast("error", f'"{filename}" does not exist.')
                else:
                    try:
                        with open(path, "w") as f:
                            f.write(new_content)
                        show_toast("success", f'"{filename}" overwritten successfully.')
                    except Exception as e:
                        show_toast("error", str(e))
            st.rerun()

# ────────────────────────────────────────────────────────────────────────────
# DELETE
# ────────────────────────────────────────────────────────────────────────────
elif op == "Delete":
    filename = st.text_input("File Name", placeholder="e.g. notes.txt", key="d_name")

    st.markdown("""
    <div style="background:#1a0a0a;border:1px solid #3a1a1a;border-left:3px solid #f05252;
                border-radius:9px;padding:0.8rem 1rem;margin:0.8rem 0 1.2rem;">
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.76rem;color:#f05252;
                     letter-spacing:0.06em;">
            ⚠  This action is permanent and cannot be undone.
        </span>
    </div>
    """, unsafe_allow_html=True)

    confirm = st.checkbox("I understand this file will be permanently deleted", key="d_confirm")

    if st.button("DELETE FILE", key="do_delete"):
        if not filename.strip():
            show_toast("error", "Please enter a file name.")
        elif not confirm:
            show_toast("error", "Please confirm deletion by checking the box above.")
        else:
            path = Path(filename.strip())
            if not path.exists():
                show_toast("error", f'"{filename}" does not exist.')
            else:
                try:
                    path.unlink()
                    show_toast("success", f'"{filename}" has been permanently deleted.')
                except Exception as e:
                    show_toast("error", str(e))
        st.rerun()

# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <p class="footer-text">Built with <span class="footer-accent">Python</span> + <span class="footer-accent">Streamlit</span></p>
</div>
""", unsafe_allow_html=True)
