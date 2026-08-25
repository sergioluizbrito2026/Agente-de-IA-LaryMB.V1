import datetime
import sqlite3
from groq import Groq
import streamlit as st

# --- CONFIGURAÇÃO ---
st.set_page_config(
    page_title="Agente de IA Larymb.v1", layout="wide", page_icon="🤖"
)

# --- CSS GLOBAL ---
st.markdown(
    """
    <style>
    .stApp { 
        background: radial-gradient(circle at center, #001f3f 0%, #050505 100%) !important;
        font-family: 'Sans Serif', Arial, sans-serif !important;
        box-shadow: inset 0px 0px 150px 30px rgba(75, 0, 130, 0.15) !important; 
    }
    [data-testid="stSidebar"] { background-color: #4B0082 !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stChatInput"] {
        box-shadow: 0px 0px 15px 5px rgba(0, 191, 255, 0.4) !important;
        border-radius: 15px !important;
        background-color: #1a1a1a !important;
    }
    .status-verde { color: #00FF00 !important; font-weight: bold; }
    </style>
""",
    unsafe_allow_html=True,
)


# --- BANCO DE DADOS ---
def init_db():
  conn = sqlite3.connect("historico_chat.db")
  c = conn.cursor()
  c.execute(
      """CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY, role TEXT,"
      " content TEXT, timestamp TEXT)"""
  )
  conn.commit()
  conn.close()


def salvar_mensagem(role, content):
  conn = sqlite3.connect("historico_chat.db")
  c = conn.cursor()
  c.execute(
      "INSERT INTO chats (role, content, timestamp) VALUES (?, ?, ?)",
      (role, content, datetime.datetime.now().isoformat()),
  )
  conn.commit()
  conn.close()


init_db()

