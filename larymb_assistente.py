import streamlit as st
from groq import Groq

# Configuração da página
st.set_page_config(
    page_title="Agente de IA LaryMB v1",
    page_icon="🤖",
    layout="centered"
)

# ==========================================
# DESIGN: Azul Petróleo Brilhante & Marca d'Água
# ==========================================
st.markdown(
    """
    <style>
    /* Fundo geral da aplicação com degradê brilhante de azul petróleo elegante */
    .stApp {
        background: radial-gradient(circle at 50% 20%, #015c6b 0%, #003642 55%, #001e26 100%);
        color: #ffffff;
    }

    /* Container do Cabeçalho com Efeito de Marca d'Água Tipográfica ao Fundo */
    .custom-header {
        position: relative;
        padding: 30px 20px;
        background: rgba(0, 45, 56, 0.45);
        border: 1px solid rgba(0, 209, 255, 0.18);
        border-radius: 12px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        margin-bottom: 25px;
        overflow: hidden;
    }

    /* Marca d'água grande e sutil no fundo do cabeçalho */
    .custom-header::before {
        content: "LARYMB";
        position: absolute;
        right: -10px;
        top: -20px;
        font-size: 130px;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.03);
        z-index: 0;
        pointer-events: none;
        letter-spacing: 8px;
    }

    /* Títulos com brilho e elegância */
    .custom-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        text-shadow: 0 2px 12px rgba(0, 225, 255, 0.35);
        margin-bottom: 0px;
        position: relative;
        z-index: 1;
    }

    .custom-subtitle {
        font-size: 1.3rem;
        font-weight: 500;
        color: #99e6ff;
        margin-top: 5px;
        margin-bottom: 10px;
        position: relative;
        z-index: 1;
    }

    .custom-caption {
        font-size: 0.9rem;
        color: #b3d1db;
        position: relative;
        z-index: 1;
    }

    /* Marca d'água centralizada e discreta na tela */
    .watermark-center {
        text-align: center;
        color: rgba(255, 255, 255, 0.22);
        font-size: 0.82rem;
        font-weight: 500;
        letter-spacing: 1.2px;
        margin: 30px 0;
        user-select: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Prompt de sistema padrão
CUSTOM_PROMPT = "Você é um assistente de IA amigável e prestativo chamado LaryMB, focado em ajudar iniciantes em tecnologia e programação."

# Cria o conteúdo da barra lateral no Streamlit
with st.sidebar:
    st.title("🤖 Agente de IA LaryMB.V1")
    st.markdown("Um Agente de IA focado para ajudar iniciantes.")
    
    # Tenta puxar a chave dos segredos do Streamlit Cloud de forma segura
    groq_api_key = None
    if "GROQ_API_KEY" in st.secrets:
        groq_api_key = st.secrets["GROQ_API_KEY"]
    
    # Se não encontrar nos segredos, mostra o campo para digitar manualmente
    if not groq_api_key:
        groq_api_key = st.text_input(
            "Insira sua API Key Groq", 
            type="password",
            help="Obtenha sua chave em https://console.groq.com/keys"
        )

    st.markdown("---")
    
    # Caixa de aviso destacada
    st.info("Aviso: IA pode gerar respostas imprecisas, incompletas ou erradas. Sempre verifique informações críticas antes de confiar totalmente no conteúdo gerado.")

    # Menu expansível para o Suporte / WhatsApp
    with st.expander("SOS - Suporte / Fale conosco"):
        st.markdown("Se tiver dúvidas envie mensagem para\n**sergiolmendes2026@gmail.com**")
        
        whatsapp_url = "https://wa.me/55994376755?text=Olá,%20vim%20pelo%20Agente%20IA%20LaryMB!"
        st.markdown(
            f'''
            <a href="{whatsapp_url}" target="_blank" style="text-decoration: none; color: inherit;">
                <button style="width: 100%; background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 5px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; text-decoration: none;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M13.601 2.326A7.85 7.85 0 0 0 7.994 0C3.627 0 .068 3.558.068 7.932c0 1.397.362 2.764 1.059 3.965L0 16l4.202-1.103a7.85 7.85 0 0 0 3.792.967h.004c4.365 0 7.926-3.558 7.926-7.93 0-2.11-.822-4.094-2.323-5.604zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.53 6.53 0 0 1 4.639 1.933 6.52 6.52 0 0 1 1.925 4.637c-.001 3.633-2.958 6.59-6.591 6.59zm3.633-4.97c-.199-.1-1.177-.581-1.359-.648-.182-.066-.314-.1-.448.1-.134.2-.517.648-.634.782-.117.133-.235.15-.434.05-.199-.1-.841-.31-1.603-.99-.592-.528-.992-1.181-1.109-1.38-.117-.199-.012-.307.087-.406.09-.089.199-.232.298-.348.1-.116.133-.199.199-.332.066-.133.033-.248-.017-.348-.05-.1-.448-1.078-.614-1.478-.161-.391-.325-.338-.448-.344l-.382-.007c-.133 0-.348.05-.53.248-.183.199-.701.685-.701 1.67 0 .985.718 1.937.818 2.07.1.133 1.41 2.155 3.417 3.022.477.206.849.33 1.139.423.479.153.915.131 1.259.08.384-.057 1.177-.481 1.343-.946.166-.465.166-.864.116-.946-.05-.084-.183-.133-.382-.232z"/>
                    </svg>
                    Falar no WhatsApp
                </button>
            </a>
            ''',
            unsafe_allow_html=True
        )

# Cabeçalho Visual Customizado
st.markdown(
    """
    <div class="custom-header">
        <div class="custom-title">Agente de IA LaryMB v1</div>
        <div class="custom-subtitle">Seu guia inteligente para iniciantes</div>
        <div class="custom-caption">Faça sua pergunta e obtenha respostas, explicações e referências.</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Inicializa o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

client = None

if groq_api_key:
    try:
        client = Groq(api_key=groq_api_key)
    except Exception as e:
        st.sidebar.error(f"Erro ao inicializar o cliente Groq: {e}")
        st.stop()
elif st.session_state.messages:
    st.warning("Por favor, insira sua API Key da Groq na barra lateral para continuar.")

# Entrada do usuário via chat
if prompt := st.chat_input("Qual sua dúvida?"):
    if not client:
        st.warning("Por favor, insira sua API Key da Groq na barra lateral para começar.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:
        messages_for_api.append(msg)

    with st.chat_message("assistant"):
        with st.spinner("Analisando sua pergunta..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=messages_for_api,
                    model="openai/gpt-oss-120b", 
                    temperature=0.7,
                    max_tokens=2048,
                )
                
                dsa_ai_resposta = chat_completion.choices[0].message.content
                st.markdown(dsa_ai_resposta)
                st.session_state.messages.append({"role": "assistant", "content": dsa_ai_resposta})

            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq: {e}")

# Rodapé com Marca d'Água
st.markdown(
    """
    <div class="watermark-center">
        Agente de IA LaryMB v1 — Acessível, confiável e útil para quem está começando.
    </div>
    """,
    unsafe_allow_html=True
)
