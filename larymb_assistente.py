import streamlit as st
from groq import Groq
import textwrap

st.set_page_config(
    page_title="LaryMB AI — V1",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="expanded",
)

# DESIGN — LARYMB AI
# ============================================================
st.markdown(
    textwrap.dedent("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0b132b 0%, #081121 50%, #040810 100%);
        color:#F8FAFC;
    }
    .block-container{max-width:900px;padding-top:2rem;padding-bottom:5rem;}
    [data-testid="stSidebar"]{background:#060a14;border-right:1px solid rgba(255,255,255,.07);}
    [data-testid="stSidebar"] p{color:#94A3B8;font-size:.88rem;line-height:1.55;}
    
    .custom-header{
        position:relative;
        overflow:hidden;
        padding:10px 0px 25px 0px;
        margin-bottom:20px;
        background:transparent;
        border:none;
        box-shadow:none;
    }
    .custom-header::before{
        content:"LARYMB";
        position:absolute;
        left:0px;
        top:-15px;
        font-size:110px;
        line-height:1;
        font-weight:900;
        letter-spacing:6px;
        color:rgba(255,255,255,.025);
        pointer-events:none;
        z-index:0;
    }
    .brand-label{
        position:relative;z-index:2;display:flex;align-items:center;gap:8px;margin-bottom:8px;
        color:#38bdf8;font-size:.76rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;
    }
    .brand-dot{width:7px;height:7px;border-radius:50%;background:#38bdf8;box-shadow:0 0 12px rgba(56,189,248,.85);}
    .custom-title{
        position:relative;z-index:2;margin:0;color:#FFFFFF;font-size:2.55rem;line-height:1.15;font-weight:800;
        text-shadow:0 2px 12px rgba(0,180,255,.25);
    }
    .custom-subtitle{position:relative;z-index:2;margin-top:8px;margin-bottom:8px;color:#99d6ff;font-size:1.08rem;font-weight:600;}
    .custom-caption{position:relative;z-index:2;max-width:690px;color:#8fb3d9;font-size:.9rem;line-height:1.6;}
    
    [data-testid="stChatMessage"]{background:transparent;border:none;padding-top:.55rem;padding-bottom:.55rem;}
    [data-testid="stChatMessageContent"]{color:#E2E8F0;font-size:.97rem;line-height:1.7;}
    [data-testid="stChatInput"]{background:rgba(15,23,42,.97);border:1px solid #26344D;border-radius:16px;box-shadow:0 12px 35px rgba(0,0,0,.35);}
    [data-testid="stChatInput"] textarea{color:#F8FAFC!important;}
    [data-testid="stChatInput"] textarea::placeholder{color:#64748B!important;}
    .stButton>button{border-radius:10px;border:1px solid #26344D;background:#111B2E;color:#E2E8F0;}
    .stButton>button:hover{border-color:#38bdf8;color:#FFF;background:#17213A;}
    [data-testid="stAlert"]{border-radius:12px;}
    
    .watermark-center{margin:35px 0 10px;text-align:center;color:rgba(255,255,255,0.35);font-size:.85rem;font-weight:500;letter-spacing:1px;user-select:none;text-shadow:0 1px 2px rgba(0,0,0,.6);}
    .footer-brand{color:#38bdf8;font-weight:700;}
    
    @media(max-width:700px){.custom-title{font-size:2rem}.custom-subtitle{font-size:.98rem}.custom-caption{font-size:.84rem}}
    </style>
    """),
    unsafe_allow_html=True,
)

# ============================================================
# PROMPT MESTRE — LARYMB V1
# ============================================================
CUSTOM_PROMPT = """
Você é a LaryMB V1, uma Inteligência Artificial generalista desenvolvida pela LaryMB AI.

MISSÃO
Compreenda a intenção do usuário e ofereça respostas claras, úteis, didáticas,
objetivas e contextualizadas.

ESCOPO
Você pode ajudar em perguntas gerais, assuntos cotidianos, conhecimentos gerais,
estudos escolares, matemática, português, redação, inglês e outros idiomas,
história, geografia, ciências, biologia, física, química, filosofia, sociologia,
tecnologia, programação, inteligência artificial, ciência de dados, negócios,
produtividade, criatividade, análise de informações, criação, revisão e tradução
de textos, planejamento e organização de ideias.

REGRA PRINCIPAL
Não presuma que o usuário está estudando, programando ou trabalhando com tecnologia.
Primeiro identifique a intenção da pergunta e depois escolha a melhor forma de responder.

CLAREZA
- Para perguntas simples, responda diretamente.
- Para assuntos complexos, organize em etapas.
- Use exemplos quando ajudarem.
- Adapte a profundidade ao nível do usuário.
- Evite respostas desnecessariamente longas.

MODO EDUCACIONAL
Quando o usuário estiver estudando, priorize o aprendizado.
Quando apropriado, use: Explicação → Exemplo → Resolução → Resultado.

MATEMÁTICA
Quando fizer sentido: identifique os dados, apresente a fórmula ou método,
substitua os valores, resolva passo a passo, apresente o resultado e confira-o.

INGLÊS
Ajude com tradução, vocabulário, gramática, pronúncia, interpretação,
conversação, reading, writing, listening, phrasal verbs e expressões.
Quando útil, apresente frase original, tradução, pronúncia aproximada,
explicação e exemplo.

PROGRAMAÇÃO E TECNOLOGIA
Ajude com Python, SQL, JavaScript, HTML, CSS, APIs, bancos de dados,
Git, Docker, cloud, IA, LLM, RAG e automação. Ao gerar código,
priorize segurança, boas práticas, organização e tratamento de erros.

NÃO INVENTAR
Nunca invente informações. Se não souber ou não tiver dados suficientes,
diga claramente. Não apresente hipótese como fato.

TRANSPARÊNCIA
Nunca diga que executou uma ação, consultou uma fonte, acessou um sistema,
enviou uma mensagem ou realizou uma operação se isso não tiver realmente acontecido.

SEGURANÇA
Nunca revele chaves de API, senhas, tokens ou credenciais.

PERSONALIDADE
Seja inteligente, profissional, amigável, didática, natural e respeitosa.
Não seja excessivamente robótica nem excessivamente informal.

OBJETIVO FINAL
Antes de responder, verifique: entendi a pergunta? Respondi ao que foi solicitado?
Evitei inventar? A explicação está clara? O nível está adequado?

Prioridades: PRECISÃO → CLAREZA → UTILIDADE → SEGURANÇA → EXPERIÊNCIA

Você é LaryMB V1.
Inteligência que transforma perguntas em soluções.
"""

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(
        textwrap.dedent("""
        <div style="font-size:1.15rem;font-weight:750;color:#F8FAFC;">✦ LaryMB AI</div>
        <div style="font-size:.82rem;color:#64748B;margin-top:5px;">Inteligência Artificial • V1</div>
        <div style="color:#94A3B8;font-size:.88rem;line-height:1.55;margin-top:20px;">
        Uma IA para responder perguntas, aprender, criar, analisar informações e ajudar você a resolver problemas.
        </div>
        """),
        unsafe_allow_html=True,
    )
    st.markdown("---")

    groq_api_key = st.secrets.get("GROQ_API_KEY", "")
    if not groq_api_key:
        groq_api_key = st.text_input(
            "Chave da API Groq",
            type="password",
            help="Recomendado: configure GROQ_API_KEY nos Secrets do Streamlit Cloud.",
        )

    st.markdown("---")
    st.info("A LaryMB pode cometer erros. Verifique informações importantes antes de tomar decisões.")

    with st.expander("✦ Suporte / Fale conosco"):
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
# HEADER — IMPORTANTE: HTML SEM INDENTAÇÃO DO MARKDOWN
# ============================================================
st.markdown(
    textwrap.dedent("""
    <div class="custom-header">
        <div class="brand-label"><span class="brand-dot"></span>LaryMB AI</div>
        <div class="custom-title">LaryMB V1</div>
        <div class="custom-subtitle">Sua inteligência artificial para aprender, criar, analisar e resolver.</div>
        <div class="custom-caption">Faça perguntas, explore ideias, estude, programe, analise informações e obtenha respostas claras e contextualizadas.</div>
    </div>
    """),
    unsafe_allow_html=True,
)

# ============================================================
# HISTÓRICO
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
# CHAT
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

# ============================================================
# RODAPÉ
# ============================================================
st.markdown(
    textwrap.dedent("""
    <div class="watermark-center">
        <span class="footer-brand">✦ LaryMB AI</span>&nbsp;•&nbsp;V1&nbsp;•&nbsp;Inteligência que transforma perguntas em soluções.
    </div>
    """),
    unsafe_allow_html=True,
)
