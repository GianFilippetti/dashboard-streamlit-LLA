
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

def dashboard():
    st.title("📊 Dashboard desde Google Drive (.xlsx)")

    # URL directa para exportar como Excel
    url = "https://docs.google.com/spreadsheets/d/1s9364GPO8W_0O-umugtyU-uHVlAKUnCEgj1WIturaEg/export?format=xlsx"
    response = requests.get(url)

    # Leer todas las hojas
    all_sheets = pd.read_excel(BytesIO(response.content), sheet_name=None, engine="openpyxl")

    # Crear pestañas
    tab1, tab2 = st.tabs(["📈 Seguidores", "🎪 Stand y QR"])

    # ---- Hoja 1 ----
    with tab1:
        df1 = all_sheets["Hoja1"]  # Asegurate del nombre real de la hoja
        st.subheader("📄 Vista previa - Hoja 1 (Seguidores)")
        st.dataframe(df1.head())

        # Gráficos
        fig1 = px.line(df1, x="Fecha", y="Cantidad_seguidores_pagina_principal", 
                    title="Evolución Seguidores Página Principal", markers=True)
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.line(df1, x="Fecha", y="Cantidad_seguidores_pagina_juventud", 
                    title="Evolución Seguidores Página Juventud", markers=True)
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.line(df1, x="Fecha", y="Cantidad_personas_activas", 
                    title="Cantidad de Personas Activas", markers=True)
        st.plotly_chart(fig3, use_container_width=True)

    # ---- Hoja 2 ----
    with tab2:
        df2 = all_sheets["Hoja2"]  # Asegurate del nombre real de la hoja
        st.subheader("📄 Vista previa - Hoja 2 (Stand y QR)")
        st.dataframe(df2.head())

        fig4 = px.bar(df2, x="Fecha", y="Stand cantidad de personas que se acercaron",
                    title="Personas que se acercaron al stand")
        st.plotly_chart(fig4, use_container_width=True)

        fig5 = px.bar(df2, x="Fecha", y="Cantidad de personas que escaneron el QR",
                    title="Personas que escanearon el QR")
        st.plotly_chart(fig5, use_container_width=True)

        fig6 = px.line(df2, x="Fecha", y="Cantidad reacciones en el video",
                    title="Reacciones en el Video", markers=True)
        st.plotly_chart(fig6, use_container_width=True)