import pandas as pd

# Shared mapping for transport options (UI label -> training code)
MTRANS_MAP = {
    'Carro': 'Automobile',
    'Moto': 'Motorbike',
    'Bicicleta': 'Bike',
    'Transporte público': 'Public_Transportation',
    'Caminhar': 'Walking'
}


def load_data():
    df = pd.read_csv("C:/Users/jenil/OneDrive/Documents/Faculdade/Tech Challenge 4/obesity/Obesity.csv")

    # ------------------------------------------------------------
    # 1️⃣ Renomear colunas
    # ------------------------------------------------------------
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
        'SCC': 'Monitora Calorias Diárias Consumidas',
        'FAF': 'Atividade Física',
        'TUE': 'Uso de Dispositivos Tecnológicos',
        'CALC': 'Consumo de Alcool',
        'MTRANS': 'Meio de Transporte',
        'Obesity': 'Nivel de Obesidade'
    }
    df.rename(columns=colunas_pt, inplace=True)


    # ------------------------------------------------------------
    # 2️⃣ Mapear níveis de obesidade
    # ------------------------------------------------------------
    mapa_obesidade = {
        'Insufficient_Weight': 'Abaixo do peso',
        'Normal_Weight': 'Peso normal',
        'Overweight_Level_I': 'Sobrepeso Tipo I',
        'Overweight_Level_II': 'Sobrepeso Tipo II',
        'Obesity_Type_I': 'Obesidade Tipo I',
        'Obesity_Type_II': 'Obesidade Tipo II',
        'Obesity_Type_III': 'Obesidade Tipo III'
    }

    ordem_niveis = list(mapa_obesidade.values())

    df['Nivel de Obesidade'] = df['Nivel de Obesidade'].map(mapa_obesidade)
    df['Nivel de Obesidade'] = pd.Categorical(df['Nivel de Obesidade'], categories=ordem_niveis, ordered=True)

    # ------------------------------------------------------------
    # 3️⃣ Mapear Comer Entre Refeições e Alcool
    # ------------------------------------------------------------
    mapa_frequencia = {
        'Always': 'Sempre',
        'Frequently': 'Frequentemente',
        'Sometimes': 'Às vezes',
        'no': 'Nunca'
    }

    for coluna in ['Comer Entre Refeições', 'Consumo de Alcool']:
        if coluna in df.columns:
            df[coluna] = df[coluna].map(mapa_frequencia).fillna(df[coluna])

    ordem_entre_refeicoes = ['Nunca', 'Às vezes', 'Frequentemente', 'Sempre']
    df['Comer Entre Refeições'] = pd.Categorical(df['Comer Entre Refeições'],
                                                 categories=ordem_entre_refeicoes,
                                                 ordered=True)

    # ------------------------------------------------------------
    # 4️⃣ Mapear Sim/Não e gênero
    # ------------------------------------------------------------
    mapa_sim_nao = {'yes': 'Sim', 'no': 'Não', 'Sim': 'Sim', 'Não': 'Não'}
    mapa_genero = {'Male': 'Masculino', 'Female': 'Feminino'}

    df['Gênero'] = df['Gênero'].map(mapa_genero)

    colunas_binarias = [
        'Histórico Familiar',
        'Consumo de Alimentos com Alta Caloria',
        'Fuma',
        'Monitora Calorias Diárias Consumidas'
    ]

    for c in colunas_binarias:
        df[c] = df[c].map(mapa_sim_nao)

    # ------------------------------------------------------------
    # 5️⃣ Criar versão numérica
    # ------------------------------------------------------------
    df_num = df.copy()

    # Binárias
    for c in colunas_binarias:
        df_num[c] = df_num[c].map({'Sim': 1, 'Não': 0})

    # Comer Entre Refeições numérico
    mapa_entre_refeicoes_num = {
        'Nunca': 0,
        'Às vezes': 1,
        'Frequentemente': 2,
        'Sempre': 3
    }
    df_num['Comer Entre Refeições'] = df['Comer Entre Refeições'].map(mapa_entre_refeicoes_num)

    # Obesidade numérica
    mapa_obesidade_num = dict(zip(ordem_niveis, range(7)))
    df_num['Nivel de Obesidade'] = df['Nivel de Obesidade'].map(mapa_obesidade_num)

    ordem_niveis_num = [0, 1, 2, 3, 4, 5, 6]
    
    # ------------------------------------------------------------
    # 6️⃣ Cores
    # ------------------------------------------------------------
    cores_obesidade = {
        'Abaixo do peso': '#F2D7A6',
        'Peso normal': '#EBC97A',
        'Sobrepeso Tipo I': '#C5C98A',
        'Sobrepeso Tipo II': '#91C4B8',
        'Obesidade Tipo I': '#6FAFC2',
        'Obesidade Tipo II': "#6391BD",
        'Obesidade Tipo III': '#4B6A97'
    }

    cores_obesidade_num = {
        0: '#F2D7A6',
        1: '#EBC97A',
        2: '#C5C98A',
        3: '#91C4B8',
        4: '#6FAFC2',
        5: "#6391BD",
        6: '#4B6A97'
    }

    cores_obesidade_num_ajustada = dict(zip(ordem_niveis, cores_obesidade_num.values()))

    # ------------------------------------------------------------
    # 🔧 Ajuste final: garantir df_num 100% numérico
    # ------------------------------------------------------------

    # Remover colunas que contém texto e não têm versão numérica
        # Converter qualquer coluna categórica restante para códigos numéricos
    df_num = df_num.apply(
        lambda col: col.astype('category').cat.codes
        if col.dtype == 'category' or col.dtype == 'object'
        else col
    )

    # Garantir que todas são numéricas
    df_num = df_num.apply(pd.to_numeric, errors='coerce')

    # ------------------------------------------------------------
    # 📌 Final
    # ------------------------------------------------------------
    return df, df_num, ordem_niveis, ordem_niveis_num, cores_obesidade, cores_obesidade_num, cores_obesidade_num_ajustada
    
