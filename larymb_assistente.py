import streamlit as st
from groq import Groq

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="LaryMB AI — V1",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ============================================================
# DESIGN — LARYMB AI
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       FUNDO PRINCIPAL
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 50% -10%,
                rgba(124, 140, 255, 0.12),
                transparent 40%
            ),
            linear-gradient(
                135deg,
                #080D1A 0%,
                #0A1020 50%,
                #050914 100%
            );

        color: #F8FAFC;
    }

    /* Remove espaços excessivos do topo */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 6rem;
        max-width: 900px;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {
        background: #0B1220;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    [data-testid="stSidebar"] h1 {
        color: #F8FAFC;
        font-size: 1.15rem;
        font-weight: 700;
    }

    [data-testid="stSidebar"] p {
        color: #94A3B8;
        font-size: 0.9rem;
        line-height: 1.5;
    }


    /* ========================================================
       HEADER PRINCIPAL
       ======================================================== */

    .custom-header {

        position: relative;

        padding: 34px 30px;

        background:
            linear-gradient(
                145deg,
                rgba(17, 28, 50, 0.92),
                rgba(10, 18, 34, 0.88)
            );

        border: 1px solid rgba(255,255,255,0.08);

        border-radius: 18px;

        box-shadow:
            0 20px 50px rgba(0,0,0,0.35),
            inset 0 1px 0 rgba(255,255,255,0.03);

        backdrop-filter: blur(14px);

        margin-bottom: 28px;

        overflow: hidden;
    }


    /* Marca d'água */

    .custom-header::before {

        content: "LARYMB";

        position: absolute;

        right: -25px;
        top: -28px;

        font-size: 125px;

        font-weight: 900;

        letter-spacing: 8px;

        color: rgba(124,140,255,0.035);

        z-index: 0;

        pointer-events: none;
    }


    /* Pequeno brilho */

    .custom-header::after {

        content: "";

        position: absolute;

        width: 180px;
        height: 180px;

        right: -80px;
        bottom: -100px;

        background: rgba(124,140,255,0.08);

        filter: blur(60px);

        border-radius: 50%;

        pointer-events: none;
    }


    /* ========================================================
       IDENTIDADE
       ======================================================== */

    .brand-label {

        display: inline-flex;

        align-items: center;

        gap: 8px;

        font-size: 0.78rem;

        font-weight: 700;

        letter-spacing: 1.2px;

        text-transform: uppercase;

        color: #A78BFA;

        margin-bottom: 8px;

        position: relative;

        z-index: 2;
    }


    .brand-dot {

        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #7C8CFF;

        box-shadow:
            0 0 12px rgba(124,140,255,0.8);
    }


    /* ========================================================
       TÍTULO
       ======================================================== */

    .custom-title {

        font-size: 2.65rem;

        line-height: 1.15;

        font-weight: 800;

        letter-spacing: -1px;

        color: #F8FAFC;

        margin: 0;

        position: relative;

        z-index: 2;
    }


    /* ========================================================
       SUBTÍTULO
       ======================================================== */

    .custom-subtitle {

        font-size: 1.15rem;

        font-weight: 500;

        color: #A5B4FC;

        margin-top: 10px;

        margin-bottom: 10px;

        position: relative;

        z-index: 2;
    }


    /* ========================================================
       DESCRIÇÃO
       ======================================================== */

    .custom-caption {

        font-size: 0.92rem;

        line-height: 1.6;

        color: #94A3B8;

        max-width: 650px;

        position: relative;

        z-index: 2;
    }


    /* ========================================================
       CHAT
       ======================================================== */

    [data-testid="stChatMessage"] {

        background: transparent;

        border: none;

        padding-top: 0.8rem;

        padding-bottom: 0.8rem;
    }


    /* Avatar */

    [data-testid="stChatMessageAvatarUser"] {

        background: #7C8CFF !important;
    }


    [data-testid="stChatMessageAvatarAssistant"] {

        background: #A78BFA !important;
    }


    /* Texto das mensagens */

    [data-testid="stChatMessageContent"] {

        color: #E2E8F0;

        font-size: 0.98rem;

        line-height: 1.7;
    }


    /* ========================================================
       INPUT DO CHAT
       ======================================================== */

    [data-testid="stChatInput"] {

        background: rgba(15, 23, 42, 0.95);

        border: 1px solid #26344D;

        border-radius: 16px;

        box-shadow:
            0 12px 35px rgba(0,0,0,0.35);
    }


    [data-testid="stChatInput"] textarea {

        color: #F8FAFC !important;

        font-size: 0.98rem;
    }


    [data-testid="stChatInput"] textarea::placeholder {

        color: #64748B !important;
    }


    /* ========================================================
       BOTÕES
       ======================================================== */

    .stButton > button {

        border-radius: 10px;

        border: 1px solid #26344D;

        background: #111B2E;

        color: #E2E8F0;

        transition: all 0.2s ease;
    }


    .stButton > button:hover {

        border-color: #7C8CFF;

        color: #FFFFFF;

        background: #17213A;
    }


    /* ========================================================
       DIVISOR
       ======================================================== */

    hr {

        border-color: rgba(255,255,255,0.07);
    }


    /* ========================================================
       ALERTA
       ======================================================== */

    [data-testid="stAlert"] {

        background: rgba(30,41,59,0.65);

        border: 1px solid rgba(148,163,184,0.15);

        color: #CBD5E1;

        border-radius: 12px;
    }


    /* ========================================================
       RODAPÉ
       ======================================================== */

    .watermark-center {

        text-align: center;

        color: #64748B;

        font-size: 0.78rem;

        font-weight: 500;

        letter-spacing: 0.5px;

        margin: 35px 0 10px;

        user-select: none;
    }


    .footer-brand {

        color: #7C8CFF;

        font-weight: 700;
    }


    /* ========================================================
       RESPONSIVO
       ======================================================== */

    @media (max-width: 700px) {

        .custom-header {

            padding: 26px 22px;

            border-radius: 14px;
        }

        .custom-title {

            font-size: 2rem;
        }

        .custom-subtitle {

            font-size: 1rem;
        }

        .custom-caption {

            font-size: 0.85rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PROMPT MESTRE — LARYMB V1
# ============================================================

CUSTOM_PROMPT = """
Você é LaryMB V1, uma Inteligência Artificial generalista desenvolvida pela LaryMB AI.

A LaryMB V1 deve responder perguntas gerais sobre assuntos cotidianos,
conhecimentos gerais, educação, tecnologia, programação, idiomas, negócios,
produtividade, criatividade, análise, estudos e outros temas dentro de sua
capacidade.

Ela não deve assumir que o usuário está necessariamente estudando,
programando ou trabalhando com tecnologia.

Primeiro identifique a intenção da pergunta e, em seguida, escolha a melhor
forma de responder.

A LaryMB V1 deve adaptar automaticamente sua linguagem, profundidade,
estrutura e abordagem ao contexto e ao objetivo do usuário.

============================================================
MISSÃO
============================================================

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
- Planejar projetos;
- Apoiar decisões;
- Aumentar produtividade.

Seu objetivo é transformar perguntas, informações e problemas em respostas
claras, úteis, práticas e confiáveis.

============================================================
PRINCÍPIOS FUNDAMENTAIS
============================================================

1. NÃO INVENTAR INFORMAÇÕES

Nunca invente informações.

Quando não souber algo, diga claramente que não possui informação suficiente.

Nunca transforme hipótese em fato.

2. PRECISÃO

Priorize respostas corretas e confiáveis.

Quando houver incerteza, informe isso ao usuário.

3. CLAREZA

Responda de maneira clara e objetiva.

Evite linguagem excessivamente técnica quando ela não for necessária.

Quando o assunto for complexo, divida a explicação em etapas.

4. CONTEXTO

Utilize o contexto disponível na conversa.

Não peça novamente informações que o usuário já forneceu.

============================================================
PERSONALIDADE
============================================================

A LaryMB V1 deve ser:

- Inteligente;
- Profissional;
- Educada;
- Didática;
- Objetiva;
- Natural;
- Estratégica;
- Colaborativa;
- Respeitosa;
- Segura.

Não seja excessivamente robótica.

Não seja excessivamente informal.

Adapte o tom ao usuário e ao contexto.

============================================================
PERGUNTAS GERAIS
============================================================

A LaryMB V1 pode responder perguntas sobre diferentes áreas.

O usuário não precisa escolher uma categoria antes de perguntar.

Identifique automaticamente o assunto e responda da maneira mais adequada.

Para perguntas simples, seja direta.

Para perguntas complexas, organize a resposta.

============================================================
MODO EDUCACIONAL
============================================================

A LaryMB V1 também atua como Assistente Educacional Inteligente.

Pode auxiliar em:

- Matemática;
- Português;
- Literatura;
- Redação;
- Inglês;
- Espanhol;
- História;
- Geografia;
- Ciências;
- Biologia;
- Física;
- Química;
- Filosofia;
- Sociologia;
- Informática;
- Estatística;
- Programação;
- Inteligência Artificial;
- Ciência de Dados;
- Outras áreas acadêmicas.

Quando o usuário estiver estudando, priorize compreensão.

Sempre que apropriado:

Explicação → Exemplo → Resolução → Resultado

============================================================
INGLÊS E IDIOMAS
============================================================

A LaryMB V1 pode atuar como tutora de idiomas.

Auxilie em:

- Tradução;
- Vocabulário;
- Gramática;
- Tempos verbais;
- Pronúncia;
- Interpretação;
- Conversação;
- Reading;
- Writing;
- Listening;
- Phrasal verbs;
- Expressões.

Quando útil, apresente:

Frase original;
Tradução;
Pronúncia aproximada;
Explicação;
Exemplo.

============================================================
MATEMÁTICA
============================================================

Para exercícios matemáticos:

1. Identifique os dados;
2. Apresente a fórmula ou método;
3. Substitua os valores;
4. Resolva passo a passo;
5. Apresente o resultado;
6. Verifique o resultado quando possível.

============================================================
PROGRAMAÇÃO E TECNOLOGIA
============================================================

A LaryMB V1 pode auxiliar em:

- Python;
- SQL;
- JavaScript;
- HTML;
- CSS;
- APIs;
- Banco de dados;
- Cloud;
- Docker;
- Git;
- Inteligência Artificial;
- LLM;
- RAG;
- Automação;
- Desenvolvimento de software.

Quando gerar código:

- Priorize segurança;
- Utilize boas práticas;
- Organize o código;
- Explique os pontos importantes;
- Inclua tratamento de erros quando necessário.

Nunca exponha chaves de API, senhas ou tokens.

============================================================
DOCUMENTOS
============================================================

Quando o usuário fornecer documentos, utilize prioritariamente as informações
presentes nesses documentos.

Não invente conteúdo que não esteja disponível.

============================================================
ANÁLISE DE PROBLEMAS
============================================================

Para problemas complexos:

1. Entender;
2. Analisar;
3. Planejar;
4. Resolver;
5. Validar;
6. Melhorar.

============================================================
TRANSPARÊNCIA
============================================================

Nunca afirme ter realizado uma ação que não realizou.

Nunca diga que consultou uma fonte, executou um código, enviou um e-mail,
salvou um arquivo ou alterou um sistema se isso não tiver realmente acontecido.

============================================================
SEGURANÇA
============================================================

Proteja informações confidenciais.

Nunca solicite informações sensíveis sem necessidade.

Nunca exponha senhas, tokens, chaves de API ou credenciais.

============================================================
OBJETIVO FINAL
============================================================

Antes de finalizar uma resposta, verifique:

- Entendi a pergunta?
- Respondi exatamente ao que foi solicitado?
- A informação está correta?
- Evitei inventar?
- A explicação está clara?
- O nível está adequado?
- O próximo passo está claro?

Prioridades:

PRECISÃO → CLAREZA → UTILIDADE → SEGURANÇA → EXPERIÊNCIA

Você é LaryMB V1.

Sua função é compreender a necessidade do usuário e fornecer a melhor
resposta possível dentro das informações e ferramentas disponíveis.

LaryMB V1 — Inteligência que transforma perguntas em soluções.
"""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size: 1.15rem;
            font-weight: 750;
            color: #F8FAFC;
            margin-bottom: 8px;
        ">
            ✦ LaryMB AI
        </div>

        <div style="
            font-size: 0.82rem;
            color: #64748B;
            margin-bottom: 20px;
        ">
            Inteligência artificial • V1
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            color: #94A3B8;
            font-size: 0.88rem;
            line-height: 1.6;
            margin-bottom: 20px;
        ">
            Uma IA para responder perguntas, aprender, criar, analisar
            informações e ajudar você a resolver problemas.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # API KEY
    # ========================================================

    groq_api_key = None

    if "GROQ_API_KEY" in st.secrets:

        groq_api_key = st.secrets["GROQ_API_KEY"]

    if not groq_api_key:

        groq_api_key = st.text_input(
            "Chave da API Groq",
            type="password",
            help="Configure sua chave da Groq nos Secrets do Streamlit Cloud."
        )


    st.markdown("---")


    # ========================================================
    # AVISO
    # ========================================================

    st.info(
        "A LaryMB pode cometer erros. "
        "Verifique informações importantes antes de tomar decisões."
    )


    # ========================================================
    # SUPORTE
    # ========================================================

    with st.expander("✦ Suporte / Fale conosco"):

        st.markdown(
            """
            <div style="
                color: #94A3B8;
                font-size: 0.88rem;
                line-height: 1.5;
                margin-bottom: 12px;
            ">
                Encontrou um problema ou precisa de ajuda?
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "**E-mail:** sergiolmendes2026@gmail.com"
        )

        whatsapp_url = (
            "https://wa.me/55994376755"
            "?text=Ol%C3%A1%2C%20vim%20pelo%20Agente%20IA%20LaryMB!"
        )

        st.markdown(
            f"""
            <a
                href="{whatsapp_url}"
                target="_blank"
                style="
                    display: block;
                    width: 100%;
                    box-sizing: border-box;
                    text-align: center;
                    text-decoration: none;
                    background: #111B2E;
                    color: #E2E8F0;
                    border: 1px solid #26344D;
                    padding: 11px;
                    border-radius: 10px;
                    font-weight: 600;
                    transition: 0.2s;
                "
            >
                Falar no WhatsApp
            </a>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="custom-header">

        <div class="brand-label">
            <span class="brand-dot"></span>
            LaryMB AI
        </div>

        <div class="custom-title">
            LaryMB V1
        </div>

        <div class="custom-subtitle">
            Sua inteligência artificial para aprender, criar, analisar e resolver.
        </div>

        <div class="custom-caption">
            Faça perguntas, explore ideias, estude, programe, analise informações
            e obtenha respostas claras e contextualizadas.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HISTÓRICO
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# EXIBE MENSAGENS ANTERIORES
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# CLIENTE GROQ
# ============================================================

client = None

if groq_api_key:

    try:

        client = Groq(
            api_key=groq_api_key
        )

    except Exception as e:

        st.sidebar.error(
            f"Erro ao inicializar o cliente Groq: {e}"
        )

        st.stop()

elif st.session_state.messages:

    st.warning(
        "Configure sua API Key da Groq para continuar."
    )


# ============================================================
# CHAT
# ============================================================

if prompt := st.chat_input("Pergunte qualquer coisa..."):

    if not client:

        st.warning(
            "Configure sua API Key da Groq na barra lateral para começar."
        )

        st.stop()


    # ========================================================
    # USUÁRIO
    # ========================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    with st.chat_message("user"):

        st.markdown(prompt)


    # ========================================================
    # MENSAGENS PARA API
    # ========================================================

    messages_for_api = [
        {
            "role": "system",
            "content": CUSTOM_PROMPT
        }
    ]


    for msg in st.session_state.messages:

        messages_for_api.append(msg)


    # ========================================================
    # RESPOSTA DA IA
    # ========================================================

    with st.chat_message("assistant"):

        with st.spinner("LaryMB está pensando..."):

            try:

                chat_completion = client.chat.completions.create(

                    messages=messages_for_api,

                    model="openai/gpt-oss-120b",

                    temperature=0.7,

                    max_tokens=2048,
                )


                dsa_ai_resposta = (
                    chat_completion
                    .choices[0]
                    .message
                    .content
                )


                st.markdown(
                    dsa_ai_resposta
                )


                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": dsa_ai_resposta
                    }
                )


            except Exception as e:

                st.error(
                    "Ocorreu um erro ao se comunicar com a API da Groq."
                )

                st.caption(
                    f"Detalhes técnicos: {e}"
                )


# ============================================================
# RODAPÉ
# ============================================================

st.markdown(
    """
    <div class="watermark-center">
        <span class="footer-brand">✦ LaryMB AI</span>
        &nbsp;•&nbsp;
        V1
        &nbsp;•&nbsp;
        Inteligência que transforma perguntas em soluções.
    </div>
    """,
    unsafe_allow_html=True
)
