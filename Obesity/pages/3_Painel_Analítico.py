import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from data_loader import load_data

st.set_page_config(page_title="Análise de Obesidade", layout="wide")
st.title('Perfil e Comportamentos Relacionados à Obesidade')

# Load cleaned data
df, df_num, ordem_niveis, ordem_nives_num, cores_obesidade, cores_obesidade_num, cores_obesidade_num_ajustada = load_data()

# ------------------------------------------------------------
# FUNÇÕES
# ------------------------------------------------------------

def texto(text):
    st.markdown(f"""
        <p style='text-align: justify; font-size: 18px; max-width: 900px; margin: auto;'>
            {text}
        </p>
    """, unsafe_allow_html=True)

def grafico_box(x, y, titulo, key):
    # protege caso a categoria não exista no mapeamento
    cmap = cores_obesidade if x == "Nivel de Obesidade" else None
    fig = px.box(df, x=x, y=y, color=x,
                 category_orders={x: ordem_niveis} if x == "Nivel de Obesidade" else None,
                 color_discrete_map=cmap, title=titulo)
    st.plotly_chart(fig, key=key)

def scatter():
    fig = px.scatter(df, x="Idade", y="Peso", color="Nivel de Obesidade",
                     trendline="ols", category_orders={"Nivel de Obesidade": ordem_niveis},
                     color_discrete_map=cores_obesidade, title="Relação entre Idade e Peso")
    st.plotly_chart(fig, key="scatter")

def box_peso():
    fig = go.Figure()
    for cat in ordem_niveis:
        # usa .get para evitar KeyError se houver categoria inesperada
        color = cores_obesidade.get(cat, '#CCCCCC')
        fig.add_trace(go.Box(
            y=df[df['Nivel de Obesidade'] == cat]['Peso'], name=cat,
            boxpoints='suspectedoutliers', marker_color=color, width=0.4
        ))
    fig.update_layout(title="Distribuição do Peso por Nível de Obesidade", yaxis_title="Peso")
    st.plotly_chart(fig, key="peso_box")

def barras_empilhadas(variavel, df=df):
    # Garante que variavel existe e é válida
    if variavel not in df_num.columns or 'Nivel de Obesidade' not in df_num.columns:
        st.warning(f"Coluna '{variavel}' ou 'Nivel de Obesidade' não encontrada.")
        return
    pass

    df_prop_label = df.groupby(["Nivel de Obesidade", variavel]).size().reset_index(name="Contagem")
    df_total_label = df.groupby("Nivel de Obesidade").size().reset_index(name="Total")
    df_prop_label = df_prop_label.merge(df_total_label, on="Nivel de Obesidade")
    
    df_prop = df_num.groupby(["Nivel de Obesidade", variavel]).size().reset_index(name="Contagem")
    df_total = df_num.groupby("Nivel de Obesidade").size().reset_index(name="Total")
    df_prop = df_prop.merge(df_total, on="Nivel de Obesidade")
    
    df_prop_label["Proporção (%)"] = (df_prop["Contagem"] / df_prop["Total"]) * 100
    df_prop_label[variavel] = df_prop[variavel].astype(int)

    df_prop["Proporção (%)"] = (df_prop["Contagem"] / df_prop["Total"]) * 100
    df_prop[variavel] = df_prop[variavel].astype(int)

    # Cria rótulo de grupo para cor
    df_prop["grupo_cor"] = df_prop_label.apply(
        lambda r: f"Sim - {r['Nivel de Obesidade']}" if r[variavel] == 1 else "Não", axis=1
    )
    df_prop_label["grupo_cor"] = df_prop_label.apply(
        lambda r: f"Sim - {r['Nivel de Obesidade']}" if r[variavel] == 1 else "Não", axis=1
    )
    # Constrói mapeamento de cores consistente: "Não" + "Sim - <Nivel>"
    # usa o mapa numérico ajustado (com chaves textuais) para manter a paleta que você tinha
    cores_personalizadas = {"Não": "#D2E7F1"}
      
    # Ajusta o mapa numérico para usar as mesmas chaves textuais que 'Nivel de Obesidade'
    # (assim podemos usar o map numérico sem causar TypeError no Plotly)
    cores_obesidade_num_ajustada = dict(zip(ordem_niveis, cores_obesidade_num.values()))
  
    # adiciona as chaves "Sim - <Nivel>" usando cores_obesidade_num_ajustada
    for nivel, color in cores_obesidade_num_ajustada.items():
        cores_personalizadas[f"Sim - {nivel}"] = color

    # Plota
    fig = px.bar(
        df_prop,
        x="Nivel de Obesidade",
        y="Proporção (%)",
        color="grupo_cor",
        color_discrete_map=cores_personalizadas,
        barmode="stack",
        text=df_prop["Proporção (%)"].round(1).astype(str) + '%',
        title=f"'{variavel}' por Nível de Obesidade"
    )
    fig.update_traces(textposition="inside")
    st.plotly_chart(fig, key=f"stack_{variavel}")

