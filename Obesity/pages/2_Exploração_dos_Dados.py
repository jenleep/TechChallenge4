# importar as bibliotecas
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# carregar os dados
csv_path = "Obesity/Obesity.csv"
df = pd.read_csv(csv_path)


# paleta de cores para os níveis de obesidade
cores_obesidade = {
    'Abaixo do peso': '#F2D7A6',
    'Peso normal': '#EBC97A',
    'Sobrepeso Tipo I': '#C5C98A',
    'Sobrepeso Tipo II': '#91C4B8',
    'Obesidade Tipo I': '#6FAFC2',
    'Obesidade Tipo II': "#6391BD",
    'Obesidade Tipo III': "#415C85"
}


# traduzir as colunas para português - para usar na interface
colunas_pt = {
    'Gender': 'Gênero',
    'Age': 'Idade',
    'Height': 'Altura',
    'Weight': 'Peso',
    'family_history': 'Histórico Familiar',
    'FAVC': 'Consumo de Alimentos com Alta Caloria',
    'FCVC': 'Frequência de Consumo de Vegetais',
    'NCP': 'Número de Refeições por Dia',
    'CAEC': 'Comer Entre Refeições',
    'SMOKE': 'Fuma',
    'CH2O': 'Consumo de Água',
    'SCC': 'Calorias Diárias Consumidas',
    'FAF': 'Atividade Física',
    'TUE': 'Uso de Dispositivos Tecnológicos',
    'CALC': 'Consumo de Alcool',
    'MTRANS': 'Meio de Transporte',
    'Obesity': 'Obesidade'
}

df.rename(columns=colunas_pt, inplace=True)


# traduzir os valores categóricos para português
mapa_obesidade = {
    'Insufficient_Weight': 'Abaixo do peso',
    'Normal_Weight': 'Peso normal',
    'Overweight_Level_I': 'Sobrepeso Tipo I',
    'Overweight_Level_II': 'Sobrepeso Tipo II',
    'Obesity_Type_I': 'Obesidade Tipo I',
    'Obesity_Type_II': 'Obesidade Tipo II',
    'Obesity_Type_III': 'Obesidade Tipo III'
}

if 'Obesidade' in df.columns:
    df['Obesidade'] = df['Obesidade'].map(mapa_obesidade).fillna(df['Obesidade'])
    ordem_niveis = [
        'Abaixo do peso', 'Peso normal', 'Sobrepeso Tipo I', 'Sobrepeso Tipo II',
        'Obesidade Tipo I', 'Obesidade Tipo II', 'Obesidade Tipo III'
    ]
    df['Obesidade'] = pd.Categorical(df['Obesidade'], categories=ordem_niveis, ordered=True)

mapa_transporte = {
    'Automobile': 'Automóvel',
    'Bike': 'Bicicleta',
    'Motorbike': 'Motocicleta',
    'Public_Transportation': 'Transporte público',
    'Walking': 'Caminhar'
}

if 'Meio de Transporte' in df.columns:
    df['Meio de Transporte'] = df['Meio de Transporte'].map(mapa_transporte).fillna(df['Meio de Transporte'])

mapa_frequencia = {
    'Always': 'Sempre',
    'Frequently': 'Frequentemente',
    'Sometimes': 'As vezes',
    'no': 'Nunca'
}

for coluna in ['Comer Entre Refeições', 'Consumo de Alcool']:
    if coluna in df.columns:
        df[coluna] = df[coluna].map(mapa_frequencia).fillna(df[coluna])

mapa_sim_nao = {'yes': 'Sim', 'no': 'Não'}
for coluna in ['Histórico Familiar', 'Consumo de Alimentos com Alta Caloria', 'Fuma', 'Calorias Diárias Consumidas']:
    if coluna in df.columns:
        df[coluna] = df[coluna].map(mapa_sim_nao).fillna(df[coluna])

mapa_genero = {'Male': 'Masculino', 'Female': 'Feminino'}
df['Gênero'] = df['Gênero'].map(mapa_genero).fillna(df['Gênero'])


# interface do Streamlit
st.title("Explorador de dados sobre obesidade")
def texto(text):
    st.markdown(f"""
        <p style='text-align: justify; font-size: 18px; max-width: 900px; margin: auto;'>
            {text}
        </p>
    """, unsafe_allow_html=True)


texto('A maioria dos participantes é jovem, com idade média de 24,3 anos, o que pode influenciar a generalização do modelo para faixas etárias mais elevadas. A altura média é de 1,70 metros, com baixa variabilidade, enquanto o peso apresenta ampla dispersão, indicando perfis corporais bastante distintos. A distribuição das classes de obesidade é equilibrada.')
st.markdown('---')
colunas = [c for c in colunas_pt.values() if c.lower() != 'obesidade']
coluna = st.selectbox("Escolha uma coluna para filtrar", colunas)

