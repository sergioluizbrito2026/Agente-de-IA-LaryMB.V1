import datetime
import logging
import sqlite3
from pathlib import Path

import streamlit as st
from groq import Groq

# ============================================================
# LARYMB AI
# Intelligent AI Platform
# Versão 3.0
# ============================================================

st.set_page_config(
    page_title="LaryMB",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CONFIGURAÇÕES
# ============================================================

APP_NAME = "LaryMB"
APP_VERSION = "3.0.0"

MODEL_NAME = "llama-3.3-70b-versatile"
DB_PATH = Path("larymb.db")

MAX_HISTORY_MESSAGES = 30
MAX_RESPONSE_TOKENS = 4096

SUPPORT_EMAIL = "sergiolmendes2026@gmail.com"
SUPPORT_PHONE = "5511994376755"

# ============================================================
# LOG
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("larymb")

# ============================================================
# ESTILO VISUAL
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at 50% 0%, rgba(124, 58, 237, 0.08), transparent 35%), #0b0d12;
        color: #f8fafc;
    }
    .main .block-container {
        max-width: 1100px;
        padding-top: 1.5rem;
        padding-bottom: 7rem;
    }
    [data-testid="stSidebar"] {
        background: #101217;
        border-right: 1px solid #232832;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }
    [data-testid="stSidebar"] .stButton > button {
        background: transparent;
        border: 1px solid transparent;
        color: #cbd5e1;
        text-align: left;
        border-radius: 9px;
        min-height: 40px;
        font-size: 13px;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #191d25;
        border-color: #2b3140;
        color: #ffffff;
    }
    .larymb-logo {
        font-size: 27px;
        font-weight: 750;
        letter-spacing: -0.8px;
        color: #ffffff;
    }
    .larymb-logo span {
        color: #8b5cf6;
    }
    .larymb-version {
        color: #64748b;
        font-size: 11px;
        margin-top: -4px;
        margin-bottom: 15px;
    }
    .home-container {
        margin-top: 11vh;
        text-align: center;
    }
    .home-icon {
        font-size: 44px;
        margin-bottom: 8px;
    }
    .home-title {
        font-size: 40px;
        font-weight: 700;
        letter-spacing: -1.5px;
        color: #f8fafc;
        margin-bottom: 8px;
    }
    .home-title span {
        color: #8b5cf6;
    }
    .home-subtitle {
        color: #94a3b8;
        font-size: 15px;
        margin-bottom: 35px;
    }
    .suggestion-title {
        color: #64748b;
        font-size: 12px;
        text-align: center;
        margin-top: 25px;
        margin-bottom: 10px;
    }
    [data-testid="stChatMessage"] {
        background: transparent;
        border: none;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    [data-testid="stChatInput"] {
        background: #171a21 !important;
        border: 1px solid #303644 !important;
        border-radius: 15px !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #f8fafc !important;
    }
    .mini-card {
        background: #12151b;
        border: 1px solid #252b36;
        border-radius: 12px;
        padding: 15px;
        height: 100%;
    }
    .mini-card-title {
        color: #e2e8f0;
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 5px;
    }
    .mini-card-text {
        color: #64748b;
        font-size: 12px;
    }
    .status-online {
        color: #4ade80;
        font-size: 11px;
    }
    .footer {
        text-align: center;
        color: #475569;
        font-size: 10px;
        margin-top: 30px;
    }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# BANCO DE DADOS
# ============================================================

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL DEFAULT 'Nova conversa',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                input_tokens INTEGER DEFAULT 0,
                output_tokens INTEGER DEFAULT 0,
                total_tokens INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                memory_key TEXT NOT NULL,
                memory_value TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        conn.commit()
    except sqlite3.Error as error:
        logger.exception("Erro inicializando banco: %s", error)
        raise
    finally:
        conn.close()

init_database()

# ============================================================
# CONVERSAS E MENSAGENS
# ============================================================

def create_conversation(title="Nova conversa"):
    now = datetime.datetime.now().isoformat()
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO conversations (title, created_at, updated_at) VALUES (?, ?, ?)", (title, now, now))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def get_conversations():
    conn = get_connection()
    try:
        return conn.execute("SELECT id, title, created_at, updated_at FROM conversations ORDER BY updated_at DESC").fetchall()
    finally:
        conn.close()

def get_conversation(conversation_id):
    conn = get_connection()
    try:
        return conn.execute("SELECT * FROM conversations WHERE id = ?", (conversation_id,)).fetchone()
    finally:
        conn.close()

def delete_conversation(conversation_id):
    conn = get_connection()
    try:
        conn.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
        conn.execute("DELETE FROM memories WHERE conversation_id = ?", (conversation_id,))
        conn.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
        conn.commit()
    finally:
        conn.close()

def delete_all_conversations():
    conn = get_connection()
    try:
        conn.execute("DELETE FROM messages")
        conn.execute("DELETE FROM memories")
        conn.execute("DELETE FROM conversations")
        conn.commit()
    finally:
        conn.close()

def save_message(conversation_id, role, content, input_tokens=0, output_tokens=0):
    now = datetime.datetime.now().isoformat()
    total_tokens = input_tokens + output_tokens
    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO messages (conversation_id, role, content, input_tokens, output_tokens, total_tokens, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (conversation_id, role, content, input_tokens, output_tokens, total_tokens, now))
        conn.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conversation_id))
        conn.commit()
    finally:
        conn.close()