def medias(df_num, variaveis):
    col1, col2 = st.columns(2)
    for i, v in enumerate(variaveis):
        df_media = df_num.groupby("Nivel de Obesidade")[v].mean().reset_index()

        # Força strings limpas e filtra apenas categorias conhecidas
        df_media["Nivel de Obesidade"] = df_media["Nivel de Obesidade"].astype(str).str.strip()
        df_media = df_media[df_media["Nivel de Obesidade"].isin(cores_obesidade.keys())]

        # Gráfico principal com mapa nominal (cores_obesidade)
        fig = px.bar(
            df_media,
            x="Nivel de Obesidade",
            y=v,
            color="Nivel de Obesidade",
            category_orders={"Nivel de Obesidade": ordem_niveis},
            color_discrete_map=cores_obesidade_num
        )
        fig.add_hline(
            y=df_media[v].mean() if not df_media[v].isna().all() else 0,
            line_dash="dot",
            annotation_text="Média geral",
            annotation_position="top left",
            line_color="gray"
        )
        (col1 if i % 2 == 0 else col2).plotly_chart(fig, key=f"media_{v}")

    # Mantive a segunda série de gráficos (com a "versão numérica" de cores)
    col1, col2 = st.columns(2)
    for i, v in enumerate(variaveis):
        df_media = df_num.groupby("Nivel de Obesidade")[v].mean().reset_index()
        df_media["Nivel de Obesidade"] = df_media["Nivel de Obesidade"].astype(str).str.strip()
        df_media = df_media[df_media["Nivel de Obesidade"].isin(cores_obesidade_num_ajustada.keys())]

        fig = px.bar(
            df_media,
            x="Nivel de Obesidade",
            y=v,
            color="Nivel de Obesidade",
            category_orders={"Nivel de Obesidade": ordem_niveis},
            color_discrete_map=cores_obesidade_num_ajustada
        )
        fig.add_hline(
            y=df_media[v].mean() if not df_media[v].isna().all() else 0,
            line_dash="dot",
            annotation_text="Média geral",
            annotation_position="top left",
            line_color="gray"
        )
        (col1 if i % 2 == 0 else col2).plotly_chart(fig, key=f"media_num_{v}")

# ------------------------------------------------------------
# DASHBOARD
# ------------------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    'Perfil Demográfico', 'Hábitos Alimentares', 
    'Histórico Familiar', 'Comportamentos'
    ])

