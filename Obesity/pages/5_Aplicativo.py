"""Streamlit app for predicting obesity level using a trained pipeline.

The app collects a reduced set of features, loads a pre-trained pipeline
(`pipeline_subset.pkl`) and shows a prediction.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import json
from obesity_pipeline import ObesityPipeline
from data_loader import MTRANS_MAP
import pickle

# Load dataset (used for examples / plots)
DATA_CSV = 'Obesity/Obesity.csv'
df = pd.read_csv(DATA_CSV)

# Pipeline feature configuration (must match the training script)
col_ordinais = ['CAEC', 'CALC']
ordem_ordinais = {
    'CAEC': ['no', 'Sometimes', 'Frequently', 'Always'],
    'CALC': ['no', 'Sometimes', 'Frequently', 'Always']
}
col_nominais = ['FAVC', 'SCC', 'MTRANS', 'family_history']
col_numericas = ['Age', 'Height', 'Weight', 'FCVC', 'FAF', 'CH2O', 'TUE']

# Create and load pipeline (show friendly message if missing)
pipeline_obj = ObesityPipeline(col_ordinais, ordem_ordinais, col_nominais, col_numericas)
try:
    pipeline_obj.carregar('Obesity/pipeline_obesidade_pickle.pkl')
except Exception as e:
    st.warning(f"Não foi possível carregar o pipeline salvo: {e}")


st.header("Classificador de Obesidade")
st.markdown("Preencha os dados abaixo para obter o nível de obesidade:")

col1, col2 = st.columns(2)

with col1:
    idade = st.number_input("Idade", 10, 80, 25)
    altura = st.number_input("Altura (m)", 1.0, 2.5, 1.7, format="%.2f")
    peso = st.number_input("Peso (kg)", 20.0, 250.0, 70.0, format="%.1f")
    historico_familiar = st.radio("Tem histórico familiar de obesidade?", ["Sim", "Não"])  # FAFM
    atividade_fisica = st.slider("Frequência de atividade física (0 a 3)", 0, 3, 1)  # FAF
    dispositivos_tecnologicos = st.slider("Uso de dispositivos tecnológicos (0 a 2)", 0, 2, 1)  # TUE
    meio_transporte = st.selectbox("Meio de transporte principal", ["Carro", "Moto", "Bicicleta", "Transporte público", "Caminhar"])  # MTRANS

with col2:
    agua = st.slider("Consumo de água (litros por dia, 1 a 5)", 1.0, 5.0, 2.0, format="%.1f")  # CH2O
    vegetais = st.slider("Frequência de consumo de vegetais (1 a 3)", 1, 3, 2)  # FCVC
    alimentos_caloricos = st.radio("Consome alimentos calóricos com frequência?", ["Sim", "Não"])  # FAVC
    monitora_calorias = st.radio("Monitora as calorias que consome?", ["Sim", "Não"])  # SCC
    entre_refeicoes = st.radio("Come entre as refeições?", ["Nunca", "As vezes", "Frequentemente", "Sempre"])  # CAEC
    alcool = st.radio("Com qual frequência faz uso de álcool", ["Nunca", "As vezes", "Frequentemente", "Sempre"])  # CALC


# Montar DataFrame de entrada
# Map user inputs to the CSV column names expected by the subset pipeline
dados_usuario = pd.DataFrame([{
    'Age': idade,
    'Height': altura,
    'Weight': peso,
    'family_history': historico_familiar,

    'CH2O': float(agua),
    'FCVC': vegetais,
    'FAVC': alimentos_caloricos,
    'SCC': monitora_calorias,
    'CAEC': entre_refeicoes,
    'CALC': alcool,

    'FAF': float(atividade_fisica),
    'TUE': float(dispositivos_tecnologicos),
    'MTRANS': meio_transporte
}])

dados_usuario['CAEC'] = dados_usuario['CAEC'].replace({
    'Nunca': 'no', 'As vezes': 'Sometimes', 'Frequentemente': 'Frequently', 'Sempre': 'Always'
})

dados_usuario['CALC'] = dados_usuario['CALC'].replace({
    'Nunca': 'no', 'As vezes': 'Sometimes', 'Frequentemente': 'Frequently', 'Sempre': 'Always'
})

dados_usuario['family_history'] = dados_usuario['family_history'].replace({
    'Não': 'no', 'Sim': 'yes'
})

dados_usuario['FAVC'] = dados_usuario['FAVC'].replace({
    'Não': 'no', 'Sim': 'yes'
})

dados_usuario['SCC'] = dados_usuario['SCC'].replace({
    'Não': 'no', 'Sim': 'yes'
})

dados_usuario['MTRANS'] = dados_usuario['MTRANS'].replace(MTRANS_MAP)
    
# Traduções: ajuste as chaves para os rótulos do seu modelo
TRANSLATIONS = {
    "Insufficient_Weight": "Abaixo do Peso",
    "Normal_Weight": "Peso Normal",
    "Overweight_Level_I": "Sobrepeso (Nível I)",
    "Overweight_Level_II": "Sobrepeso (Nível II)",
    "Obesity_Type_I": "Obesidade (Tipo I)",
    "Obesity_Type_II": "Obesidade (Tipo II)",
    "Obesity_Type_III": "Obesidade (Tipo III)",
}

EXPLANATIONS = {
    "Insufficient_Weight": "Abaixo do peso ideal; pode indicar risco nutricional ou metabólico.",
    "Normal_Weight": "Faixa de peso considerada saudável segundo índice padrão; não é diagnóstico médico.",
    "Overweight_Level_I": "Acima do peso ideal; recomenda-se avaliar hábitos e procurar orientação.",
    "Overweight_Level_II": "Excesso de peso mais acentuado; atenção a sinais de risco à saúde.",
    "Obesity_Type_I": "Obesidade leve; importante buscar acompanhamento profissional.",
    "Obesity_Type_II": "Obesidade moderada; maior risco de doenças associadas ao excesso de peso.",
    "Obesity_Type_III": "Obesidade grave; requer intervenção médica e mudanças no estilo de vida."
}

if st.button("Classificar"):
    with st.spinner("Avaliando..."):
        try:            
            bmi = peso / (altura ** 2) if altura > 0 else None
            
            # prever() já retorna um array-like de rótulos
            pred = pipeline_obj.prever(dados_usuario)
            label = pred[0]
            if bmi is not None and bmi < 18.3:
                label = "Insufficient_Weight"
            
            # tradução
            translated = TRANSLATIONS.get(label, label)
            
            st.markdown("""
            <style>
                .stAlert .st-bb {
                    background-color: #EBC97A;
                }
                .stAlert .st-at {
                    color: #EBC97A;
                }
            </style>
            """, unsafe_allow_html=True)
            
            st.success(f"Nível de obesidade previsto: **{translated}**")

            # explicação adicional, se existir
            expl = EXPLANATIONS.get(label)
            if expl:
                st.info(expl)

        except Exception as e:
            st.error(f"Erro ao obter previsão: {e}")





