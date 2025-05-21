import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# CONFIGURAÇÕES INICIAIS
st.set_page_config(page_title="Manual de Infrações", layout="centered")

# CARREGA CONFIGURAÇÃO DO LOGIN
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# LOGIN
name, authentication_status, username = authenticator.login("main", "Login")

# LOGIN INVÁLIDO
if authentication_status == False:
    st.error('Usuário ou senha incorretos')

# LOGIN EM ABERTO
elif authentication_status == None:
    st.image("manual_capa.png", use_container_width=True)
    st.warning('Por favor, insira suas credenciais')

# LOGIN BEM-SUCEDIDO
elif authentication_status:
    # DADOS
    df_siglas = pd.read_csv("Tabela_de_Siglas_e_Significados.csv", sep=",")
    df_infracoes = pd.read_excel("Exemplo_Infrações.xlsx")

    # FUNÇÕES
    def mostrar_capa():
        st.image("manual_capa.png", use_container_width=True)

    def tela_siglas():
        st.markdown("## Tabela de Siglas")
        st.dataframe(df_siglas, use_container_width=True)
        if st.button("⬅ Voltar"):
            st.session_state["tela"] = "inicial"
            st.rerun()

    def tela_infracoes():
        st.markdown("## Consulta de Infrações")
        palavra = st.text_input("🔍 Assunto da Infração", placeholder="Digite uma palavra (ex: celular)")

        if palavra:
            resultados = df_infracoes[df_infracoes["Infração"].str.contains(palavra, case=False, na=False)]
            if not resultados.empty:
                opcao = st.selectbox("Selecione uma infração", resultados["Infração"].tolist())
                if st.button("Consultar"):
                    st.markdown("### Detalhes da Infração")
                    linha = resultados[resultados["Infração"] == opcao].iloc[0]
                    for col in resultados.columns:
                        st.markdown(f"**{col}:** {linha[col]}")
                    if st.button("🔁 Realizar Nova Consulta"):
                        st.rerun()
            else:
                st.warning("Nenhuma infração encontrada.")

        if st.button("📘 Consultar Siglas"):
            st.session_state["tela"] = "siglas"
            st.rerun()

        if st.button("⬅ Voltar"):
            st.session_state["tela"] = "inicial"
            st.rerun()

    # INÍCIO DA INTERFACE
    authenticator.logout("Sair", "sidebar")
    st.sidebar.success(f"Bem-vindo, {name}!")

    if "tela" not in st.session_state:
        st.session_state["tela"] = "inicial"

    if st.session_state["tela"] == "inicial":
        mostrar_capa()
        st.markdown(f"### 👋 Bem-vindo, **{name}**!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📘 CONSULTAR SIGLAS"):
                st.session_state["tela"] = "siglas"
                st.rerun()
        with col2:
            if st.button("🚨 CONSULTAR INFRAÇÕES"):
                st.session_state["tela"] = "infracoes"
                st.rerun()

    elif st.session_state["tela"] == "siglas":
        tela_siglas()

    elif st.session_state["tela"] == "infracoes":
        tela_infracoes()
