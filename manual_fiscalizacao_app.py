import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO STREAMLIT ---
st.set_page_config(page_title="Consulta de Infrações", layout="centered")

# --- CARREGAMENTO DE DADOS ---
df_siglas = pd.read_csv("Tabela_de_Siglas_e_Significados.csv", sep=";", encoding="latin-1")
df_infracoes = pd.read_csv("Detalhamento_Infracoes.csv", sep=";", encoding="latin-1")
df_conceitos = pd.read_csv("Tabela_de_Conceitos_e_Definicoes.csv",  sep=";", encoding="latin-1")


principais_codigos = [
    "520-70", "521-51", "521-52",
    "522-31", "522-32", "523-11",
    "523-12", "524-00"
]

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

    # Entrada da busca (pode ser código ou palavra)
    termo_busca = st.text_input(
        "🔍 Assunto da Infração ou Código",
        placeholder="Digite uma palavra ou código (ex: aclive ou 592-41)"
    )

    if st.button("🔍 Buscar Infração"):
        st.session_state["palavra_busca"] = termo_busca.strip()
        st.session_state["buscar"] = True
        st.session_state["mostrar_detalhes"] = False
        st.rerun()

    if st.session_state.get("buscar") and st.session_state.get("palavra_busca"):
        termo = st.session_state["palavra_busca"]

        # Filtro por código exato ou por palavra-chave
        resultados = df_infracoes[
            (df_infracoes["CÓDIGO"].astype(str).str.lower() == termo.lower()) |
            (df_infracoes["PALAVRAS_CHAVE"].str.contains(termo, case=False, na=False))
        ]

        if not resultados.empty:
            # Cria coluna de exibição "CÓDIGO - INFRAÇÃO"
            resultados["OPCAO_FORMATADA"] = resultados["CÓDIGO"].astype(str) + " - " + resultados["INFRACAO"]

            # Exibe selectbox com a descrição formatada
            opcao_formatada = st.selectbox(
                "Selecione uma infração para visualizar os detalhes e clique em consultar",
                resultados["OPCAO_FORMATADA"].tolist()
            )

            # Recupera a infração original
            opcao = resultados[resultados["OPCAO_FORMATADA"] == opcao_formatada]["INFRACAO"].values[0]

            st.session_state["resultados"] = resultados
            st.session_state["opcao_selecionada"] = opcao

            if st.button("Consultar"):
                st.session_state["mostrar_detalhes"] = True
                st.rerun()
        else:
            st.warning("Nenhuma infração encontrada com esse termo.")
            st.session_state["buscar"] = False

    if st.session_state.get("mostrar_detalhes"):
        resultados = st.session_state.get("resultados")
        opcao = st.session_state.get("opcao_selecionada")

        if resultados is not None and opcao is not None:
            linha = resultados[resultados["INFRACAO"] == opcao].iloc[0]
            st.markdown("### Detalhes da Infração")

            labels = {
                "CÓDIGO": "Código",
                "INFRACAO": "Infração",
                "AMPARO_LEGAL": "Amparo Legal",
                "PROCEDIMENTO": "Procedimento",
                "TIPO_INFRACAO": "Tipo de Infração",
                "PONTUACAO": "Pontuação",
                "INFRATOR": "Infrator"
            }

            for col in resultados.columns:
                if col not in ["PALAVRAS_CHAVE", "OPCAO_FORMATADA"]:
                    nome_exibicao = labels.get(col, col.replace("_", " ").title())
                    st.markdown(f"**{nome_exibicao}:** {linha[col]}")

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

    # Lista de principais códigos
    principais_codigos = [
        "520-70", "521-51", "521-52",
        "522-31", "522-32", "523-11",
        "523-12", "524-00"
    ]

    # Filtra as principais infrações
    principais = df_infracoes[df_infracoes["CÓDIGO"].astype(str).isin(principais_codigos)].copy()
    principais["OPCAO"] = principais["CÓDIGO"].astype(str) + " - " + principais["INFRACAO"]

    st.markdown("---")
    st.markdown("## 🚦 Principais Infrações")

    opcao_principal = st.selectbox(
        "Clique em uma infração para visualizar o detalhamento:",
        principais["OPCAO"].tolist(),
        key="select_principal"
    )

    if st.button("🔍 Ver Detalhes", key="botao_principal"):
        codigo_escolhido = principais[principais["OPCAO"] == opcao_principal]["CÓDIGO"].values[0]

        # Simula uma busca direta por código
        st.session_state["palavra_busca"] = str(codigo_escolhido)
        st.session_state["buscar"] = True
        st.session_state["mostrar_detalhes"] = False
        st.session_state["tela"] = "infracoes"
        st.rerun()

    # Botão para download do manual
    st.markdown("---")
    st.markdown("📄 [Clique aqui para baixar o Manual Completo](https://drive.google.com/uc?export=download&id=1KeeASS6mdiHzDzk2gZwS2d7XTZbDk36m)", unsafe_allow_html=True)

elif st.session_state["tela"] == "siglas":
    tela_siglas()

elif st.session_state["tela"] == "infracoes":
    tela_infracoes()

elif st.session_state["tela"] == "conceitos":
    tela_conceitos()



# # --- LÓGICA DE NAVEGAÇÃO ---
# if "tela" not in st.session_state:
#     st.session_state["tela"] = "inicial"

# if st.session_state["tela"] == "inicial":
#     mostrar_capa()
#     col1, col2, col3 = st.columns([1, 1, 1])

#     with col1:
#         if st.button("🚨 CONSULTAR INFRAÇÕES"):
#             st.session_state["tela"] = "infracoes"
#             st.rerun()

#     with col2:
#         if st.button("📘 CONSULTAR SIGLAS"):
#             st.session_state["tela"] = "siglas"
#             st.rerun()

#     with col3:
#         if st.button("📚 CONSULTAR CONCEITOS"):
#             st.session_state["tela"] = "conceitos"
#             st.rerun()

#     st.markdown("---")
#     st.markdown("📄 [Clique aqui para baixar o Manual Completo](https://drive.google.com/uc?export=download&id=1KeeASS6mdiHzDzk2gZwS2d7XTZbDk36m)", unsafe_allow_html=True)

# elif st.session_state["tela"] == "siglas":
#     tela_siglas()

# elif st.session_state["tela"] == "infracoes":
#     tela_infracoes()

# elif st.session_state["tela"] == "conceitos":
#     tela_conceitos()