# ------------------------------------------------------------
# Tab 1: Perfil Demográfico
# ------------------------------------------------------------
with tab1:    
    # --- Peso ---
    box_peso()
   
    texto("Observa-se um aumento progressivo e bem definido do peso corporal conforme o avanço dos níveis de obesidade. Enquanto os grupos abaixo do peso e com peso normal apresentam menor dispersão, os níveis mais elevados, especialmente a obesidade tipo III, exibem ampla variabilidade, indicando maior heterogeneidade corporal nos quadros mais severos.")
    
    # --- Idade por nível de obesidade ---
    grafico_box('Nivel de Obesidade', 'Idade', 'Idade por Nível de Obesidade', 'idade')
    
    texto("A idade média tende a crescer gradualmente com o aumento do nível de obesidade, atingindo seu pico na obesidade tipo II. A presença de indivíduos mais jovens na obesidade tipo III sugere a ocorrência precoce de quadros graves, o que pode indicar fatores de risco acumulados desde a juventude.")
    
    # --- Distribuição por Sexo e Nível de Obesidade ---
    if 'Gênero' in df.columns and 'Nivel de Obesidade' in df.columns:

        # Criar df_sexo com contagem
        df_sexo = df.groupby(['Nivel de Obesidade', 'Gênero']).size().reset_index(name='Contagem')

        # Converter contagem em percentual dentro de cada nível de obesidade
        df_sexo['Percentual'] = df_sexo.groupby('Nivel de Obesidade')['Contagem'].transform(
            lambda x: 100 * x / x.sum()
        )

        cores_genero = {
            'Masculino': '#4B6A97',
            'Feminino': '#6FAFC2'
        }

        # Gráfico de barras empilhadas
        fig_sexo = px.bar(
            df_sexo,
            x='Nivel de Obesidade',
            y='Percentual',
            color='Gênero',
            text='Percentual',
            color_discrete_map=cores_genero,
            title='Distribuição percentual de Sexo por Nível de Obesidade'
        )

        # Formatar texto das barras
        fig_sexo.update_traces(texttemplate='%{text:.1f}%', textposition='inside')

        # Layout
        fig_sexo.update_layout(
            xaxis_title='Nível de Obesidade',
            yaxis_title='Percentual (%)',
            legend_title='Gênero',
            yaxis=dict(range=[0, 100])
        )

        st.plotly_chart(fig_sexo, use_container_width=True)

    else:
        st.warning("As colunas 'Gênero' e 'Nivel de Obesidade' são necessárias para gerar este gráfico.")

    texto("A distribuição entre os sexos é relativamente equilibrada ao longo dos níveis de obesidade, sem evidência de predominância expressiva de um gênero específico. Esse resultado sugere que, na amostra analisada, o sexo não atua como fator determinante isolado para os níveis de obesidade.")
    
    # --- Altura por Sexo ---
    if 'Gênero' in df.columns and 'Altura' in df.columns:

        fig_altura_sexo = px.box(
            df,
            x='Gênero',
            y='Altura',
            color='Gênero',
            color_discrete_map={
                'Masculino': '#4B6A97',
                'Feminino': '#6FAFC2'
            },
            title='Distribuição da Altura por Sexo'
        )

        fig_altura_sexo.update_layout(
            xaxis_title='Sexo',
            yaxis_title='Altura (m)',
            showlegend=False
        )

        st.plotly_chart(fig_altura_sexo, use_container_width=True)

    else:
        st.warning("As colunas 'Gênero' e 'Altura' são necessárias para gerar este gráfico.")

    texto("As diferenças de altura entre os sexos seguem padrões fisiológicos esperados, com médias ligeiramente maiores entre homens. Não se observa associação direta entre altura e níveis de obesidade, indicando que essa variável possui impacto limitado na classificação do estado nutricional.")

    # ---  Relação entre Idade e Peso (sem nível de obesidade) ---
    if 'Idade' in df.columns and 'Peso' in df.columns:

        fig_idade_peso = px.scatter(
            df,
            x='Idade',
            y='Peso',
            opacity=0.6,
            trendline='ols',
            title='Relação entre Idade e Peso'
        )

        fig_idade_peso.update_layout(
            xaxis_title='Idade (anos)',
            yaxis_title='Peso (kg)'
        )

        st.plotly_chart(fig_idade_peso, use_container_width=True)

    else:
        st.warning("As colunas 'Idade' e 'Peso' são necessárias para gerar este gráfico.")

    texto("A relação entre idade e peso indica uma tendência de aumento do peso corporal com o avanço etário, embora com elevada dispersão. Esse comportamento reforça a influência de fatores comportamentais e ambientais acumulados ao longo do tempo, mais do que um efeito linear da idade isoladamente.")