def get_messages(conversation_id):
    conn = get_connection()
    try:
        return conn.execute("""
            SELECT id, role, content, input_tokens, output_tokens, total_tokens, created_at
            FROM messages WHERE conversation_id = ? ORDER BY id ASC
        """, (conversation_id,)).fetchall()
    finally:
        conn.close()

def get_statistics():
    conn = get_connection()
    try:
        conversations = conn.execute("SELECT COUNT(*) AS total FROM conversations").fetchone()["total"]
        messages = conn.execute("SELECT COUNT(*) AS total FROM messages").fetchone()["total"]
        tokens = conn.execute("SELECT COALESCE(SUM(total_tokens), 0) AS total FROM messages").fetchone()["total"]
        return {"conversations": conversations, "messages": messages, "tokens": tokens}
    finally:
        conn.close()

# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
# LARYMB AI — SYSTEM PROMPT
## IDENTIDADE
Você é o LaryMB, um assistente de inteligência artificial moderno, inteligente, confiável e versátil.
Seu objetivo é ajudar o usuário a pensar, criar, aprender, analisar problemas, desenvolver soluções e trabalhar com tecnologia.
"""

# ============================================================
# CLIENTE GROQ & GERAÇÃO
# ============================================================

def get_groq_client():
    if "GROQ_API_KEY" not in st.secrets:
        raise RuntimeError("GROQ_API_KEY não configurada.")
    api_key = st.secrets["GROQ_API_KEY"]
    if not api_key:
        raise RuntimeError("GROQ_API_KEY está vazia.")
    return Groq(api_key=api_key)

def generate_response(conversation_id):
    messages = get_messages(conversation_id)
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    recent_messages = messages[-MAX_HISTORY_MESSAGES:]
    for message in recent_messages:
        if message["role"] in ("user", "assistant"):
            api_messages.append({"role": message["role"], "content": message["content"]})
    
    client = get_groq_client()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=api_messages,
        temperature=0.35,
        max_tokens=MAX_RESPONSE_TOKENS,
    )
    answer = response.choices[0].message.content
    
    input_tokens = 0
    output_tokens = 0
    usage = getattr(response, "usage", None)
    if usage:
        input_tokens = getattr(usage, "prompt_tokens", 0) or 0
        output_tokens = getattr(usage, "completion_tokens", 0) or 0

    return answer, input_tokens, output_tokens

# ============================================================
# ESTADO DA SESSÃO
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

def new_conversation():
    conversation_id = create_conversation()
    st.session_state.conversation_id = conversation_id
    st.session_state.page = "home"
    st.rerun()

def open_conversation(conversation_id):
    st.session_state.conversation_id = conversation_id
    st.session_state.page = "home"
    st.rerun()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown('<div class="larymb-logo">LaryMB<span>✦</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="larymb-version">Intelligent AI · v3.0</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-online">● Online</div>', unsafe_allow_html=True)
    st.write("")

    if st.button("＋  Nova conversa", use_container_width=True):
        new_conversation()

    search = st.text_input("Pesquisar", placeholder="Pesquisar conversas...", label_visibility="collapsed")
    st.caption("CONVERSAS")

    conversations = get_conversations()
    if search:
        search_lower = search.lower()
        conversations = [c for c in conversations if search_lower in c["title"].lower()]

    if conversations:
        for conversation in conversations[:12]:
            title = conversation["title"]
            if len(title) > 28:
                title = title[:28] + "..."
            is_current = conversation["id"] == st.session_state.conversation_id
            prefix = "● " if is_current else "○ "
            if st.button(prefix + title, key=f"conv_{conversation['id']}", use_container_width=True):
                open_conversation(conversation["id"])
    else:
        st.caption("Nenhuma conversa encontrada.")

    st.divider()

    if st.button("🧠  Memória", use_container_width=True):
        st.session_state.page = "memory"
        st.rerun()

    if st.button("⚙️  Configurações", use_container_width=True):
        st.session_state.page = "settings"
        st.rerun()

    st.write("")
    st.caption("LaryMB AI")
    st.caption("Sua inteligência artificial.")

# ============================================================
# ROTEAMENTO DE PÁGINAS (MEMORY / SETTINGS / HOME-CHAT)
# ============================================================

if st.session_state.page == "memory":
    st.title("🧠 Memória")
    st.caption("A memória do LaryMB será usada para personalizar futuras conversas.")
    st.info("A estrutura de memória já está preparada no banco SQLite.")
    if st.button("← Voltar para o LaryMB"):
        st.session_state.page = "home"
        st.rerun()

elif st.session_state.page == "settings":
    st.title("⚙️ Configurações")
    st.subheader("Modelo de IA")
    st.text_input("Modelo atual", value=MODEL_NAME, disabled=True)
    
    st.subheader("Sistema")
    col1, col2 = st.columns(2)
    stats = get_statistics()
    with col1:
        st.metric("Conversas", stats["conversations"])
    with col2:
        st.metric("Mensagens", stats["messages"])
        
    st.divider()
    confirm = st.checkbox("Confirmo que desejo apagar todas as conversas.")
    if st.button("🗑️ Apagar todas as conversas", disabled=not confirm):
        delete_all_conversations()
        st.session_state.conversation_id = None
        st.success("Conversas removidas.")
        st.rerun()
        
    if st.button("← Voltar para o LaryMB"):
        st.session_state.page = "home"
        st.rerun()

else:
    conversation_id = st.session_state.conversation_id

    # HOME SEM CONVERSA
    if conversation_id is None:
        st.markdown("""
            <div class="home-container">
                <div class="home-icon">✦</div>
                <div class="home-title">Como posso <span>ajudar</span>?</div>
                <div class="home-subtitle">Sua inteligência artificial para criar, aprender, analisar e resolver.</div>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="mini-card"><div class="mini-card-title">💡 Criar e escrever</div><div class="mini-card-text">Ideias, textos, planejamento e documentação.</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="mini-card"><div class="mini-card-title">💻 Programar</div><div class="mini-card-text">Python, SQL, APIs, Streamlit e arquitetura.</div></div>', unsafe_allow_html=True)

        st.write("")
        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="mini-card"><div class="mini-card-title">🧠 Explorar IA</div><div class="mini-card-text">LLMs, RAG, agentes e automação.</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="mini-card"><div class="mini-card-title">📊 Analisar</div><div class="mini-card-text">Dados, projetos, problemas e estratégias.</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="suggestion-title">Comece uma conversa para continuar</div>', unsafe_allow_html=True)
        if st.button("＋ Começar uma nova conversa", type="primary", use_container_width=True):
            new_conversation()
            
        st.markdown('<div class="footer">LaryMB pode cometer erros. Verifique informações importantes.</div>', unsafe_allow_html=True)

    # CHAT ATIVO
    else:
        conversation = get_conversation(conversation_id)
        if conversation is None:
            st.session_state.conversation_id = None
            st.rerun()

        st.subheader(conversation["title"])
        
        # Histórico de mensagens
        messages = get_messages(conversation_id)
        for msg in messages:
            avatar_icon = "👩‍💻" if msg["role"] == "assistant" else "👤"
            with st.chat_message(msg["role"], avatar=avatar_icon):
                st.markdown(msg["content"])

        # Input de nova mensagem do chat
        if prompt := st.chat_input("Digite sua mensagem para o LaryMB..."):
            # Salva a mensagem do usuário
            save_message(conversation_id, "user", prompt)
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)

            # Gera a resposta via Groq de forma segura
            with st.chat_message("assistant", avatar="👩‍💻"):
                with st.spinner("LaryMB pensando..."):
                    try:
                        answer, in_tok, out_tok = generate_response(conversation_id)
                        st.markdown(answer)
                        save_message(conversation_id, "assistant", answer, in_tok, out_tok)
                        
                        # Atualiza o título da conversa com a primeira pergunta se ainda estiver padrão
                        if conversation["title"] == "Nova conversa":
                            new_title = prompt[:30] + "..." if len(prompt) > 30 else prompt
                            conn = get_connection()
                            conn.execute("UPDATE conversations SET title = ? WHERE id = ?", (new_title, conversation_id))
                            conn.commit()
                            conn.close()
                            
                    except Exception as e:
                        error_msg = f"Desculpe, ocorreu um erro ao processar sua solicitação: `{e}`"
                        st.error(error_msg)
