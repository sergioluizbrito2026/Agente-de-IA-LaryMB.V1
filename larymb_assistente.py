import streamlit as st
from groq import Groq
import textwrap

import streamlit as st
from groq import Groq

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="LaryMB V1",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CONFIGURAÇÕES GLOBAIS DE ESTILO
# ============================================================
st.markdown(
    """
    <style>
        /* Oculta o cabeçalho nativo do Streamlit */
        header {visibility: hidden;}

        /* Fundo geral: Azul escuro profundo e brilhante */
        .stApp {
            background: radial-gradient(circle at 50% 25%, #132247 0%, #070d1b 60%, #03070f 100%) !important;
            background-attachment: fixed !important;
        }

        /* Estilização da Barra Lateral (Sidebar) com largura fixa ideal */
        [data-testid="stSidebar"] {
            background-color: #070d1b !important;
            border-right: 1px solid rgba(212, 175, 55, 0.2);
            min-width: 280px !important;
            max-width: 320px !important;
        }

        /* Ajusta o espaço no topo da página e garante margem inferior para o chat não colar */
        .main .block-container {
            padding-top: 25px !important;
            padding-bottom: 100px !important;
            max-width: 950px !important;
        }

        /* Estilização dos avatares das mensagens */
        div.stChatMessage[data-testid="stChatMessage-user"] div[data-testid="stAvatar"] {
            background-color: #d4af37 !important;
            color: #070d1b !important;
        }

        div.stChatMessage[data-testid="stChatMessage-assistant"] {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        /* Estilização e espaçamento da barra de input do chat */
        .stChatInput {
            max-width: 900px !important;
            margin: 0 auto !important;
            bottom: 20px !important;
        }
        
        .stChatInput textarea {
            background-color: rgba(19, 34, 71, 0.5) !important;
            border: 1px solid rgba(212, 175, 55, 0.35) !important;
            border-radius: 12px !important;
            color: #ffffff !important;
            font-size: 0.95rem !important;
        }

        .stChatInput textarea:focus {
            border-color: rgba(212, 175, 55, 0.9) !important;
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.25) !important;
        }

        /* Estilo dos Cards de Sugestão */
        .suggestion-card {
            background: rgba(19, 34, 71, 0.4);
            border: 1px solid rgba(212, 175, 55, 0.25);
            border-radius: 10px;
            padding: 9px 4px;
            text-align: center;
            color: #e5e7eb;
            font-size: 0.79rem;
            font-weight: 500;
            transition: all 0.3s ease;
            white-space: nowrap;
        }
        .suggestion-card:hover {
            border-color: rgba(212, 175, 55, 0.8);
            background: rgba(212, 175, 55, 0.15);
            color: #ffffff;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# CONFIGURAÇÃO DA API DA GROQ E PROMPT MESTRE
# ============================================================
client = Groq(api_key=st.secrets.get("GROQ_API_KEY", ""))

SYSTEM_PROMPT = """
Você é LaryMB V1, uma Inteligência Artificial generalista desenvolvida pela LaryMB AI.
Sua missão é ajudar o usuário a responder perguntas gerais, explicar conceitos, resolver problemas, ensinar conteúdos, auxiliar nos estudos, criar e revisar textos, traduzir idiomas, analisar documentos, trabalhar com programação, auxiliar em tecnologia, analisar dados, desenvolver ideias, organizar informações, automatizar tarefas, planejar projetos, apoiar decisões e aumentar produtividade.
Seu objetivo é transformar perguntas, informações e problemas em respostas claras, úteis e práticas.
Princípios: Nunca invente informações, priorize precisão, clareza e utilize o contexto disponível.
"""

# Inicializa o histórico de mensagens da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================================
# BARRA LATERAL (SIDEBAR)
# ============================================================
with st.sidebar:
    st.image("agente de ia lm.png", width=120)
    st.markdown("### LaryMB AI")
    st.markdown("<p style='color: #94a3b8; font-size: 0.85rem; margin-top: -10px;'>Inteligência Artificial • V1</p>", unsafe_allow_html=True)
    st.markdown("Uma IA para responder perguntas, aprender, criar, analisar informações e ajudar você a resolver problemas.")
    st.markdown("---")
    st.markdown(
        """
        <div style="background-color: rgba(212, 175, 55, 0.08); border-left: 3px solid #d4af37; padding: 10px; border-radius: 4px; font-size: 0.8rem; color: #cbd5e1;">
            ⚠️ A LaryMB pode cometer erros. Verifique informações importantes antes de tomar decisões.
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")
    with st.expander("🛠️ Suporte / Fale conosco"):
        st.markdown("Encontrou um problema ou precisa de ajuda?")
        st.markdown("**E-mail:** sergiolmendes2026@gmail.com")
        st.markdown(
            """
            <a href="https://wa.me/" target="_blank" style="text-decoration: none;">
                <div style="background-color: #d4af37; color: #070d1b; text-align: center; padding: 8px; border-radius: 8px; font-weight: bold; font-size: 0.9rem; margin-top: 10px;">
                    Falar no WhatsApp
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Limpar conversa", use_container_width=True, key="btn_limpar_conversa_main"):
        st.session_state.messages = []
        st.rerun()

# ============================================================
# TELA PRINCIPAL
# ============================================================

# 1. Logotipo centralizado
col_l1, col_l2, col_l3 = st.columns([1.4, 0.9, 1.4])
with col_l2:
    st.image("agente de ia lm.png", use_container_width=True)

# 2. Subtítulo
st.markdown(
    """
    <div style="text-align: center; margin-top: 2px; margin-bottom: 18px; color: #94a3b8; font-size: 0.9rem;">
        Sua inteligência artificial para aprender, criar, analisar e resolver.
    </div>
    """,
    unsafe_allow_html=True
)

# 3. Cards de Sugestão
c1, s1, c2, s2, c3, s3, c4 = st.columns([3.8, 0.2, 3.8, 0.2, 3.8, 0.2, 3.8])

with c1:
    st.markdown('<div class="suggestion-card">💡 Explorar ideia</div>', unsafe_allow_html=True)
with s1:
    st.markdown('<div style="text-align: center; color: rgba(212,175,55,0.4); margin-top: 8px; font-size: 0.8rem;">|</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="suggestion-card">📚 Estudar assunto</div>', unsafe_allow_html=True)
with s2:
    st.markdown('<div style="text-align: center; color: rgba(212,175,55,0.4); margin-top: 8px; font-size: 0.8rem;">|</div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="suggestion-card">💻 Programar</div>', unsafe_allow_html=True)
with s3:
    st.markdown('<div style="text-align: center; color: rgba(212,175,55,0.4); margin-top: 8px; font-size: 0.8rem;">|</div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="suggestion-card">📊 Analisar dados</div>', unsafe_allow_html=True)

# 4. Saudação de boas-vindas
if not st.session_state.messages:
    st.markdown(
        """
        <div style="text-align: center; margin-top: 22px; margin-bottom: 15px;">
            <h3 style="color: #ffffff; margin-bottom: 2px; font-weight: 700;">Olá 👋</h3>
            <p style="color: #94a3b8; font-size: 0.9rem;">Como posso ajudar você hoje?</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# HISTÓRICO E ENTRADA DO CHAT
# ============================================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua mensagem para a LaryMB..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}] + [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ]
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages_payload,
                temperature=0.7,
                stream=True,
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"Desculpe, ocorreu um erro ao processar sua solicitação: {e}"
            message_placeholder.markdown(full_response)
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
