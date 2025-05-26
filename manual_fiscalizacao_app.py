import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO STREAMLIT ---
st.set_page_config(page_title="Consulta de Infrações", layout="centered")

# --- CARREGAMENTO DE DADOS ---
df_siglas = pd.read_csv("Tabela_de_Siglas_e_Significados.csv", sep=";", encoding="latin-1")
df_infracoes = pd.read_csv("Descricao_Infracoes.csv", sep=";", encoding="latin-1")
df_conceitos = pd.read_csv("Tabela_de_Conceitos_e_Definicoes.csv",  sep=";", encoding="latin-1")

# --- FUNÇÕES ---
def mostrar_capa():
    st.image("manual_capa.png", use_container_width=True)

def tela_siglas():
    st.markdown("## Tabela de Siglas")
    st.dataframe(df_siglas, use_container_width=True)
    if st.button("⬅ Voltar"):
        st.session_state["tela"] = "inicial"
        st.rerun()

def tela_conceitos():
    st.markdown("## Tabela de Conceitos e Definições")
    st.dataframe(df_conceitos, use_container_width=True)
    if st.button("⬅ Voltar"):
        st.session_state["tela"] = "inicial"
        st.rerun()

def tela_infracoes():
    st.markdown("## Consulta de Infrações")

    # Entrada da palavra-chave
    palavra = st.text_input(
        "🔍 Assunto da Infração",
        placeholder="Digite uma palavra relacionada à infração (ex: estacionar)"
    )

    # Botão de busca
    if st.button("🔍 Buscar Infração"):
        st.session_state["palavra_busca"] = palavra
        st.session_state["buscar"] = True
        st.session_state["mostrar_detalhes"] = False
        st.rerun()

    # Executa busca se a flag estiver ativada
    if st.session_state.get("buscar") and st.session_state.get("palavra_busca"):
        palavra_busca = st.session_state["palavra_busca"]
        resultados = df_infracoes[df_infracoes["PALAVRAS_CHAVE"].str.contains(palavra_busca, case=False, na=False)]

        if not resultados.empty:
            # Exibe a lista de opções
            opcao = st.selectbox(
                "Selecione uma infração para visualizar os detalhes e clique em consultar",
                resultados["INFRACAO"].tolist()
            )
            st.session_state["resultados"] = resultados
            st.session_state["opcao_selecionada"] = opcao

            if st.button("Consultar"):
                st.session_state["mostrar_detalhes"] = True
                st.rerun()
        else:
            st.warning("Nenhuma infração encontrada com essa palavra.")
            st.session_state["buscar"] = False

    # Exibe os detalhes se solicitado
    if st.session_state.get("mostrar_detalhes"):
        resultados = st.session_state.get("resultados")
        opcao = st.session_state.get("opcao_selecionada")

        if resultados is not None and opcao is not None:
            linha = resultados[resultados["INFRACAO"] == opcao].iloc[0]
            st.markdown("### Detalhes da Infração")
            for col in resultados.columns:
                st.markdown(f"**{col}:** {linha[col]}")
            st.markdown("---")
            if st.button("🔁 Realizar Nova Consulta"):
                for chave in ["buscar", "palavra_busca", "mostrar_detalhes", "resultados", "opcao_selecionada"]:
                    st.session_state.pop(chave, None)
                st.rerun()

    if st.button("⬅ Voltar"):
        st.session_state["tela"] = "inicial"
        for chave in ["buscar", "palavra_busca", "mostrar_detalhes", "resultados", "opcao_selecionada"]:
            st.session_state.pop(chave, None)
        st.rerun()

# --- LÓGICA DE NAVEGAÇÃO ---
if "tela" not in st.session_state:
    st.session_state["tela"] = "inicial"

if st.session_state["tela"] == "inicial":
    mostrar_capa()
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("🚨 CONSULTAR INFRAÇÕES"):
            st.session_state["tela"] = "infracoes"
            st.rerun()

    with col2:
        if st.button("📘 CONSULTAR SIGLAS"):
            st.session_state["tela"] = "siglas"
            st.rerun()

    with col3:
        if st.button("📚 CONSULTAR CONCEITOS"):
            st.session_state["tela"] = "conceitos"
            st.rerun()

    st.markdown("---")
    st.markdown("📄 [Clique aqui para baixar o Manual Completo](https://drive.google.com/uc?export=download&id=1KeeASS6mdiHzDzk2gZwS2d7XTZbDk36m)", unsafe_allow_html=True)

elif st.session_state["tela"] == "siglas":
    tela_siglas()

elif st.session_state["tela"] == "infracoes":
    tela_infracoes()

elif st.session_state["tela"] == "conceitos":
    tela_conceitos()
