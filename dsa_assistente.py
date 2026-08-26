import datetime
import logging
import sqlite3
from pathlib import Path

import streamlit as st
from groq import Groq

# ============================================================
# LARYMB AI — CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="LaryMB AI",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ============================================================
# CONFIGURAÇÕES E CONSTANTES
# ============================================================

APP_NAME = "LaryMB"
APP_VERSION = "3.1.0"
MODEL_NAME = "llama-3.3-70b-versatile"
DB_PATH = Path("larymb.db")

MAX_HISTORY_MESSAGES = 30
MAX_RESPONSE_TOKENS = 4096

# ============================================================
# LOG
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("larymb")

# ============================================================
# ESTILO VISUAL (DESIGN MINIMALISTA E LIMPO)
# ============================================================

st.markdown(
    """
    <style>
    /* Tema geral escuro e sofisticado */
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }
    
    /* Centralização e largura do container principal */
    .main .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }

    /* Sidebar limpa */
    [data-testid="stSidebar"] {
        background-color: #18181b;
        border-right: 1px solid #27272a;
    }
    [data-testid="stSidebar"] .stButton > button {
        background: transparent;
        border: none;
        color: #a1a1aa;
        text-align: left;
        border-radius: 6px;
        font-size: 13px;
        padding: 6px 10px;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #27272a;
        color: #ffffff;
    }

    /* Logo da Sidebar */
    .larymb-logo {
        font-size: 18px;
        font-weight: 600;
        color: #f4f4f5;
        letter-spacing: -0.5px;
        padding-bottom: 2px;
    }
    .larymb-logo span {
        color: #a78bfa;
    }
    .larymb-version {
        color: #71717a;
        font-size: 11px;
        margin-bottom: 20px;
    }

    /* Tela inicial limpa (sem cards cheios de ícones) */
    .welcome-container {
        text-align: center;
        margin-top: 18vh;
        margin-bottom: 4vh;
    }
    .welcome-title {
        font-size: 32px;
        font-weight: 600;
        color: #f4f4f5;
        letter-spacing: -0.8px;
        margin-bottom: 8px;
    }
    .welcome-subtitle {
        color: #a1a1aa;
        font-size: 14px;
    }

    /* Caixa de input do chat */
    [data-testid="stChatInput"] {
        background-color: #18181b !important;
        border: 1px solid #27272a !important;
        border-radius: 12px !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #f4f4f5 !important;
    }

    /* Ocultar elementos padrão desnecessários do Streamlit */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# BANCO DE DADOS (SQLITE)
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
        conn.commit()
    except sqlite3.Error as error:
        logger.exception("Erro inicializando banco: %s", error)
        raise
    finally:
        conn.close()

init_database()

# ============================================================
# GERENCIAMENTO DE CONVERSAS E MENSAGENS
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
# SYSTEM PROMPT (DIRETRIZES DA LARYMB)
# ============================================================

SYSTEM_PROMPT = """
Você é a LaryMB, uma assistente de Inteligência Artificial moderna, profissional, confiável e orientada à resolução de problemas.
Sua missão é ajudar o usuário a transformar perguntas, problemas e ideias em respostas claras, úteis e acionáveis.
Sempre priorize contexto, precisão, clareza e utilidade. Nunca invente informações ou dados técnicos.
"""

# ============================================================
# CLIENTE GROQ
# ============================================================

def get_groq_client():
    if "GROQ_API_KEY" not in st.secrets:
        raise RuntimeError("GROQ_API_KEY não configurada nos segredos do Streamlit.")
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
# SIDEBAR LATERAL (MINIMALISTA)
# ============================================================

with st.sidebar:
    st.markdown('<div class="larymb-logo">LaryMB <span>✦</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="larymb-version">v3.1</div>', unsafe_allow_html=True)
    
    if st.button("Nova conversa", use_container_width=True):
        new_conversation()

    st.write("")
    st.caption("Histórico")

    conversations = get_conversations()
    if conversations:
        for conversation in conversations[:12]:
            title = conversation["title"]
            if len(title) > 26:
                title = title[:26] + "..."
            is_current = conversation["id"] == st.session_state.conversation_id
            label = "· " + title if is_current else title
            if st.button(label, key=f"conv_{conversation['id']}", use_container_width=True):
                open_conversation(conversation["id"])
    else:
        st.caption("Nenhuma conversa ainda.")

    st.divider()

    if st.button("Configurações", use_container_width=True):
        st.session_state.page = "settings"
        st.rerun()

# ============================================================
# ROTEAMENTO DE TELA
# ============================================================

if st.session_state.page == "settings":
    st.title("Configurações")
    st.caption("Gerenciamento do sistema e estatísticas de uso.")
    
    st.write("")
    st.subheader("Uso Geral")
    stats = get_statistics()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Conversas", stats["conversations"])
    with col2:
        st.metric("Mensagens", stats["messages"])
    with col3:
        st.metric("Tokens Totais", stats["tokens"])
        
    st.divider()
    
    if st.button("Limpar todo o histórico"):
        delete_all_conversations()
        st.session_state.conversation_id = None
        st.success("Histórico apagado com sucesso.")
        st.rerun()
        
    st.write("")
    if st.button("Voltar ao chat"):
        st.session_state.page = "home"
        st.rerun()

else:
    conversation_id = st.session_state.conversation_id

    # TELA INICIAL LIMPA (SEM CARDS OU ÍCONES POLUINDO)
    if conversation_id is None:
        st.markdown("""
            <div class="welcome-container">
                <div class="welcome-title">Como posso ajudar hoje?</div>
                <div class="welcome-subtitle">Digite sua mensagem abaixo para iniciar a conversa com a LaryMB.</div>
            </div>
        """, unsafe_allow_html=True)

        if prompt := st.chat_input("Escreva uma mensagem..."):
            new_id = create_conversation(title=prompt[:30])
            st.session_state.conversation_id = new_id
            save_message(new_id, "user", prompt)
            
            with st.spinner("Pensando..."):
                answer, in_tok, out_tok = generate_response(new_id)
                save_message(new_id, "assistant", answer, in_tok, out_tok)
            st.rerun()

    # CHAT ATIVO
    else:
        conversation = get_conversation(conversation_id)
        if conversation is None:
            st.session_state.conversation_id = None
            st.rerun()

        # Renderiza histórico de mensagens de forma limpa
        messages = get_messages(conversation_id)
        for msg in messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Input de nova mensagem
        if prompt := st.chat_input("Digite sua mensagem..."):
            save_message(conversation_id, "user", prompt)
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Pensando..."):
                    try:
                        answer, in_tok, out_tok = generate_response(conversation_id)
                        st.markdown(answer)
                        save_message(conversation_id, "assistant", answer, in_tok, out_tok)
                        
                        # Atualiza título se for a primeira mensagem real
                        if conversation["title"] == "Nova conversa":
                            new_title = prompt[:28] + "..." if len(prompt) > 28 else prompt
                            conn = get_connection()
                            conn.execute("UPDATE conversations SET title = ? WHERE id = ?", (new_title, conversation_id))
                            conn.commit()
                            conn.close()
                            
                    except Exception as e:
                        st.error(f"Erro ao processar a resposta: `{e}`")
