import streamlit as st
import pandas as pd
import unidecode

st.set_page_config(page_title="ChatLid - Lideranças na Câmara", layout="wide")
st.image("https://www.consilliumrig.com.br/wp-content/uploads/2022/07/02_Logotipo_Consillium-1024x218.png", width=300)
st.title("🔍 ChatLid - Lideranças na Câmara dos Deputados")

@st.cache_data
def carregar_dados():
    df = pd.read_excel("Lideres_CD.xlsx")
    df.columns = df.columns.str.strip().str.title()
    df["Nome Parlamentar"] = df["Nome Parlamentar"].astype(str).str.strip()
    df["Partido"] = df["Partido"].astype(str).str.strip()
    df["Representação"] = df["Representação"].astype(str).str.strip()
    return df

df = carregar_dados()

dados_complementares = {
    "Adolfo Viana": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204560.jpg", "perfil": "https://www.camara.leg.br/deputados/204560"},
    "Antonio Brito": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/160553.jpg", "perfil": "https://www.camara.leg.br/deputados/160553"},
    "Aureo Ribeiro": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/160512.jpg", "perfil": "https://www.camara.leg.br/deputados/160512"},
    "Doutor Luizinho": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204450.jpg", "perfil": "https://www.camara.leg.br/deputados/204450"},
    "Fred Costa": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204494.jpg", "perfil": "https://www.camara.leg.br/deputados/204494"},
    "Gilberto Abramo": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204491.jpg", "perfil": "https://www.camara.leg.br/deputados/204491"},
    "Isnaldo Bulhões Jr.": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204436.jpg", "perfil": "https://www.camara.leg.br/deputados/204436"},
    "Lindbergh Farias": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/74858.jpg", "perfil": "https://www.camara.leg.br/deputados/74858"},
    "Luis Tibé": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/160510.jpg", "perfil": "https://www.camara.leg.br/deputados/160510"},
    "Marcel van Hattem": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/156190.jpg", "perfil": "https://www.camara.leg.br/deputados/156190"},
    "Mário Heringer": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/74158.jpg", "perfil": "https://www.camara.leg.br/deputados/74158"},
    "Neto Carletto": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/220703.jpg", "perfil": "https://www.camara.leg.br/deputados/220703"},
    "Pedro Campos": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/220667.jpg", "perfil": "https://www.camara.leg.br/deputados/220667"},
    "Pedro Lucas Fernandes": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/122974.jpg", "perfil": "https://www.camara.leg.br/deputados/122974"},
    "Rodrigo Gambale": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/220641.jpg", "perfil": "https://www.camara.leg.br/deputados/220641"},
    "Sóstenes Cavalcante": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/178947.jpg", "perfil": "https://www.camara.leg.br/deputados/178947"},
    "Talíria Petrone": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204464.jpg", "perfil": "https://www.camara.leg.br/deputados/204464"},
    "José Guimarães": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/141470.jpg", "perfil": "https://www.camara.leg.br/deputados/141470"},
    "Arlindo Chinaglia": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/73433.jpg", "perfil": "https://www.camara.leg.br/deputados/73433"},
    "Caroline de Toni": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204369.jpg", "perfil": "https://www.camara.leg.br/deputados/204369"},
    "Zucco": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/220552.jpg", "perfil": "https://www.camara.leg.br/deputados/220552"}
}

titulos_especiais = {
    "governo": "José Guimarães",
    "maioria": "Arlindo Chinaglia",
    "minoria": "Caroline de Toni",
    "oposição": "Zucco",
    "oposicao": "Zucco"
}

pergunta = st.text_input("Pesquise por partido, bloco ou parlamentar:")

if pergunta:
    pergunta_lower = unidecode.unidecode(pergunta.lower())
    encontrados = []

    # Busca por título especial
    for titulo, nome in titulos_especiais.items():
        if titulo in pergunta_lower:
            encontrados.append(nome)

    # Busca por nome do parlamentar
    for nome in df["Nome Parlamentar"]:
        if unidecode.unidecode(nome.lower()) in pergunta_lower:
            encontrados.append(nome)

    # Busca por partido ou representação
    por_partido = df[df["Partido"].apply(lambda x: unidecode.unidecode(x.lower()) in pergunta_lower)]
    por_representacao = df[df["Representação"].apply(lambda x: unidecode.unidecode(x.lower()) in pergunta_lower)]

    resultados = df[df["Nome Parlamentar"].isin(encontrados)]

    if resultados.empty:
        resultados = pd.concat([por_partido, por_representacao]).drop_duplicates()

    if not resultados.empty:
        for _, row in resultados.iterrows():
            col1, col2 = st.columns([1, 5])
            nome = row["Nome Parlamentar"]
            representacao = row["Representação"]
            info = dados_complementares.get(nome, {})
            foto = info.get("foto", "")
            link = info.get("perfil", "#")

            with col1:
                if foto:
                    st.image(foto, width=80)
                if representacao:
                    st.markdown(f"**Líder {representacao} na Câmara**")

            with col2:
                st.markdown(f"### [{nome}]({link})")
                st.markdown(f"**Partido:** {row['Partido']} | **UF:** {row['Uf']}")
                st.markdown(f"**Email:** [{row['Correio Eletrônico']}]({row['Correio Eletrônico']})")
                st.markdown(f"**Telefone:** {row['Telefone']}")

                tabela_end = pd.DataFrame({
                    "Endereço da Liderança": [row.get("Endereço Liderança", "-")],
                    "Endereço do Gabinete": [row.get("Endereço Gabinete", "-")]
                })
                st.markdown("**Endereços:**")
                st.table(tabela_end)
    else:
        st.warning("Nenhum líder encontrado com base na sua pergunta.")
