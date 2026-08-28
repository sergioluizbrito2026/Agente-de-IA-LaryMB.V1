import streamlit as st
from groq import Groq
import textwrap

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
# CONFIGURAÇÕES GLOBAIS DE ESTILO E MARCA D'ÁGUA
# ============================================================
st.markdown(
    """
    <style>
        /* Oculta o cabeçalho nativo do Streamlit */
        header {visibility: hidden;}

        /* Fundo geral: Azul escuro profundo e brilhante com Marca d'água elegante */
        .stApp {
            background: radial-gradient(circle at 50% 25%, #132247 0%, #070d1b 60%, #03070f 100%) !important;
            background-attachment: fixed !important;
        }

        /* Marca d'água sutil ao fundo da tela principal */
        .stApp::before {
            content: "LARY MB";
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 14vw;
            font-weight: 900;
            color: rgba(212, 175, 55, 0.025);
            z-index: 0;
            pointer-events: none;
            white-space: nowrap;
            letter-spacing: 15px;
        }

        /* Estilização da Barra Lateral (Sidebar) */
        [data-testid="stSidebar"] {
            background-color: #070d1b !important;
            border-right: 1px solid rgba(212, 175, 55, 0.2);
            z-index: 10;
        }

        /* Ajusta o espaçamento do conteúdo principal */
        .main .block-container {
            padding-top: 15px !important;
            padding-bottom: 90px !important;
            max-width: 900px !important;
            position: relative;
            z-index: 1;
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

        /* Caixa de Digitação Compacta e Fina */
        [data-testid="stChatInput"] {
            max-width: 720px !important;
            margin: 0 auto !important;
            background: rgba(19, 34, 71, 0.6) !important;
            backdrop-filter: blur(10px);
            border-radius: 10px !important;
            border: 1px solid rgba(212, 175, 55, 0.35) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
            padding: 0px !important;
        }
        
        .stChatInput textarea {
            background-color: transparent !important;
            border: none !important;
            color: #ffffff !important;
            font-size: 0.9rem !important;
            padding-top: 8px !important;
            padding-bottom: 8px !important;
            height: 40px !important;
            max-height: 40px !important;
        }

        .stChatInput textarea:focus {
            box-shadow: none !important;
            border: none !important;
        }

        /* Estilo refinado dos Cards de Sugestão */
        .suggestion-card {
            background: rgba(19, 34, 71, 0.5);
            border: 1px solid rgba(212, 175, 55, 0.25);
            border-radius: 10px;
            padding: 8px 12px;
            text-align: center;
            color: #e5e7eb;
            font-size: 0.79rem;
            font-weight: 500;
            transition: all 0.3s ease;
            white-space: nowrap;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
        .suggestion-card:hover {
            border-color: rgba(212, 175, 55, 0.8);
            background: rgba(212, 175, 55, 0.15);
            color: #ffffff;
            transform: translateY(-2px);
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

# 1. Logotipo centralizado com tamanho ideal
col_l1, col_l2, col_l3 = st.columns([1.9, 1.2, 1.9])
with col_l2:
    st.image("agente de ia lm.png", use_container_width=True)

# 2. Subtítulo
st.markdown(
    """
    <div style="text-align: center; margin-top: 2px; margin-bottom: 22px; color: #94a3b8; font-size: 0.85rem;">
        Sua inteligência artificial para aprender, criar, analisar e resolver.
    </div>
    """,
    unsafe_allow_html=True
)

# 3. Bloco Inicial (Exibido apenas quando o chat estiver vazio)
if not st.session_state.messages:
    
    # 4. Cards de Sugestão em cima
    c1, s1, c2, s2, c3, s3, c4 = st.columns([3.8, 0.2, 3.8, 0.2, 3.8, 0.2, 3.8])

    with c1:
        st.markdown('<div class="suggestion-card">💡 Explorar uma ideia</div>', unsafe_allow_html=True)
    with s1:
        st.markdown('<div style="text-align: center; color: rgba(212,175,55,0.4); margin-top: 8px; font-size: 0.8rem;">|</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="suggestion-card">📚 Estudar um assunto</div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div style="text-align: center; color: rgba(212,175,55,0.4); margin-top: 8px; font-size: 0.8rem;">|</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="suggestion-card">💻 Programar</div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div style="text-align: center; color: rgba(212,175,55,0.4); margin-top: 8px; font-size: 0.8rem;">|</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="suggestion-card">📊 Analisar informações</div>', unsafe_allow_html=True)

    # 5. Saudação e "Como posso ajudar você hoje?" embaixo dos cards
    st.markdown(
        """
        <div style="text-align: center; margin-top: 18px; margin-bottom: 15px;">
            <h3 style="color: #ffffff; margin-bottom: 2px; font-weight: 700;">Olá 👋</h3>
            <p style="color: #94a3b8; font-size: 0.9rem;">Como posso ajudar você hoje?</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

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
