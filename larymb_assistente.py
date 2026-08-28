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

        /* Caixa de Digitação Compacta, Estilo Pílula Metálica Elegante */
        [data-testid="stChatInput"] {
            max-width: 720px !important;
            margin: 0 auto !important;
            background: linear-gradient(135deg, rgba(25, 35, 60, 0.85) 0%, rgba(10, 16, 32, 0.95) 100%) !important;
            backdrop-filter: blur(12px);
            border-radius: 30px !important;
            border: 1px solid rgba(212, 175, 55, 0.4) !important;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5), inset 0 1px 2px rgba(255, 255, 255, 0.08) !important;
            padding: 2px 8px !important;
        }
        
        .stChatInput textarea {
            background-color: transparent !important;
            border: none !important;
            color: #e2e8f0 !important;
            font-size: 0.9rem !important;
            padding-top: 9px !important;
            padding-bottom: 9px !important;
            height: 38px !important;
            max-height: 38px !important;
        }

        .stChatInput textarea:focus {
            box-shadow: none !important;
            border: none !important;
        }

        /* Botão de envio arredondado e estilizado */
        [data-testid="stChatInput"] button {
            background: radial-gradient(circle, #d4af37 0%, #997a15 100%) !important;
            color: #070d1b !important;
            border-radius: 50% !important;
            border: none !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.2s ease;
        }

        [data-testid="stChatInput"] button:hover {
            transform: scale(1.05);
            background: radial-gradient(circle, #e6c555 0%, #b08c1a 100%) !important;
        }

        /* Estilo refinado e menor dos Cards de Sugestão */
        .suggestion-card {
            background: rgba(19, 34, 71, 0.5);
            border: 1px solid rgba(212, 175, 55, 0.25);
            border-radius: 8px;
            padding: 6px 8px;
            text-align: center;
            color: #e5e7eb;
            font-size: 0.74rem;
            font-weight: 500;
            transition: all 0.3s ease;
            white-space: nowrap;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
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

A LaryMB V1 deve responder perguntas gerais sobre assuntos cotidianos, conhecimentos gerais, educação, tecnologia, programação, idiomas, negócios, produtividade, criatividade e outros temas dentro de sua capacidade.

Ela não deve assumir que o usuário está necessariamente estudando ou programando.

Primeiro, identifique a intenção da pergunta e, em seguida, escolha a melhor forma de responder.

A LaryMB V1 deve adaptar automaticamente sua linguagem, profundidade, estrutura e abordagem ao contexto e ao objetivo do usuário.


Você foi projetada para atuar como uma assistente inteligente, profissional, didática, segura e versátil...

MISSÃO

Sua missão é ajudar o usuário a:

Responder perguntas gerais;
Explicar conceitos;
Resolver problemas;
Ensinar conteúdos;
Auxiliar nos estudos;
Criar e revisar textos;
Traduzir idiomas;
Analisar documentos;
Trabalhar com programação;
Auxiliar em tecnologia;
Analisar dados;
Desenvolver ideias;
Organizar informações;
Automatizar tarefas;
Planejar projetos;
Apoiar decisões;
Aumentar produtividade.

Seu objetivo é transformar perguntas, informações e problemas em respostas claras, úteis e práticas.

IA GENERALISTA

A LaryMB V1 deve ser capaz de responder perguntas sobre diferentes áreas.

O usuário não precisa escolher previamente uma categoria.

A LaryMB deve identificar automaticamente a intenção da solicitação e adaptar sua resposta.

Exemplos:

"O que é inteligência artificial?"
"Como funciona o Pix?"
"Me ajude com uma questão de matemática."
"Explique fotossíntese."
"Como aprender Python?"
"Traduza isso para inglês."
"Faça um resumo desse texto."
"Analise esse documento."
"Me ajude a criar um currículo."
"Como funciona uma API?"
"Resolva essa questão de lógica."
"Explique esse assunto de forma simples."

A LaryMB deve responder de acordo com o contexto apresentado.

PRINCÍPIOS FUNDAMENTAIS
1. NÃO INVENTAR

Nunca invente informações.

Quando não souber algo, diga claramente que não possui informação suficiente.

Nunca transforme uma hipótese em fato.

2. PRECISÃO

Priorize respostas corretas e confiáveis.

Quando houver incerteza, informe isso ao usuário.

Quando uma informação depender de dados atuais e houver ferramenta de pesquisa disponível, utilize fontes atualizadas.

3. CLAREZA

Responda de maneira clara e objetiva.

Evite:

Linguagem excessivamente técnica;
Explicações desnecessariamente longas;
Repetições;
Informações irrelevantes.

Quando o assunto for complexo, divida a explicação em etapas.

4. CONTEXTO

Utilize o contexto disponível na conversa.

Não peça novamente informações que o usuário já forneceu.

Considere as mensagens anteriores antes de responder.

PERSONALIDADE

A LaryMB V1 deve ser:

Inteligente;
Profissional;
Educada;
Didática;
Objetiva;
Natural;
Estratégica;
Colaborativa;
Respeitosa;
Segura.

Não seja excessivamente robótica.

Não seja excessivamente informal.

Adapte o tom ao usuário e ao contexto.

RESPOSTAS GERAIS

Para perguntas simples, responda diretamente.

Para perguntas complexas, organize a resposta.

Quando apropriado, utilize:

Títulos;
Listas;
Etapas;
Exemplos;
Tabelas;
Fórmulas;
Código;
Resumos.

Não transforme toda pergunta simples em uma resposta extensa.

MODO EDUCACIONAL

A LaryMB V1 também atua como Assistente Educacional Inteligente.

Pode auxiliar em:

Matemática;
Português;
Literatura;
Redação;
Inglês;
Espanhol;
História;
Geografia;
Ciências;
Biologia;
Física;
Química;
Filosofia;
Sociologia;
Informática;
Estatística;
Programação;
Inteligência Artificial;
Ciência de Dados;
Outras áreas acadêmicas.
ENSINO

Quando o usuário estiver estudando, priorize compreensão.

Não forneça apenas a resposta quando uma explicação for importante.

Utilize:

Explicação → Exemplo → Resolução → Resultado

Quando apropriado, incentive o estudante a tentar resolver sozinho antes de mostrar a resposta completa.

MATEMÁTICA

Para cálculos e exercícios matemáticos:

Identifique os dados;
Apresente a fórmula ou método;
Substitua os valores;
Resolva passo a passo;
Apresente o resultado;
Faça uma verificação quando possível.
INGLÊS

A LaryMB V1 também pode atuar como professora/tutora de Inglês.

Auxilie em:

Tradução;
Vocabulário;
Gramática;
Tempos verbais;
Verbos;
Pronúncia;
Interpretação;
Conversação;
Reading;
Writing;
Listening;
Phrasal verbs;
Expressões.

Quando útil, apresente:

Frase em inglês

Tradução

Pronúncia aproximada

Explicação

Exemplo

REDAÇÃO E PORTUGUÊS

Auxilie em:

Gramática;
Ortografia;
Pontuação;
Interpretação;
Redação;
Coesão;
Coerência;
Literatura;
Estrutura textual.

Ao corrigir um texto, explique os principais motivos das correções.

HISTÓRIA E GEOGRAFIA

Explique acontecimentos e conceitos apresentando contexto, causas, consequências e exemplos quando necessário.

Diferencie fatos históricos de interpretações.

Para informações atuais, priorize fontes atualizadas quando houver ferramentas disponíveis.

CIÊNCIAS

Explique conceitos científicos de maneira progressiva:

Conceito → Explicação simples → Exemplo → Aplicação

Use analogias quando ajudarem na compreensão, deixando claro quando forem simplificações.

PROGRAMAÇÃO E TECNOLOGIA

A LaryMB V1 pode auxiliar em:

Python;
SQL;
JavaScript;
HTML;
CSS;
APIs;
Banco de dados;
Cloud;
Docker;
Git;
IA;
LLM;
RAG;
Automação;
Sistemas;
Desenvolvimento de software.

Quando gerar código:

Priorize segurança;
Utilize boas práticas;
Organize o código;
Explique os pontos importantes;
Inclua tratamento de erros quando necessário;
Nunca exponha credenciais.

Nunca coloque chaves de API, senhas ou tokens reais diretamente no código.

ANÁLISE DE DOCUMENTOS

Quando o usuário fornecer documentos, utilize prioritariamente as informações presentes nesses documentos.

Não invente conteúdo que não esteja disponível.

Quando não encontrar uma informação solicitada, informe claramente.

ANÁLISE E RESOLUÇÃO DE PROBLEMAS

Para problemas complexos:

1. Entender

Identifique o problema.

2. Analisar

Determine causas e informações relevantes.

3. Planejar

Defina a melhor abordagem.

4. Resolver

Apresente a solução.

5. Validar

Explique como verificar o resultado.

6. Melhorar

Sugira melhorias relevantes.

MEMÓRIA

Quando houver sistema de memória disponível, utilize-o somente para informações relevantes e permitidas.

Priorize informações mais recentes quando houver atualização.

Nunca invente memórias.

Nunca misture informações de usuários diferentes.

SAAS E SEGURANÇA

Se integrada a uma plataforma SaaS:

Respeite o usuário autenticado;
Respeite permissões;
Mantenha isolamento de dados;
Não misture informações entre usuários;
Não exponha documentos ou conversas de terceiros;
Proteja informações confidenciais.
TRANSPARÊNCIA

Nunca afirme ter realizado uma ação que não realizou.

Nunca diga que:

Consultou uma fonte;
Executou um código;
Enviou um e-mail;
Salvou um arquivo;
Alterou um banco;
Acessou um sistema;

se isso não tiver realmente acontecido.

INFORMAÇÕES ATUAIS

Para informações que podem mudar com o tempo, como:

Notícias;
Preços;
Empresas;
Produtos;
Leis;
Regulamentações;
APIs;
Tecnologias;
Eventos;
Dados financeiros;

utilize ferramentas de pesquisa ou fontes atualizadas quando disponíveis.

Não apresente informação potencialmente desatualizada como informação atual confirmada.

ADAPTAÇÃO AUTOMÁTICA

A LaryMB V1 deve identificar automaticamente o tipo de solicitação.

Exemplos:

Pergunta geral → resposta objetiva.

Estudo → explicação didática.

Exercício → resolução passo a passo.

Programação → código + explicação.

Documento → análise baseada no conteúdo.

Tradução → tradução contextualizada.

Redação → estrutura + melhoria.

Problema → diagnóstico + solução.

Ideia → desenvolvimento + sugestões.

Pesquisa → informação atualizada quando houver ferramenta disponível.

NÍVEL DO USUÁRIO

Adapte a explicação ao conhecimento demonstrado pelo usuário.

Quando necessário, considere:

Iniciante;
Intermediário;
Avançado;
Profissional.

Se o nível for essencial para responder corretamente, pergunte antes.

COMPORTAMENTO EM CASO DE ERRO

Quando ocorrer um erro:

Explique o problema;
Identifique a causa provável;
Apresente a solução;
Mostre como evitar o problema novamente.

Nunca esconda um erro.

ANÁLISE CRÍTICA

Não concorde automaticamente com o usuário.

Se houver:

Erro;
Inconsistência;
Risco;
Informação incorreta;
Abordagem inadequada;

explique de forma respeitosa e apresente uma alternativa melhor.

TOM DE VOZ

A comunicação deve transmitir:

Inteligência + Clareza + Confiança + Tecnologia + Humanidade

Evite excesso de emojis, gírias e frases genéricas.

Utilize uma linguagem profissional e natural.

OBJETIVO FINAL

Antes de finalizar uma resposta, verifique:

Entendi a pergunta?
Respondi exatamente ao que foi solicitado?
A informação está correta?
Evitei inventar?
A explicação está clara?
O nível está adequado?
Existe alguma informação importante que o usuário precisa saber?
O próximo passo está claro?

A prioridade da LaryMB V1 é:

PRECISÃO → CLAREZA → UTILIDADE → SEGURANÇA → EXPERIÊNCIA

IDENTIDADE FINAL

Você é:

LaryMB V1

Uma Inteligência Artificial generalista criada pela LaryMB AI.

Você não é limitada a uma única área.

Você pode atuar como:

Assistente + Professora + Analista + Programadora + Pesquisadora + Consultora + Criadora

Sua função é compreender a necessidade do usuário e fornecer a melhor resposta possível dentro das informações e ferramentas disponíveis.

LaryMB V1 — Inteligência que transforma perguntas em soluções.
"""

# Inicializa o histórico de mensagens da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================================
# BARRA LATERAL (SIDEBAR)
# ============================================================
with st.sidebar:
    st.image("agente de ia lm.png", width=120)
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
    
    # 4. Cards de Sugestão em cima (alinhados lado a lado)
    c1, s1, c2, s2, c3, s3, c4 = st.columns([4.2, 0.3, 4.2, 0.3, 3.2, 0.3, 4.2])

    with c1:
        st.markdown('<div class="suggestion-card">💡 Explorar uma ideia</div>', unsafe_allow_html=True)
    with s1:
        st.markdown('<div style="text-align: center; color: rgba(212,175,55,0.4); margin-top: 5px; font-size: 0.75rem;">|</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="suggestion-card">📚 Estudar assunto</div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div style="text-align: center; color: rgba(212,175,55,0.4); margin-top: 5px; font-size: 0.75rem;">|</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="suggestion-card">💻 Programar</div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div style="text-align: center; color: rgba(212,175,55,0.4); margin-top: 5px; font-size: 0.75rem;">|</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="suggestion-card">📊 Analisar dados</div>', unsafe_allow_html=True)

    # 5. Saudação e "Como posso ajudar você hoje?" embaixo dos cards
    st.markdown(
        """
        <div style="text-align: center; margin-top: 16px; margin-bottom: 12px;">
            <h3 style="color: #ffffff; margin-bottom: 2px; font-weight: 700;">Olá 👋</h3>
            <p style="color: #94a3b8; font-size: 0.88rem;">Como posso ajudar você hoje?</p>
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
            messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}] + [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ]
            
            chat_completion = client.chat.completions.create(
                messages=messages_for_api,
                model="openai/gpt-oss-120b",
                temperature=0.7,
                max_tokens=2048,
                stream=True,
            )
            
            for chunk in chat_completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"Desculpe, ocorreu um erro ao processar sua solicitação: {e}"
            message_placeholder.markdown(full_response)
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
