import streamlit as st
from modelo import (
    carregar_dados,
    treinar_modelos,
    prever_melhorado
)

st.set_page_config(page_title="Análise Clínica Veterinária com IA", layout="centered")

st.title("🐾 Análise Clínica Veterinária com IA")
st.write("Insira a anamnese do paciente para prever os cuidados clínicos e analisar doenças mencionadas.")

# Inicialização de estado
if "input_key" not in st.session_state:
    st.session_state.input_key = "input_0"
if "resultado" not in st.session_state:
    st.session_state.resultado = None
if "analisado" not in st.session_state:
    st.session_state.analisado = False

# Recarregar
if st.button("🆕 Analisar nova anamnese"):
    st.session_state.input_key = "input_" + str(st.session_state.input_key.count("_") + 1)
    st.session_state.resultado = None
    st.session_state.analisado = False

# Entrada
texto = st.text_area("✍️ Digite a anamnese do paciente:", key=st.session_state.input_key)

if st.button("🔍 Analisar"):
    if texto.strip() == "":
        st.warning("Digite uma anamnese para analisar.")
    else:
        try:
            df, palavras_chave_total, palavras_chave_graves = carregar_dados()
            features = ['Idade', 'Peso', 'Gravidade', 'Dor', 'Mobilidade', 'Apetite', 'Temperatura']
            features_eutanasia = features + ['tem_doenca_letal']

            modelos = treinar_modelos(df, features, features_eutanasia)

            resultado = prever_melhorado(
                texto, modelos, modelos[4], modelos[5], palavras_chave_total,
                palavras_chave_graves, features, features_eutanasia
            )

            if isinstance(resultado, dict):
                st.session_state.resultado = resultado
                st.session_state.analisado = True
            else:
                st.error("Erro inesperado na análise.")
        except Exception as e:
            st.error(f"Erro ao carregar dados ou treinar modelos: {e}")
            st.stop()

# Exibir resultado
if st.session_state.analisado and st.session_state.resultado:
    st.subheader("📋 Resultado da Análise")
    for k, v in st.session_state.resultado.items():
        st.markdown(f"**{k}**: {v}")

if st.session_state.analisado:
    if st.button("➕ Adicionar à Lista de Eutanásia"):
        st.success("✅ Paciente adicionado à lista de eutanásia (simulação).")

    if st.button("❌ Encerrar Programa"):
        st.info("Aplicação encerrada.")
        st.stop()