# ------------------------------------------------------------
# Tab 2: Hábitos Alimentares
# ------------------------------------------------------------
with tab2:
    # Verifica se a coluna existe
    if 'Frequência de Consumo de Vegetais' in df.columns:
        # Remove valores nulos
        df_vegetais = df    .dropna(subset=['Frequência de Consumo de Vegetais']).copy()

        # Categoriza frequência de vegetais
        def categorizar_vegetais(valor):
            if valor <= 1.5:
                return 'Baixo (0-1.5)'
            elif valor <= 2.5:
                return 'Médio (1.6-2.5)'
            else:
                return 'Alto (2.6+)'

        df_vegetais['Freq_Vegetais_Categoria'] = df_vegetais['Frequência de Consumo de Vegetais'].apply(categorizar_vegetais)

        ordem_vegetais = ['Baixo (0-1.5)', 'Médio (1.6-2.5)', 'Alto (2.6+)']
        df_vegetais['Freq_Vegetais_Categoria'] = pd.Categorical(
            df_vegetais['Freq_Vegetais_Categoria'],
            categories=ordem_vegetais,
            ordered=True
        )

        cores_vegetais = {
            'Baixo (0-1.5)': '#EBC97A',
            'Médio (1.6-2.5)': '#6FAFC2',
            'Alto (2.6+)': '#4B6A97'
        }
      
        # --- Obesidade vs Consumo de Vegetais (cores personalizadas) ---
        if 'Nivel de Obesidade' in df_vegetais.columns:

            obesity_veg_counts = (
                df_vegetais
                .groupby(['Nivel de Obesidade', 'Freq_Vegetais_Categoria'])
                .size()
                .reset_index(name='count')
            )

            # cria lista de cores a partir do seu esquema de obesidade
            paleta_personalizada = list(cores_obesidade.values())

            heatmap_obesity = alt.Chart(obesity_veg_counts).mark_rect().encode(
                x=alt.X(
                    'Freq_Vegetais_Categoria:N',
                    title='Consumo de Vegetais',
                    sort=ordem_vegetais
                ),
                y=alt.Y(
                    'Nivel de Obesidade:N',
                    title='Nível de Obesidade',
                    sort=ordem_niveis
                ),
                color=alt.Color(
                    'count:Q',
                    scale=alt.Scale(range=paleta_personalizada),
                    legend=alt.Legend(title='Número de Pessoas')
                )
            ).properties(
                title='Relação entre Nível de Obesidade e Consumo de Vegetais'
            )

            st.altair_chart(heatmap_obesity, use_container_width=True)

            texto("O consumo de álcool apresenta uma relação não linear com o peso. Indivíduos que relatam ingerir bebidas alcoólicas “às vezes” tendem a apresentar maior peso médio, enquanto aqueles que nunca consomem ou que relatam consumo frequente ou constante apresentam pesos menores. Esse padrão pode estar associado a contextos sociais e alimentares específicos do consumo ocasional.")       

    texto("Não se identifica um padrão claro de menor consumo de vegetais associado aos níveis mais elevados de obesidade. Tanto indivíduos abaixo do peso quanto aqueles com obesidade tipo III apresentam médias elevadas de consumo, sugerindo que a ingestão de vegetais, isoladamente, não é suficiente para explicar as diferenças de peso corporal.")

    # --- Consumo de Álcool x Peso (frequência + paleta do projeto) ---
    if 'Consumo de Alcool' in df.columns and 'Peso' in df.columns:
        ordem_frequencia = ['Nunca', 'Às vezes', 'Frequentemente', 'Sempre']
        cores_alcool = {
            'Nunca': cores_obesidade_num_ajustada.get(ordem_niveis[0], '#D2E7F1'),
            'Às vezes': cores_obesidade_num_ajustada.get(ordem_niveis[1], '#A9CCE3'),
            'Frequentemente': cores_obesidade_num_ajustada.get(ordem_niveis[-2], '#9B59B6'),
            'Sempre': cores_obesidade_num_ajustada.get(ordem_niveis[-1], '#6C3483')
        }

        fig_alcool_peso = px.box(
            df,
            x='Consumo de Alcool',
            y='Peso',
            color='Consumo de Alcool',
            category_orders={'Consumo de Alcool': ordem_frequencia},
            color_discrete_map=cores_alcool,
            title='Distribuição do Peso por Frequência de Consumo de Álcool'
        )

        fig_alcool_peso.update_layout(
            xaxis_title='Frequência de Consumo de Álcool',
            yaxis_title='Peso (kg)',
            showlegend=False
        )

        st.plotly_chart(fig_alcool_peso, use_container_width=True)

    else:
        st.warning("As colunas 'Consumo de Alcool' e 'Peso' são necessárias.")

    texto("O peso médio é mais elevado entre indivíduos que relatam consumo ocasional de álcool. Em contraste, aqueles que nunca consomem ou que apresentam consumo frequente ou constante exibem pesos médios menores. Esse padrão sugere uma relação indireta, possivelmente mediada por contextos sociais e alimentares associados ao consumo esporádico.")
    
    # --- Alimentos Calóricos x Nível de Obesidade ---
    barras_empilhadas('Consumo de Alimentos com Alta Caloria')

    texto("Há uma associação clara entre o consumo de alimentos altamente calóricos e os níveis mais elevados de obesidade. Nos grupos com obesidade dos tipos I, II e III, quase a totalidade dos indivíduos relata consumir esse tipo de alimento, reforçando seu papel como fator relevante no excesso de peso.")
    
    # --- Comer entre Refeições x Nível de Obesidade (ordinal + paleta) ---
    if 'Comer Entre Refeições' in df.columns and 'Nivel de Obesidade' in df.columns:

        ordem_frequencia = ['Nunca', 'Às vezes', 'Frequentemente', 'Sempre']

        cores_frequencia = {
            'Nunca': cores_obesidade_num_ajustada.get(ordem_niveis[0], '#D2E7F1'),
            'Às vezes': cores_obesidade_num_ajustada.get(ordem_niveis[1], '#A9CCE3'),
            'Frequentemente': cores_obesidade_num_ajustada.get(ordem_niveis[-2], '#9B59B6'),
            'Sempre': cores_obesidade_num_ajustada.get(ordem_niveis[-1], '#6C3483')
        }

        # Contagem
        df_freq = (
            df.groupby(['Nivel de Obesidade', 'Comer Entre Refeições'])
            .size()
            .reset_index(name='Contagem')
        )

        # Percentual dentro de cada nível de obesidade
        df_freq['Percentual'] = df_freq.groupby('Nivel de Obesidade')['Contagem'].transform(
            lambda x: 100 * x / x.sum()
        )

        # Gráfico
        fig_freq = px.bar(
            df_freq,
            x='Nivel de Obesidade',
            y='Percentual',
            color='Comer Entre Refeições',
            category_orders={
                'Nivel de Obesidade': ordem_niveis,
                'Comer Entre Refeições': ordem_frequencia
            },
            color_discrete_map=cores_frequencia,
            barmode='stack',
            text=df_freq['Percentual'].round(1).astype(str) + '%',
            title='Comer entre Refeições por Nível de Obesidade'
        )

        fig_freq.update_traces(textposition='inside')
        fig_freq.update_layout(
            xaxis_title='Nível de Obesidade',
            yaxis_title='Percentual (%)',
            legend_title='Frequência'
        )

        st.plotly_chart(fig_freq, use_container_width=True)

    else:
        st.warning("As colunas 'Comer_Entre_Refeicoes' e 'Nivel de Obesidade' são necessárias para gerar este gráfico.")

    texto("O comportamento de comer entre as refeições é mais frequente entre indivíduos com sobrepeso e obesidade. Esse padrão pode contribuir para um aumento do consumo calórico diário e para o desequilíbrio energético, favorecendo a manutenção do excesso de peso.")

