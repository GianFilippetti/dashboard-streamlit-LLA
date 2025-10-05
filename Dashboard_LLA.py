
# Acordate de armar el requiremetns txt
# Git hub comandos
# git init
# git config --global user.name "Gian Filippetti"
# git config --global user.email 'gian_filippetti_97@hotmail.com'
# git add . https://github.com/GianFilippetti/dashboard-streamlit-LLA.git
# git commit -m "Primer commit - Dashboard Streamlit"
# git remote add origin https://github.com/GianFilippetti/dashboard-streamlit-LLA.git solo si lo teness q añadir por primera vez
# git branch -M main
# git push -u origin main
# streamlit run dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import BytesIO

# ---- CREDENCIALES ----
USER = st.secrets["credentials"]["user"]
PASSWORD = st.secrets["credentials"]["password"]

def login():
    st.title("🔒 Acceso restringido")
    
    if "user_input" not in st.session_state:
        st.session_state["user_input"] = ""
    if "pwd_input" not in st.session_state:
        st.session_state["pwd_input"] = ""
    
    with st.form("login_form"):
        st.session_state["user_input"] = st.text_input("Usuario", st.session_state["user_input"])
        st.session_state["pwd_input"] = st.text_input("Contraseña", st.session_state["pwd_input"], type="password")
        submitted = st.form_submit_button("Ingresar")
    
        if submitted:
            if st.session_state["user_input"] == USER and st.session_state["pwd_input"] == PASSWORD:
                st.session_state["auth"] = True
            else:
                st.error("❌ Usuario o contraseña incorrectos")

# ---- DASHBOARD ----
# ---- DASHBOARD ----
def dashboard():
    st.title("📊 Dashboard desde Google Drive (.xlsx)")

    url = "https://docs.google.com/spreadsheets/d/1s9364GPO8W_0O-umugtyU-uHVlAKUnCEgj1WIturaEg/export?format=xlsx"
    response = requests.get(url)

    # --- Leer Hoja1 ---
    df1 = pd.read_excel(BytesIO(response.content), sheet_name="Hoja 1", engine="openpyxl")
    st.subheader("Vista previa de Hoja1")
    st.dataframe(df1.head())

    # Gráfico Hoja1
    x_col1 = "Fecha"
    y_col1 = "Cantidad_seguidores_pagina_principal"
    df1[y_col1] = pd.to_numeric(df1[y_col1], errors="coerce")

    fig1 = px.line(df1, x=x_col1, y=y_col1, markers=True)
    fig1.update_layout(
        xaxis_title=x_col1,
        yaxis_title=y_col1,
        title=f"{y_col1} vs {x_col1}",
        template="plotly_white"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # --- Leer Hoja2 ---
    df2 = pd.read_excel(BytesIO(response.content), sheet_name="Hoja 2", engine="openpyxl")
    st.subheader("Vista previa de Hoja2")
    st.dataframe(df2.head())

    # Gráfico Hoja2 (ejemplo, cambia columnas según tus datos)
    x_col2 = "Fecha"
    y_col2 = "Stand cantidad de personas que se acercaron"  # reemplaza con el nombre real de la columna
    df2[y_col2] = pd.to_numeric(df2[y_col2], errors="coerce")

    fig2 = px.line(df2, x=x_col2, y=y_col2, markers=True)
    fig2.update_layout(
        xaxis_title=x_col2,
        yaxis_title=y_col2,
        title=f"{y_col2} vs {x_col2}",
        template="plotly_white"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---- INICIALIZAR SESSION_STATE ----
if "auth" not in st.session_state:
    st.session_state["auth"] = False

# ---- FLUJO PRINCIPAL ----
if not st.session_state["auth"]:
    login()
else:
    dashboard()