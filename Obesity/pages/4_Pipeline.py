import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# =========================
# CONFIGURAÇÕES INICIAIS
# =========================
st.set_page_config(page_title="Análise de Obesidade", layout="wide")

# =========================
# FUNÇÃO DE TEXTO JUSTIFICADO
# =========================
def texto(text):
    st.markdown(
        f"""
        <p style='text-align: justify; font-size: 18px; max-width: 900px; margin: auto;'>
            {text}
        </p>
        """,
        unsafe_allow_html=True
    )

# =========================
# CARREGAMENTO DOS DADOS
# =========================
df = pd.read_csv(
    "C:/Users/jenil/OneDrive/Documents/Faculdade/Tech Challenge 4/obesity/df_numerico.csv"
)
df_modelo = df.copy()

# =========================
# TÍTULO
# =========================
st.title("Análise e Modelagem de Dados de Obesidade")

# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(
    ["Pipeline de ML", "Correlação", "Comparação de Modelos"]
)

# =========================
# TAB 1 — PIPELINE
# =========================
with tab1:
    st.header("Pipeline de Machine Learning")

    st.subheader("1. Separação de Variáveis")
    st.markdown("""
    - **Numéricas contínuas**: idade, altura, peso, consumo de vegetais, número de refeições, ingestão de água, atividade física e tempo de tela.  
    - **Categóricas nominais**: sexo, histórico familiar, consumo de alimentos calóricos, hábito de fumar, monitoramento de calorias e meio de transporte.  
    - **Categóricas ordinais**: frequência de alimentação entre refeições, consumo de álcool e nível de obesidade (variável alvo).
    """)

    st.subheader("2. Pré-processamento")
    st.markdown("""
    - Imputação de valores ausentes (média e moda).  
    - Normalização com `MinMaxScaler`.  
    - Codificação One-Hot e Ordinal.
    """)

    st.subheader("3. Balanceamento de Classes")
    st.markdown("""
    - Aplicação do **SMOTE** apenas no conjunto de treino.
    """)

    st.subheader("4. Treinamento do Modelo")
    st.markdown("""
    - Modelo principal: **Random Forest Classifier**.  
    - Capaz de capturar relações não lineares.
    """)

    st.subheader("5. Avaliação e Interpretação")
    st.markdown("""
    - Acurácia, matriz de confusão e relatório de classificação.  
    - Importância das variáveis.
    """)

# =========================
# TAB 2 — CORRELAÇÃO
# =========================
with tab2:
    st.header("Correlação entre Variáveis Numéricas")

    corr = df.select_dtypes(include="number").corr()

    texto(
        "O heatmap de correlação apresenta as relações lineares entre as variáveis numéricas. "
        "Cores quentes indicam correlações positivas e cores frias indicam correlações negativas."
    )

    plt.figure(figsize=(12, 10))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Heatmap de Correlação")
    st.pyplot(plt)

# =========================
# TAB 3 — COMPARAÇÃO DE MODELOS (COM DROPDOWN)
# =========================
with tab3:
    st.header("Comparação de Modelos de Classificação")
    
    texto(
        "O modelo Random Forest apresentou o melhor desempenho geral, com acurácia aproximada de 94,8%, "
        "além de permitir a interpretação da importância das variáveis. Comparado aos demais modelos, "
        "mostrou-se mais robusto para o problema de classificação da obesidade."
    )

    st.markdown("---")
    
    X = df_modelo.drop(columns="obesidade")
    y = df_modelo["obesidade"]

    # Dropdown de modelos
    model_name = st.selectbox(
        "Selecione o modelo:",
        ["Random Forest", "Logistic Regression", "Gradient Boosting"]
    )

    # Instanciação
    if model_name == "Random Forest":
        model = RandomForestClassifier(random_state=42)
    elif model_name == "Logistic Regression":
        model = LogisticRegression(max_iter=8000, random_state=42)
    else:
        model = GradientBoostingClassifier(random_state=42)

    # Treinamento
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Métricas
    st.subheader(f"Resultados — {model_name}")
    st.write(f"**Acurácia:** {accuracy_score(y_test, y_pred):.4f}")
    st.text("Relatório de Classificação:")
    st.text(classification_report(y_test, y_pred, zero_division=0))

    # Matriz de confusão
    st.subheader("Matriz de Confusão")
    fig, ax = plt.subplots()
    ConfusionMatrixDisplay.from_estimator(
        model, X_test, y_test, ax=ax, cmap="Blues", normalize="true"
    )
    st.pyplot(fig)

    # Importância das variáveis
    if hasattr(model, "feature_importances_"):
        st.subheader("Importância das Variáveis")
        importances = pd.Series(
            model.feature_importances_, index=X.columns
        ).sort_values(ascending=False)

        fig2, ax2 = plt.subplots(figsize=(8, 6))
        sns.barplot(x=importances.values, y=importances.index, ax=ax2)
        st.pyplot(fig2)
    else:
        st.info("Este modelo não possui análise de importância das variáveis.")


