import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO STREAMLIT ---
st.set_page_config(page_title="Consulta de Infrações", layout="centered")

# --- CARREGAMENTO DE DADOS ---
df_siglas = pd.read_csv("Tabela_de_Siglas_e_Significados.csv", sep=",")
df_infracoes = pd.read_excel("Exemplo_Infrações.xlsx")

# --- FUNÇÕES ---
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
    palavra = st.text_input("🔍 Assunto da Infração", placeholder="Digite uma palavra relacionada a infração (ex: estacionar)")

    if palavra:
        resultados = df_infracoes[df_infracoes["Infração"].str.contains(palavra, case=False, na=False)]
        if not resultados.empty:
            opcao = st.selectbox("Selecione uma infração para visualizar os detalhes e clique em consultar", resultados["Infração"].tolist())
            if st.button("Consultar"):
                st.markdown("### Detalhes da Infração")
                linha = resultados[resultados["Infração"] == opcao].iloc[0]
                for col in resultados.columns:
                    st.markdown(f"**{col}:** {linha[col]}")
                st.markdown("---")
                if st.button("🔁 Realizar Nova Consulta"):
                    st.rerun()
        else:
            st.warning("Nenhuma infração encontrada com essa palavra.")

    if st.button("📘 Consultar Siglas"):
        st.session_state["tela"] = "siglas"
        st.rerun()

    if st.button("⬅ Voltar"):
        st.session_state["tela"] = "inicial"
        st.rerun()

# --- LÓGICA DE NAVEGAÇÃO ---
if "tela" not in st.session_state:
    st.session_state["tela"] = "inicial"

if st.session_state["tela"] == "inicial":
    mostrar_capa()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📘 CONSULTAR SIGLAS"):
            st.session_state["tela"] = "siglas"
            st.rerun()
    with col2:
        if st.button("🚨 CONSULTAR INFRAÇÕES"):
            st.session_state["tela"] = "infracoes"
            st.rerun()

    st.markdown("---")
    st.markdown("📄 [Clique aqui para baixar o Manual Completo](https://github.com/seu_usuario/seu_repositorio/raw/main/manual_completo.pdf)", unsafe_allow_html=True)

elif st.session_state["tela"] == "siglas":
    tela_siglas()

elif st.session_state["tela"] == "infracoes":
    tela_infracoes()