explicacoes = {
    'Gênero': 'Identifica o gênero do participante (Feminino ou Masculino).',
    'Idade': 'Idade do participante em anos completos.',
    'Altura': 'Altura do participante em metros (m).',
    'Peso': 'Peso corporal do participante em quilogramas (kg).',
    'Histórico Familiar': 'Indica se há histórico familiar de obesidade.',
    'Consumo de Alimentos com Alta Caloria': 'Se consome alimentos altamente calóricos com frequência.',
    'Frequência de Consumo de Vegetais': 'Se há o costume de comer vegetais nas refeições.',
    'Número de Refeições por Dia': 'Quantidade média de refeições realizadas diariamente.',
    'Comer Entre Refeições': 'Frequência com que o participante realiza lanches entre as refeições principais.',
    'Fuma': 'Indica se o participante é fumante ou não.',
    'Consumo de Água': 'Quantidade média de água ingerida por dia (em litros).',
    'Calorias Diárias Consumidas': 'Informa se o participante monitora a ingestão diária de calorias.',
    'Atividade Física': 'Frequência semanal de prática de atividades físicas.',
    'Uso de Dispositivos Tecnológicos': 'Tempo médio de uso diário de dispositivos eletrônicos (celular, TV, computador e outros).',
    'Consumo de Alcool': 'Frequência de consumo de bebidas alcoólicas.',
    'Meio de Transporte': 'Principal meio de transporte utilizado no dia a dia (ex: carro, bicicleta, caminhada).',
    'Obesidade': 'Classificação do nível de obesidade com base em aspectos que vão além de peso e altura.'
}

st.info(explicacoes[coluna])


# filtragem dos dados
unique_vals = df[coluna].unique()

if np.issubdtype(df[coluna].dtype, np.number) and len(unique_vals) > 8:
    valor_min, valor_max = df[coluna].min(), df[coluna].max()
    amplitude = valor_max - valor_min

    if amplitude < 0.01:
        st.warning(f"A coluna '{coluna}' possui pouca variação ({valor_min:.2f}–{valor_max:.2f}). Mostrando todos os dados.")
        filtered_df = df.copy()
    else:
        bins = np.unique(np.linspace(valor_min, valor_max, 5))
        labels = [f"{bins[i]:.2f}–{bins[i+1]:.2f}" for i in range(len(bins)-1)]
        df["faixa_temp"] = pd.cut(df[coluna], bins=bins, labels=labels)
        options = ["Mostrar todos"] + labels
        choice = st.selectbox(f"Escolha uma faixa para '{coluna}'", options, index=1)
        filtered_df = df.copy() if choice == "Mostrar todos" else df[df["faixa_temp"] == choice]
        df.drop(columns="faixa_temp", inplace=True)
else:
    options = ["Mostrar todos"] + sorted(map(str, unique_vals))
    choice = st.selectbox(f"Escolha um valor para '{coluna}'", options, index=1)
    filtered_df = df if choice == "Mostrar todos" else df[df[coluna].astype(str) == choice]


# gráfico de barras
if 'Obesidade' in df.columns:
    st.plotly_chart(
        px.bar(
            filtered_df,
            x='Obesidade',
            title=f"Distribuição de Obesidade para {coluna} = {choice}",
            color='Obesidade',
            category_orders={'Obesidade': ordem_niveis},
            color_discrete_map=cores_obesidade  
        ),
        use_container_width=True
    )


# scatter plot altura x peso
if {'Altura', 'Peso'}.issubset(df.columns):
    st.plotly_chart(
        px.scatter(
            filtered_df,
            x='Altura', y='Peso',
            color='Obesidade',
            title=f"Altura x Peso para {coluna} = {choice}",
            opacity=0.7,
            category_orders={'Obesidade': ordem_niveis},
            color_discrete_map=cores_obesidade  # ✅ aplica a paleta
        ),
        use_container_width=True
    )


# histograma da coluna selecionada
if np.issubdtype(df[coluna].dtype, np.number):
    st.plotly_chart(
        px.histogram(
            filtered_df,
            x=coluna,
            nbins=20,
            title=f"Distribuição de {coluna} ({choice})",
            color='Obesidade' if 'Obesidade' in df.columns else None,
            color_discrete_map=cores_obesidade if 'Obesidade' in df.columns else None,  # ✅ aplica a paleta
            marginal="box"
        ),
        use_container_width=True
    )


# resumo da seleção
categoria_obesidade_mais_comum = filtered_df['Obesidade'].mode()[0] if 'Obesidade' in filtered_df.columns else "N/A"
peso_medio = filtered_df['Peso'].mean() if 'Peso' in filtered_df.columns else 0
altura_media = filtered_df['Altura'].mean() if 'Altura' in filtered_df.columns else 0
total_registros = len(filtered_df)

descricao_md = f"""
**Resumo da seleção:** `{coluna} = {choice}`  

- **Total de registros:** {total_registros}  
- **Peso médio:** {peso_medio:.1f} kg  
- **Altura média:** {altura_media:.2f} m  
- **Categoria de obesidade mais comum:** {categoria_obesidade_mais_comum}  
"""

st.markdown(descricao_md)