# --- SIDEBAR ---
with st.sidebar:
  st.markdown(
      """
        <div style="text-align: center; padding-bottom: 20px;">
            <img src="https://api.dicebear.com/7.x/bottts/svg?seed=Larymb" width="100">
            <h3>Agente de IA Larymb.v1</h3>
            <div class="status-verde">● Status: Online</div>
        </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("---")
  if st.button("🏠 Início", use_container_width=True):
    st.session_state.page = "Início"
  if st.button("💬 Conversas", use_container_width=True, key="btn_c"):
    st.session_state.page = "Conversas"
  if st.button("⚙️ Configurações", use_container_width=True):
    st.session_state.page = "Configurações"

  st.markdown("---")
  st.info(
      "Aviso: IA pode gerar respostas imprecisas, incompletas ou erradas."
      " Sempre verifique informações críticas antes de confiar totalmente.",
      icon="ℹ️",
  )

  st.markdown("---")
  # Botão Email
  st.sidebar.markdown(
      """
    <a href="mailto:sergiolmendes2026@gmail.com" style="
        display: flex;
        align-items: center;
        justify-content: left;
        background-color: #262730;
        color: #FAFAFA;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        text-decoration: none;
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: 400;
        font-size: 1rem;
        margin-bottom: 0.5rem;
        border: 1px solid #464e5f;
        transition: border-color 300ms, background-color 300ms;
        width: 100%;
        box-sizing: border-box;
    " onmouseover="this.style.borderColor='#FF4B4B'; this.style.backgroundColor='#2e303a'" onmouseout="this.style.borderColor='#464e5f'; this.style.backgroundColor='#262730'">
        <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" width="20" style="margin-right: 10px;">
        Enviar e-mail para Suporte
    </a>
    """,
      unsafe_allow_html=True,
  )

  # Botão WhatsApp
  NUMERO_TELEFONE = "5511994376755"
  MENSAGEM_PADRAO = "Olá, preciso de ajuda com o Agente de IA."
  URL_WHATSAPP = (
      f"https://wa.me/{NUMERO_TELEFONE}?text={MENSAGEM_PADRAO.replace(' ', '%20')}"
  )

  st.sidebar.markdown(
      f"""
    <a href="{URL_WHATSAPP}" target="_blank" style="
        display: flex;
        align-items: center;
        justify-content: left;
        background-color: #262730;
        color: #FAFAFA;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        text-decoration: none;
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: 400;
        font-size: 1rem;
        margin-bottom: 0.5rem;
        border: 1px solid #464e5f;
        transition: border-color 300ms, background-color 300ms;
        width: 100%;
        box-sizing: border-box;
    " onmouseover="this.style.borderColor='#FF4B4B'; this.style.backgroundColor='#2e303a'" onmouseout="this.style.borderColor='#464e5f'; this.style.backgroundColor='#262730'">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="20" style="margin-right: 10px;">
        WhatsApp Falar com Suporte
    </a>
    """,
      unsafe_allow_html=True,
  )

# --- LÓGICA DO CHATBOT ---
if "page" not in st.session_state:
  st.session_state.page = "Início"

if st.session_state.page == "Início":
  st.markdown(
      """
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: white; margin-bottom: 5px;">
            Como posso <span style="color: #8B5CF6;">te ajudar</span> hoje?
        </h1>
        <p style="color: #A0A0A0; font-size: 1.1em; font-weight: 300;">
            Seu guia inteligente para respostas, explicações e referências.
        </p>
    </div>
""",
      unsafe_allow_html=True,
  )

  # Carregar histórico do banco
  conn = sqlite3.connect("historico_chat.db")
  mensagens_db = (
      conn.cursor().execute("SELECT role, content FROM chats ORDER BY id ASC").fetchall()
  )
  conn.close()

  # Exibir histórico na tela
  for role, content in mensagens_db:
    avatar = "🤖" if role == "assistant" else "👤"
    with st.chat_message(role, avatar=avatar):
      st.markdown(content)

  if prompt := st.chat_input("Qual sua dúvida?"):
    # Verifica se a chave de API está configurada nos segredos do Streamlit
    if "GROQ_API_KEY" not in st.secrets:
      st.error(
          "Chave de API não configurada. Adicione 'GROQ_API_KEY' nas"
          " configurações de Secrets do Streamlit Cloud."
      )
    else:
      salvar_mensagem("user", prompt)
      with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

      # Preparar histórico para a API (Memória)
      historico_api = [{
          "role": "system",
          "content": (
              "Você é o Larymb.v1, um assistente inteligente e prestativo."
          ),
      }]
      for r, c in mensagens_db:
        historico_api.append({"role": r, "content": c})
      historico_api.append({"role": "user", "content": prompt})

      # Pega a chave direto do st.secrets de forma segura
      client = Groq(api_key=st.secrets["GROQ_API_KEY"])
      resposta = client.chat.completions.create(
          messages=historico_api, model="llama-3.3-70b-versatile"
      ).choices[0].message.content

      salvar_mensagem("assistant", resposta)
      st.rerun()

elif st.session_state.page == "Conversas":
  st.subheader("💬 Histórico de Conversas")
  conn = sqlite3.connect("historico_chat.db")
  mensagens_db = (
      conn.cursor()
      .execute(
          "SELECT role, content, timestamp FROM chats ORDER BY id ASC"
      )
      .fetchall()
  )
  conn.close()

  if not mensagens_db:
    st.info("Nenhuma conversa registrada ainda.")
  else:
    for role, content, timestamp in mensagens_db:
      origem = "Assistente" if role == "assistant" else "Usuário"
      st.text(f"[{timestamp}] {origem}: {content}")

elif st.session_state.page == "Configurações":
  st.subheader("⚙️ Configurações do Sistema")
  if st.button("🗑️ Limpar Histórico do Chat"):
    conn = sqlite3.connect("historico_chat.db")
    conn.cursor().execute("DELETE FROM chats")
    conn.commit()
    conn.close()
    st.success("Histórico limpo com sucesso!")
    st.rerun()
