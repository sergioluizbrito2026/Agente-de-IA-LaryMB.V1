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
# CONFIGURAÇÕES GLOBAIS DE ESTILO
# ============================================================
st.markdown(
    """
    <style>
        /* Oculta o cabeçalho nativo do Streamlit */
        header {visibility: hidden;}

        /* Fundo geral: Azul mais escuro, profundo e com brilho central elegante */
        .stApp {
            background: radial-gradient(circle at 50% 25%, #132247 0%, #070d1b 60%, #03070f 100%) !important;
            background-attachment: fixed !important;
        }

        /* Estilização da Barra Lateral (Sidebar) */
        [data-testid="stSidebar"] {
            background-color: #070d1b !important;
            border-right: 1px solid rgba(212, 175, 55, 0.2);
        }

        /* Cria a barra superior fixa para o logotipo principal no topo */
        .top-logo-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background: linear-gradient(90deg, #070d1b 0%, #132247 50%, #070d1b 100%);
            z-index: 99999;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 3px 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.8);
            border-bottom: 1px solid rgba(212, 175, 55, 0.25);
        }

        /* Logotipo do topo reduzido */
        .top-logo-bar img {
            max-height: 34px !important;
            width: auto !important;
        }

        /* Ajusta o espaço no topo da página */
        .main .block-container {
            padding-top: 75px !important;
            max-width: 950px !important;
        }

        /* Estilização limpa para os avatares das mensagens */
        div.stChatMessage[data-testid="stChatMessage-user"] div[data-testid="stAvatar"] {
            background-color: #d4af37 !important;
            color: #070d1b !important;
        }

        /* Remove a caixa/borda ao redor da resposta da IA para ficar fluído */
        div.stChatMessage[data-testid="stChatMessage-assistant"] {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding-left: 0px !important;
            padding-right: 0px !important;
        }

        /* Estilização elegante e espaçada para a barra de input do chat */
        .stChatInput {
            max-width: 900px !important;
            margin: 0 auto !important;
        }
        
        .stChatInput textarea {
            background-color: rgba(19, 34, 71, 0.5) !important;
            border: 1px solid rgba(212, 175, 55, 0.35) !important;
            border-radius: 12px !important;
            color: #ffffff !important;
            font-size: 0.95rem !important;
            padding-top: 12px !important;
            padding-bottom: 12px !important;
            padding-left: 18px !important;
            padding-right: 18px !important;
            transition: all 0.3s ease !important;
        }

        .stChatInput textarea:focus {
            border-color: rgba(212, 175, 55, 0.9) !important;
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.25) !important;
        }

        /* Estilo dos Cards em Linha Única */
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
    
    <div class="top-logo-bar">
        <img src="app/static/agente de ia lm.png" onerror="this.style.display='none'">
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# PROMPT MESTRE — LARYMB V1
# ============================================================
CUSTOM_PROMPT = """
Você é LaryMB V1, uma Inteligência Artificial generalista desenvolvida pela LaryMB AI.

A LaryMB V1 deve responder perguntas gerais sobre assuntos cotidianos, conhecimentos gerais, educação, tecnologia, programação, idiomas, negócios, produtividade, criatividade e outros temas dentro de sua capacidade.

Ela não deve assumir que o usuário está necessariamente estudando ou programando.

Primeiro, identifique a intenção da pergunta e, em seguida, escolha a melhor forma de responder.

A LaryMB V1 deve adaptar automaticamente sua linguagem, profundidade, estrutura e abordagem ao contexto e ao objetivo do usuário.

Você foi projetada para atuar como uma assistente inteligente, profissional, didática, segura e versátil...

MISSÃO
Sua missão é ajudar o usuário a responder perguntas gerais, explicar conceitos, resolver problemas, ensinar conteúdos, auxiliar nos estudos, criar e revisar textos, traduzir idiomas, analisar documentos, trabalhar com programação, auxiliar em tecnologia, analisar dados, desenvolver ideias, organizar informações, automatizar tarefas, planejar projetos, apoiar decisões e aumentar produtividade.

Seu objetivo é transformar perguntas, informações e problemas em respostas claras, úteis e práticas.

IA GENERALISTA
A LaryMB V1 deve ser capaz de responder perguntas sobre diferentes áreas. O usuário não precisa escolher previamente uma categoria. A LaryMB deve identificar automaticamente a intenção da solicitação e adaptar sua resposta.

PRINCÍPIOS FUNDAMENTAIS
1. NÃO INVENTAR: Nunca invente informações. Quando não souber algo, diga claramente que não possui informação suficiente.
2. PRECISÃO: Priorize respostas corretas e confiáveis.
3. CLAREZA: Responda de maneira clara e objetiva.
4. CONTEXTO: Utilize o contexto disponível na conversa.

PERSONALIDADE
A LaryMB V1 deve ser inteligente, profissional, educada, didática, objetiva, natural, estratégica, colaborativa, respeitosa e segura.

IDENTIDADE FINAL
Você é LaryMB V1, uma Inteligência Artificial generalista criada pela LaryMB AI.
LaryMB V1 — Inteligência que transforma perguntas em soluções.
"""

# ============================================================
# CONTEÚDO DA BARRA LATERAL (SIDEBAR)
# ============================================================
with st.sidebar:
    st.image("agente de ia lm.png", width=120)
    
    st.markdown("### LaryMB AI")
    st.markdown("<p style='color: #94a3b8; font-size: 0.85rem; margin-top: -10px;'>Inteligência Artificial • V1</p>", unsafe_allow_html=True)
    
    st.markdown(
        """
        Uma IA para responder perguntas, aprender, criar, analisar informações e ajudar você a resolver problemas.
        """,
        unsafe_allow_html=True
    )
    
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
    
    if st.button("🗑️ Limpar conversa", use_container_width=True, key="btn_limpar_conversa"):
        st.rerun()

# ============================================================
# TELA PRINCIPAL
# ============================================================

# 1. Logotipo centralizado no topo
col_l1, col_l2, col_l3 = st.columns([1.4, 0.9, 1.4])
with col_l2:
    st.image("agente de ia lm.png", use_container_width=True)

# 2. Frase descritiva centralizada
st.markdown(
    """
    <div style="text-align: center; margin-top: 2px; margin-bottom: 18px; color: #94a3b8; font-size: 0.9rem;">
        Sua inteligência artificial para aprender, criar, analisar e resolver.
    </div>
    """,
    unsafe_allow_html=True
)

# 3. Os 4 Cards Lado a Lado
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
# CONFIGURAÇÕES GLOBAIS DE ESTILO
# ============================================================
st.markdown(
    """
    <style>
        /* Oculta o cabeçalho nativo do Streamlit */
        header {visibility: hidden;}

        /* Fundo geral: Azul mais escuro, profundo e com brilho central elegante */
        .stApp {
            background: radial-gradient(circle at 50% 25%, #132247 0%, #070d1b 60%, #03070f 100%) !important;
            background-attachment: fixed !important;
        }

        /* Estilização da Barra Lateral (Sidebar) */
        [data-testid="stSidebar"] {
            background-color: #070d1b !important;
            border-right: 1px solid rgba(212, 175, 55, 0.2);
        }

        /* Cria a barra superior fixa para o logotipo principal no topo */
        .top-logo-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background: linear-gradient(90deg, #070d1b 0%, #132247 50%, #070d1b 100%);
            z-index: 99999;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 3px 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.8);
            border-bottom: 1px solid rgba(212, 175, 55, 0.25);
        }

        /* Logotipo do topo reduzido */
        .top-logo-bar img {
            max-height: 34px !important;
            width: auto !important;
        }

        /* Ajusta o espaço no topo da página */
        .main .block-container {
            padding-top: 75px !important;
            max-width: 950px !important;
        }

        /* Estilização limpa para os avatares das mensagens */
        div.stChatMessage[data-testid="stChatMessage-user"] div[data-testid="stAvatar"] {
            background-color: #d4af37 !important;
            color: #070d1b !important;
        }

        /* Remove a caixa/borda ao redor da resposta da IA para ficar fluído */
        div.stChatMessage[data-testid="stChatMessage-assistant"] {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding-left: 0px !important;
            padding-right: 0px !important;
        }

        /* Estilização elegante e espaçada para a barra de input do chat */
        .stChatInput {
            max-width: 900px !important;
            margin: 0 auto !important;
        }
        
        .stChatInput textarea {
            background-color: rgba(19, 34, 71, 0.5) !important;
            border: 1px solid rgba(212, 175, 55, 0.35) !important;
            border-radius: 12px !important;
            color: #ffffff !important;
            font-size: 0.95rem !important;
            padding-top: 12px !important;
            padding-bottom: 12px !important;
            padding-left: 18px !important;
            padding-right: 18px !important;
            transition: all 0.3s ease !important;
        }

        .stChatInput textarea:focus {
            border-color: rgba(212, 175, 55, 0.9) !important;
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.25) !important;
        }

        /* Estilo dos Cards em Linha Única */
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
    
    <div class="top-logo-bar">
        <img src="app/static/agente de ia lm.png" onerror="this.style.display='none'">
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# CONTEÚDO DA BARRA LATERAL (SIDEBAR)
# ============================================================
with st.sidebar:
    st.image("agente de ia lm.png", width=120)
    
    st.markdown("### LaryMB AI")
    st.markdown("<p style='color: #94a3b8; font-size: 0.85rem; margin-top: -10px;'>Inteligência Artificial • V1</p>", unsafe_allow_html=True)
    
    st.markdown(
        """
        Uma IA para responder perguntas, aprender, criar, analisar informações e ajudar você a resolver problemas.
        """,
        unsafe_allow_html=True
    )
    
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
    
    if st.button("🗑️ Limpar conversa", use_container_width=True):
        st.rerun()

