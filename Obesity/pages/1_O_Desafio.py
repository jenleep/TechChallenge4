import streamlit as st

def texto(text):
    st.markdown(f"""
        <p style='text-align: justify; font-size: 18px; max-width: 900px; margin: auto;'>
            {text}
        </p>
    """, unsafe_allow_html=True)

st.title("Projeto de Previsão de Obesidade")

# Cria duas colunas e coloca em cada uma o subtítulo e o texto correspondente
col1, gap, col2 = st.columns([0.6, 0.06, 1.4])

with col1:
    st.subheader("Objetivo")
    texto("Desenvolver um modelo de machine learning para auxiliar médicas e médicos a preverem o nível de obesidade de uma pessoa.")

with col2:
    st.subheader("Entregáveis do Projeto")
    texto("- Pipeline do modelo de machine learning;")
    texto("- Assertividade do modelo > 75%;")
    texto("- Deploy do modelo em uma aplicação preditiva utilizando Streamlit;")
    texto("- Visão analítica em um painel com principais insights obtidos;")

st.markdown("---")


with st.expander("Por que não usar apenas o IMC?"):
    st.markdown("""
    O IMC ignora aspectos importantes como:
    - Hábitos alimentares
    - Nível de atividade física
    - Consumo de água
    - Histórico familiar de excesso de peso

    Além disso, não distingue entre massa muscular e gordura corporal. Um modelo de ML permite uma análise mais individualizada e precisa.
    """)

with st.expander("Importância da classificação"):
    st.markdown("""
    Classificar o nível de obesidade permite:
    - Prever riscos de saúde como diabetes tipo 2, doenças cardiovasculares e câncer
    - Guiar escolhas mais saudáveis e estratégias de controle de peso
    - Criar planos personalizados de acompanhamento clínico
    """)
