import streamlit as st

def texto(text):
    st.markdown(f"""
        <p style='text-align: justify; font-size: 18px; max-width: 900px; margin: auto;'>
            {text}
        </p>
    """, unsafe_allow_html=True)
    
st.subheader("Recomendações Personalizadas")
texto("Com base nos padrões identificados nos dados, esta seção apresenta recomendações voltadas à prevenção e controle da obesidade, considerando fatores como idade, hábitos alimentares e estilo de vida.")

st.markdown("---")

st.markdown("### Por Nível de Obesidade")

with st.expander("🔹 Abaixo do peso"):
    texto("Incentivar acompanhamento nutricional para garantir ganho de peso saudável, especialmente entre mulheres jovens com baixa estatura.")

with st.expander("🔹 Peso normal"):
    texto("Manter hábitos saudáveis com foco em alimentação balanceada e atividade física regular para evitar progressão para sobrepeso.")

with st.expander("🔹 Sobrepeso Tipo I e II"):
    texto("Estimular mudanças graduais no estilo de vida, como redução de alimentos ultraprocessados e aumento da prática de exercícios.")

with st.expander("🔹 Obesidade Tipo I, II e III"):
    texto("Recomendar acompanhamento médico e nutricional, além de estratégias multidisciplinares para controle de peso e prevenção de comorbidades.")

st.markdown("### Por Hábitos e Estilo de Vida")

with st.expander("Baixo consumo de vegetais"):
    texto("Aumentar a ingestão de vegetais frescos pode contribuir para o controle do peso e melhora metabólica.")

with st.expander("Alto consumo de alimentos calóricos"):
    texto("Reduzir frituras, doces e refrigerantes é essencial para evitar o acúmulo de gordura corporal.")

with st.expander("Sedentarismo"):
    texto("Incorporar pelo menos 150 minutos de atividade física moderada por semana pode melhorar significativamente a saúde geral.")

st.markdown("---")
st.subheader("Considerações Finais")
texto("Mudanças simples e consistentes no dia a dia podem ter grande impacto na saúde a longo prazo. Este painel busca apoiar decisões mais conscientes e promover qualidade de vida.")
