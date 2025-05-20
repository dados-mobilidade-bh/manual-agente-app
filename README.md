
# 📱 Consulta de Infrações de Trânsito - BH

Este é um aplicativo desenvolvido com [Streamlit](https://streamlit.io/) para facilitar a **consulta de infrações e siglas de trânsito** pelos agentes municipais de Belo Horizonte. Ele substitui a necessidade de navegar por extensos manuais em PDF, permitindo uma **pesquisa rápida e intuitiva**, acessível diretamente pelo celular.

---

## 🚦 Funcionalidades

- **Tela inicial** com imagem de capa e botões de acesso.
- **Consulta de Siglas**: exibe uma tabela com as siglas e seus significados.
- **Consulta de Infrações**:
  - Campo de busca por palavra-chave no nome da infração.
  - Seleção de uma infração para exibir detalhes completos.
  - Botão para realizar nova consulta ou mudar para a tela de siglas.
- Interface adaptada para **uso em dispositivos móveis**.

---

## 🗂️ Estrutura do Projeto

```
📁 consulta-infracoes-bh
│
├── app.py                          # Código principal do Streamlit
├── manual_capa.png                # Imagem da capa do manual (tela inicial)
├── Exemplo_Infrações.xlsx         # Base de dados das infrações
├── Tabela_de_Siglas_e_Significados.csv  # Base de dados das siglas
├── requirements.txt               # Dependências do projeto
└── README.md                      # Este arquivo
```

---

## ▶️ Como executar localmente

1. Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/consulta-infracoes-bh.git
cd consulta-infracoes-bh
```

2. Instale as dependências (recomenda-se uso de ambiente virtual):

```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:

```bash
streamlit run app.py
```

---

## ☁️ Deploy no Streamlit Cloud

Você pode publicar o app gratuitamente em [https://streamlit.io/cloud](https://streamlit.io/cloud). Basta:

1. Criar um repositório público no GitHub com esses arquivos.
2. Acessar o Streamlit Cloud, clicar em **"New app"**, selecionar o repositório e definir o arquivo principal como `app.py`.

---

## 📷 Preview

![Capa do app](manual_capa.png)

---

## 👥 Desenvolvido por

Prefeitura de Belo Horizonte  
Superintendência de Mobilidade Urbana - SUMOB  
Gerência de Pesquisa e Ciência de Dados

---

## 📄 Licença

Este projeto é de uso interno e institucional. Para reutilização ou distribuição, entre em contato com os responsáveis pelo sistema.
