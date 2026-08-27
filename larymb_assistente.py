import streamlit as st
from groq import Groq
import textwrap

# Configuração da página
st.set_page_config(
    page_title="LaryMB V1",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ESTILOS CSS - Fundo e Sidebar harmonizados com o tom elegante da referência
st.markdown(
    textwrap.dedent("""
    <style>
    /* Fundo degradê principal */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #172033 0%, #0c111d 45%, #05070a 100%);
        color: #F8FAFC;
    }
    
    .block-container {
        max-width: 900px;
        padding-top: 2.5rem;
        padding-bottom: 6rem;
        margin: 0 auto;
    }
    
    /* Barra Lateral (Sidebar) com o mesmo tom elegante e translúcido */
    [data-testid="stSidebar"] {
        background: rgba(12, 17, 29, 0.88) !important;
        border-right: 1px solid rgba(56, 189, 248, 0.1);
        backdrop-filter: blur(12px);
    }
    
    /* Ajustes visuais internos da Sidebar para combinar perfeitamente */
    [data-testid="stSidebar"] .stAlert {
        background: rgba(17, 26, 43, 0.7) !important;
        border: 1px solid rgba(56, 189, 248, 0.15) !important;
        color: #99d6ff !important;
    }

    /* Cabeçalho Customizado */
    .custom-header {
        position: relative;
        padding: 10px 0px 20px 0px;
        margin-bottom: 25px;
        background: transparent;
        border: none;
        box-shadow: none;
    }
    .brand-label {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
        color: #38bdf8;
        font-size: .76rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    .brand-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #38bdf8;
        box-shadow: 0 0 12px rgba(56,189,248,.85);
    }
    .custom-title {
        margin: 0;
        color: #FFFFFF;
        font-size: 2.55rem;
        line-height: 1.15;
        font-weight: 800;
        text-shadow: 0 2px 12px rgba(0,180,255,.25);
    }
    .custom-subtitle {
        margin-top: 8px;
        margin-bottom: 8px;
        color: #99d6ff;
        font-size: 1.08rem;
        font-weight: 600;
    }
    .custom-caption {
        max-width: 690px;
        color: #8fb3d9;
        font-size: .9rem;
        line-height: 1.6;
    }

    /* Mensagens de Chat */
    [data-testid="stChatMessage"] {
        background: rgba(12, 18, 30, 0.6) !important;
        border: 1px solid rgba(56, 189, 248, 0.12) !important;
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(8px);
    }

    /* Barra de Chat Flutuante */
    [data-testid="stChatInput"] {
        background: rgba(10, 15, 25, 0.9) !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(10px);
    }

    .watermark-center {
        text-align: center;
        color: #64748B;
        font-size: 0.82rem;
        margin-top: 3rem;
    }
    .footer-brand {
        color: #38bdf8;
        font-weight: 600;
    }
    </style>
    """),
    unsafe_allow_html=True,
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

Você foi projetada para atuar como uma assistente inteligente, profissional, didática, segura e versátil, capaz de compreender diferentes tipos de solicitações e adaptar sua resposta de acordo com a intenção do usuário.
Você deve oferecer uma experiência moderna de IA, semelhante à experiência de assistentes generativos avançados, mantendo identidade própria, linguagem natural e foco em utilidade.

MISSÃO
Sua missão é ajudar o usuário a:
- Responder perguntas gerais;
- Explicar conceitos;
- Resolver problemas;
- Ensinar conteúdos;
- Auxiliar nos estudos;
- Criar e revisar textos;
- Traduzir idiomas;
- Analisar documentos;
- Trabalhar com programação;
- Auxiliar em tecnologia;
- Analisar dados;
- Desenvolver ideias;
- Organizar informações;
- Automatizar tarefas;
- Planejar projetos;
- Apoiar decisões;
- Aumentar produtividade.

Seu objetivo é transformar perguntas, informações e problemas em respostas claras, úteis e práticas.

PRINCÍPIOS FUNDAMENTAIS
1. NÃO INVENTAR: Nunca invente informações. Quando não souber algo, diga claramente.
2. PRECISÃO: Priorize respostas corretas e confiáveis.
3. CLAREZA: Responda de maneira clara e objetiva. Divida explicações em etapas quando complexo.
4. CONTEXTO: Utilize o contexto disponível na conversa e não peça informações já fornecidas.

LaryMB V1 — Inteligência que transforma perguntas em soluções.
"""

# ============================================================
# BARRA LATERAL (Sidebar)
# ============================================================
with st.sidebar:
    st.markdown("### ⚡ LaryMB AI")
    st.caption("Inteligência Artificial • V1")
    st.write("Uma IA para responder perguntas, aprender, criar, analisar informações e ajudar você a resolver problemas.")
    
    st.markdown("---")
    
    groq_api_key = st.secrets.get("GROQ_API_KEY", "")
    if not groq_api_key:
        groq_api_key = st.text_input(
            "Chave da API Groq",
            type="password",
            help="Recomendado: configure GROQ_API_KEY nos Secrets do Streamlit Cloud.",
        )

    st.markdown("---")
    st.info("⚠️ A LaryMB pode cometer erros. Verifique informações importantes antes de tomar decisões.")

    with st.expander("📌 Suporte / Fale conosco"):
        st.markdown("Encontrou um problema ou precisa de ajuda?")
        st.markdown("**E-mail:** sergiolmendes2026@gmail.com")
        whatsapp_url = "https://wa.me/55994376755?text=Ol%C3%A1%2C%20vim%20pelo%20Agente%20IA%20LaryMB%21"
        st.markdown(
            f'<a href="{whatsapp_url}" target="_blank" style="display:block;text-align:center;text-decoration:none;background:#111B2E;color:#E2E8F0;border:1px solid #26344D;padding:11px;border-radius:10px;font-weight:600;">Falar no WhatsApp</a>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    if st.button("🗑️ Limpar conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ============================================================
# CABEÇALHO PRINCIPAL
# ============================================================
st.markdown(
    textwrap.dedent("""
    <div class="custom-header">
        <div class="brand-label"><div class="brand-dot"></div>LaryMB AI</div>
        <div class="custom-title">LaryMB V1</div>
        <div class="custom-subtitle">Sua inteligência artificial para aprender, criar, analisar e resolver.</div>
        <div class="custom-caption">Faça perguntas, explore ideias, estude, programe, analise informações e obtenha respostas claras e contextualizadas.</div>
    </div>
    """),
    unsafe_allow_html=True,
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
if prompt := st.chat_input("Pergunte qualquer coisa..."):
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

