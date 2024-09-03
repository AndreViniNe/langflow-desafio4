MAX_FILE_SIZE = 1 * 1024 * 1024 #1Mb

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from database_infos import DATABASE_HOST, DATABASE_PASSWORD, DATABASE_USERNAME

# password = os.environ["DATABASE_PASSWORD"]
# username = os.environ["DATABASE_USERNAME"]
# host = os.environ["DATABASE_HOST"]

#-----------DATABASE CONNECTION-----------
# conn = st.connection(
#     "local_db",
#     type="sql",
#     url="postgresql://postgres:123456@localhost:5432/langflow"
# )

@st.cache_resource
def get_connection():
    engine = create_engine(f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:5432/postgres")
    Session = sessionmaker(bind=engine)
    return Session()


nome_teste = st.text_input("Nome")
infos_teste = st.text_input("Infos")
processamento_teste = st.text_input("Tempo de processamento (yyyy-mm-dd HH:MM:SS)")
salvamento_teste = st.file_uploader("Salvamento (PDF)", type=["pdf"])

if st.button("Adicionar na tabela"):
    
    session = get_connection()

    try:
        processamento_teste_dt = datetime.strptime(processamento_teste, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        st.error("Formato de data e hora inválido. Use o formato: yyyy-mm-dd HH:MM:SS")
        st.stop()

    # Lê o PDF como bytes
    if salvamento_teste is not None:
        salvamento_teste_bin = salvamento_teste.read()
    else:
        salvamento_teste_bin = None

    try:
        # Cria a query de inserção usando SQLAlchemy e text()
        insert_query = text("""
            INSERT INTO langflow_desafio4 (nome_usuario, informacoes_filtro, ultimo_processamento, salvamento_pdf)
            VALUES (:nome_teste, :infos_teste, :processamento_teste, :salvamento_teste)
        """)

        # Executa a query com os parâmetros
        session.execute(insert_query, {
            "nome_teste": nome_teste,
            "infos_teste": infos_teste,
            "processamento_teste": processamento_teste_dt,
            "salvamento_teste": salvamento_teste_bin
        })

        # Confirma a transação
        session.commit()
        st.success("Dados inseridos com sucesso!")

    except Exception as e:
        session.rollback()  # Reverte a transação em caso de erro
        st.error(f"Erro ao inserir os dados: {e}")

    finally:
        session.close()


#-----------STREAMLIT PRINCIPAL PAGE-----------
st.markdown("## Estagio Delivery ")

def reset_file_uploader():
    st.session_state['uploaded_file'] = None

uploaded_file = st.file_uploader("Anexe seu currículo **aqui** (Limite de 5MB):", type=["png", "jpg", "pdf", "docx", "doc"])

if uploaded_file is not None:
    file_size = uploaded_file.size

    if file_size > MAX_FILE_SIZE:
        st.error(f"O arquivo é muito grande! O tamanho máximo permitido é {MAX_FILE_SIZE / (1024 * 1024)} MB.\nEscolha outro arquivo")
        reset_file_uploader()
    else:
        st.write("Nome do arquivo:", uploaded_file.name)

st.divider()

linkedin_url = st.text_input("**Insira o link do seu perfil do linkedin**", value="Link perfil...")


#-----------STREAMLIT SIDEBAR-----------
st.sidebar.markdown("### Seleção de filtros para procura das vagas no Linkedin: ")

st.sidebar.title("Data de postagem das vagas")
date = st.sidebar.selectbox(
    'Selecione uma opção',
    ('1 dia', '3 dias', '7 dias', '15 dias', '30 dias')
)

st.sidebar.divider()

st.sidebar.title("Modalidade de trabalho")
genre = st.sidebar.radio(
    "Modalidade",
    [":blue[Remoto]", "**Híbrido**", ":blue[Presencial]"],
    index=None,
    label_visibility="hidden"
)

st.sidebar.divider()