# ------------------------------------------------------------
# Tab 3: Histórico Familiar
# ------------------------------------------------------------
with tab3:
    # --- Histórico Familiar x Nível de Obesidade ---
    barras_empilhadas('Histórico Familiar', df=df)  # assume que a função recebe df
    
    texto("Observa-se um crescimento expressivo da proporção de indivíduos com histórico familiar de obesidade conforme aumenta o nível de excesso de peso. Esse percentual ultrapassa 90% no sobrepeso nível II e atinge 100% na obesidade tipo III, evidenciando forte influência de fatores genéticos e ambientais compartilhados.")

    # --- Histórico Familiar x Peso ---
    if 'Histórico Familiar' in df.columns and 'Peso' in df.columns:

        fig_hist_peso = px.box(
            df,
            x='Histórico Familiar',
            y='Peso',
            color='Histórico Familiar',
            color_discrete_map={
                'Não': '#EBC97A',
                'Sim': '#6391BD'
            },
            title='Distribuição do Peso por Histórico Familiar de Obesidade'
        )

        fig_hist_peso.update_layout(
            xaxis_title='Histórico Familiar de Obesidade',
            yaxis_title='Peso (kg)',
            showlegend=False
        )

        st.plotly_chart(fig_hist_peso, use_container_width=True)

    else:
        st.warning("As colunas 'Histórico Familiar' e 'Peso' são necessárias para gerar este gráfico.")
        
    texto("Indivíduos com histórico familiar de obesidade apresentam peso médio substancialmente maior do que aqueles sem esse histórico. Essa diferença reforça a relevância do ambiente familiar e da predisposição genética como determinantes importantes do peso corporal.")
    
    # --- Histórico Familiar x Alimentos Calóricos (Sim / Não) ---
    if 'Histórico Familiar' in df.columns and 'Consumo de Alimentos com Alta Caloria' in df.columns:

        cores_binarias = {
            'Não': '#EBC97A',
            'Sim': cores_obesidade_num_ajustada.get(ordem_niveis[-1], '#6C3483')
        }

        df_hist_cal = (
            df.groupby(['Histórico Familiar', 'Consumo de Alimentos com Alta Caloria'])
            .size()
            .reset_index(name='Contagem')
        )

        # Percentual dentro de cada grupo de histórico familiar
        df_hist_cal['Percentual'] = df_hist_cal.groupby('Histórico Familiar')['Contagem'].transform(
            lambda x: 100 * x / x.sum()
        )

        fig_hist_cal = px.bar(
            df_hist_cal,
            x='Histórico Familiar',
            y='Percentual',
            color='Consumo de Alimentos com Alta Caloria',
            color_discrete_map=cores_binarias,
            barmode='stack',
            text=df_hist_cal['Percentual'].round(1).astype(str) + '%',
            title='Consumo de Alimentos Calóricos por Histórico Familiar de Obesidade'
        )

        fig_hist_cal.update_traces(textposition='inside')
        fig_hist_cal.update_layout(
            xaxis_title='Histórico Familiar de Obesidade',
            yaxis_title='Percentual (%)',
            legend_title='Consumo de Alimentos Calóricos'
        )

        st.plotly_chart(fig_hist_cal, use_container_width=True)

    else:
        st.warning("As colunas 'Historico_Familiar' e 'Alimentos_Caloricos' são necessárias para gerar este gráfico.")

    texto("Entre indivíduos com histórico familiar de obesidade, observa-se maior prevalência do consumo de alimentos com alta densidade calórica. Esse resultado sugere que padrões alimentares familiares podem contribuir para a perpetuação do excesso de peso entre gerações.")

