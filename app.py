import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# 1. Configuração da Página
st.set_page_config(page_title="VoxLead AI - Simulador", layout="wide")
st.title("🎙️ VoxLead AI Engine - SDR Simulator")

# 2. Captura segura da API Key
groq_api_key = os.getenv("GROQ_API_KEY")

# 3. Inicialização do Estado (Simulando o Banco de Dados)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lead_status" not in st.session_state:
    st.session_state.lead_status = "NEW"

# 4. Barra Lateral: Personalização (Sem o campo de API Key)
with st.sidebar:
    st.header("⚙️ Configurações do Motor")
    
    st.subheader("Engenharia de Prompt")
    system_prompt = st.text_area(
        "Instruções da Persona", 
        value="Você é uma assistente executiva sênior de pré-vendas. Seu objetivo é confirmar interesse, identificar orçamento e agendar reunião de forma concisa. Máximo 2 frases por resposta.",
        height=200
    )
    
    st.subheader("Estado Atual do Lead")
    st.info(f"Status: {st.session_state.lead_status}")

# 5. Validação de Segurança
if not groq_api_key:
    st.error("⚠️ Chave da API do Groq não encontrada! Verifique se o arquivo .env está configurado corretamente com a variável GROQ_API_KEY.")
    st.stop()

# 6. Interface de Chat Principal
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Simule a resposta do lead aqui..."):
    st.session_state.lead_status = "IN_CONVERSATION"
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # 7. Comunicação com Groq
    try:
        client = Groq(api_key=groq_api_key)
        
        # Construindo o histórico de mensagens com a persona configurável
        messages_to_send = [{"role": "system", "content": system_prompt}] + st.session_state.messages
        
        with st.spinner("Analisando intenção e gerando resposta..."):
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant", # Modelo atualizado
                messages=messages_to_send,
                temperature=0.3, 
            )
            
            response = completion.choices[0].message.content
            
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        with st.chat_message("assistant"):
            st.markdown(response)
            
    except Exception as e:
        st.error(f"Erro de processamento: {e}")