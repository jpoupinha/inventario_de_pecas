
import streamlit as st
import pandas as pd
import os

inventario_path = "inventario_pecas_por_item.xlsx"

if os.path.exists(inventario_path):
    inventario_df = pd.read_excel(inventario_path, engine="openpyxl")
else:
    inventario_df = pd.DataFrame(columns=["Nome", "Item", "Quantidade", "Criticidade"])

criticas_df = pd.read_excel("base_pecas_criticas_por_item.xlsx", engine="openpyxl")

st.title("Inventário de Peças por Item - Armazém DPD Lisbon")

st.header("Registo de Nova Peça")
with st.form("formulario_peca"):
    nome = st.text_input("Nome da Peça")
    item = st.number_input("Número do Item", min_value=1, step=1)
    quantidade = st.number_input("Quantidade Existente", min_value=0, step=1)
    criticidade = st.selectbox("Criticidade", options=["1 - Paragem Total", "2 - Condicionamentos", "N/A"])
    submeter = st.form_submit_button("Registar")

    if submeter:
        nova_linha = pd.DataFrame({
            "Nome": [nome],
            "Item": [item],
            "Quantidade": [quantidade],
            "Criticidade": [criticidade.split(" ")[0]]
        })
        inventario_df = pd.concat([inventario_df, nova_linha], ignore_index=True)
        inventario_df.to_excel(inventario_path, index=False)
        st.success("Peça registada com sucesso!")

st.header("Peças Registadas")
st.dataframe(inventario_df)

st.header("Peças Críticas em Falta ou com Stock Baixo")

comparacao_df = criticas_df.merge(inventario_df, on="Item", how="left")
comparacao_df["Quantidade"] = comparacao_df["Quantidade"].fillna(0)
pecas_em_falta = comparacao_df[(comparacao_df["Criticidade_x"] == 1) & (comparacao_df["Quantidade"] < 1)]
pecas_baixo_stock = comparacao_df[(comparacao_df["Criticidade_x"] == 1) & (comparacao_df["Quantidade"] > 0) & (comparacao_df["Quantidade"] < 2)]

st.subheader("⚠️ Peças Críticas em Falta")
st.dataframe(pecas_em_falta[["Nome_x", "Item", "Quantidade"]])

st.subheader("🔵 Peças Críticas com Stock Baixo")
st.dataframe(pecas_baixo_stock[["Nome_x", "Item", "Quantidade"]])