# ------------------------------------------------------------
# Tab 4: Comportamentos e Estilo de Vida
# ------------------------------------------------------------
with tab4:
    df_walking = df[df['Meio de Transporte - Caminhar'] == 'Walking']

    # --- Caminhar x Nível de Obesidade (apenas caminhar) ---
    if not df_walking.empty and 'Nivel de Obesidade' in df_walking.columns:

        df_walk_ob = (
            df_walking.groupby('Nivel de Obesidade')
            .size()
            .reset_index(name='Contagem')
        )

        df_walk_ob['Percentual'] = 100 * df_walk_ob['Contagem'] / df_walk_ob['Contagem'].sum()

        fig_walk_ob = px.bar(
            df_walk_ob,
            x='Nivel de Obesidade',
            y='Percentual',
            category_orders={'Nivel de Obesidade': ordem_niveis},
            color='Nivel de Obesidade',
            color_discrete_map=cores_obesidade,
            text=df_walk_ob['Percentual'].round(1).astype(str) + '%',
            title='Distribuição do Nível de Obesidade entre os que Caminham como Meio de Transporte'
        )

        fig_walk_ob.update_traces(textposition='inside')
        fig_walk_ob.update_layout(
            xaxis_title='Nível de Obesidade',
            yaxis_title='Percentual (%)'
        )

        st.plotly_chart(fig_walk_ob, use_container_width=True)

    else:
        st.warning("Não há registros suficientes para Walking.")

    texto("Indivíduos que utilizam a caminhada como principal meio de transporte estão pouco representados na amostra, porém concentram-se majoritariamente nos níveis mais baixos de obesidade. Esse achado sugere um efeito protetor da atividade física incorporada à rotina diária.")
    
    # --- Atividade Física (0–3) x Nível de Obesidade ---
    if 'Atividade Física' in df.columns and 'Nivel de Obesidade' in df.columns:

        fig_ativ_ob = px.box(
            df,
            x='Nivel de Obesidade',
            y='Atividade Física',
            category_orders={'Nivel de Obesidade': ordem_niveis},
            color='Nivel de Obesidade',
            color_discrete_map=cores_obesidade,
            title='Distribuição da Atividade Física por Nível de Obesidade'
        )

        fig_ativ_ob.update_layout(
            xaxis_title='Nível de Obesidade',
            yaxis_title='Atividade Física (0–3)'
        )

        st.plotly_chart(fig_ativ_ob, use_container_width=True)

    else:
        st.warning("As colunas 'Atividade Física' e 'Nivel de Obesidade' são necessárias.")

    texto("Níveis mais elevados de obesidade estão associados a menores médias de prática de atividade física. Esse padrão evidencia o papel do sedentarismo tanto na manutenção quanto na progressão do excesso de peso.")

    # --- Caminhar (meio de transporte) x Idade ---
    if 'Meio de Transporte - Caminhar' in df.columns and 'Idade' in df.columns:

        # Cria variável binária: Caminhada vs Outros
        df['Walking_Transporte'] = df['Meio de Transporte - Caminhar'].apply(
            lambda x: 'Caminhada' if str(x).strip() == 'Walking' else 'Outros'
        )

        fig_walking_idade = px.box(
            df,
            x='Walking_Transporte',
            y='Idade',
            color='Walking_Transporte',
            color_discrete_map={
                'Caminhada': '#EBC97A',
                'Outros': '#6391BD'
            },
            title='Distribuição da Idade por Uso de Caminhada como Meio de Transporte'
        )

        fig_walking_idade.update_layout(
            xaxis_title='Meio de Transporte',
            yaxis_title='Idade (anos)',
            showlegend=False
        )

        st.plotly_chart(fig_walking_idade, use_container_width=True)

    else:
        st.warning("As colunas 'Meio_Transporte' e 'Idade' são necessárias.")

    texto("O uso da caminhada como meio de transporte é mais frequente entre indivíduos mais jovens. Esse comportamento pode indicar hábitos mais ativos no início da vida adulta, com possíveis impactos positivos no controle do peso ao longo do tempo.")