# ============================================================
# TELA PRINCIPAL (EXECUTADA APENAS UMA VEZ)
# ============================================================

# 1. Logotipo centralizado no topo
col_l1, col_l2, col_l3 = st.columns([1.4, 0.9, 1.4])
with col_l2:
    st.image("agente de ia lm.png", use_container_width=True)

# 2. Frase descritiva centralizada
st.markdown(
    """
    <div style="text-align: center; margin-top: 2px; margin-bottom: 18px; color: #94a3b8; font-size: 0.9rem;">
        Sua inteligência artificial para aprender, criar, analisar e resolver.
    </div>
    """,
    unsafe_allow_html=True
)

# 3. Os 4 Cards Lado a Lado
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
# HISTÓRICO DE MENSAGENS
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================================
# CLIENTE GROQ
# ============================================================
client = None
if groq_api_key:
    try:
        client = Groq(api_key=groq_api_key)
    except Exception as e:
        st.sidebar.error(f"Erro ao inicializar a Groq: {e}")

# ============================================================
# CHAT E ENTRADA
# ============================================================
if prompt := st.chat_input ("  Digite uma mensagem para a Larymb..."):
    if not client:
        st.warning("Configure a GROQ_API_KEY nos Secrets do Streamlit Cloud ou informe a chave na barra lateral.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    messages_for_api.extend(st.session_state.messages)

    with st.chat_message("assistant"):
        with st.spinner("LaryMB está pensando..."):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=messages_for_api,
                    temperature=0.7,
                    max_tokens=2048,
                )
                answer = response.choices[0].message.content or "Não consegui gerar uma resposta desta vez."
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error("Não foi possível obter uma resposta da IA.")
                st.caption(f"Detalhes técnicos: {e}")

