import streamlit as st

def texto(text):
    st.markdown(f"""
        <p style='text-align: justify; font-size: 18px; max-width: 900px; margin: auto;'>
            {text}
        </p>
    """, unsafe_allow_html=True)
    

st.subheader("Recomendações Baseadas nos Dados")
texto("As recomendações a seguir foram construídas a partir dos padrões observados nos dados, considerando variáveis como faixa etária, hábitos alimentares, estilo de vida, nível de atividade física e presença de histórico familiar.")


st.markdown("---")
st.markdown("### Por Perfil de Nível de Obesidade")

with st.expander("🔹 Abaixo do Peso"):
    texto("""
        • Incentivar acompanhamento nutricional para evitar deficiências nutricionais e promover ganho de peso saudável.
        • Atenção redobrada em faixas etárias mais jovens, onde o baixo peso teve maior incidência.
        • Estímulo ao aumento calórico com qualidade: cereais integrais, leguminosas, proteínas e frutas.
    """)

with st.expander("🔹 Peso Normal"):
    texto("""
        • Reforçar manutenção de hábitos alimentares saudáveis para evitar progressão ao sobrepeso.
        • Incentivar prática regular de atividade física ao menos 150 min/semana.
        • Evitar consumo excessivo de alimentos ultraprocessados.
    """)

with st.expander("🔹 Sobrepeso Tipo I e II"):
    texto("""
        • Redução gradual de alimentos de alta densidade energética como frituras, doces e bebidas açucaradas.
        • Inserção de vegetais e fibras para maior saciedade e melhora metabólica.
        • Aumento da prática de atividades aeróbicas e exercícios resistidos.
    """)

with st.expander("🔹 Obesidade Tipo I, II e III"):
    texto("""
        • Recomendado acompanhamento multidisciplinar (nutricionista, endocrinologista, educador físico).
        • Controle de fatores associados como hipertensão, diabetes e dislipidemias.
        • Estratégias comportamentais: controle de porções e registro alimentar.
        • Importante atenção ao sono e estresse, que aparecem relacionados ao ganho de peso.
    """)


st.markdown("### Por Hábitos Alimentares e Estilo de Vida")

with st.expander("Baixo Consumo de Vegetais"):
    texto("""
        • Aumentar vegetais frescos melhora saciedade e reduz densidade calórica.
        • Estratégias simples: incluir ao menos 1 porção no almoço e jantar.
    """)

with st.expander("Alto Consumo de Alimentos Ultracalóricos"):
    texto("""
        • Evitar frituras, doces, fast food e bebidas açucaradas reduz significativamente risco de sobrepeso.
        • Sugestão: substituir refrigerantes por água ou chás sem açúcar.
    """)

with st.expander("Histórico Familiar de Obesidade"):
    texto("""
        • Indivíduos com histórico familiar apresentaram maior probabilidade de sobrepeso e obesidade.
        • Estratégias precoces são fundamentais: alimentação equilibrada + atividade física regular.
        • Importante atenção em jovens com histórico familiar, pois tendem a desenvolver mais cedo.
    """)


st.markdown("---")
st.subheader("Considerações Finais")
texto("""
        Os dados reforçam que intervenções simples e consistentes podem gerar impacto significativo em longo prazo.
        O objetivo deste painel é auxiliar na construção de estratégias preventivas e personalizadas para promoção da saúde e qualidade de vida.
    """)
