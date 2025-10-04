
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
def dashboard():
    st.title("📊 Dashboard desde Google Drive (.xlsx)")

    url = "https://docs.google.com/spreadsheets/d/1s9364GPO8W_0O-umugtyU-uHVlAKUnCEgj1WIturaEg/export?format=xlsx"
    response = requests.get(url)
    df = pd.read_excel(BytesIO(response.content), engine="openpyxl")
    
    st.subheader("Vista previa de los datos")
    st.dataframe(df.head())
    
    # Columnas a graficar
    x_col = "Fecha"
    y_col = "Cantidad_seguidores_pagina_principal"
    df[y_col] = pd.to_numeric(df[y_col], errors="coerce")
    
    fig = px.line(df, x=x_col, y=y_col, markers=True)
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        title=f"{y_col} vs {x_col}",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---- INICIALIZAR SESSION_STATE ----
if "auth" not in st.session_state:
    st.session_state["auth"] = False

# ---- FLUJO PRINCIPAL ----
if not st.session_state["auth"]:
    login()
else:
    dashboard()