import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference

# Configuration de la page
st.set_page_config(
    page_title='Comparaison de chiffre d\'affaires',
    page_icon=':chart_with_upwards_trend:',
    layout='wide',
    initial_sidebar_state='auto'
)
st.title('Comparaison entre années')

# Layout en colonnes pour les entrées utilisateur
year, ca = st.columns(2) 

# Obtenir la date actuelle
date_actuelle = datetime.date.today()

# Entrées utilisateur pour les années et les chiffres d'affaires
with year: 
    st.text('Choisissez une année')
    year_minus_one =  st.number_input('Année de référence', min_value=2014, max_value=date_actuelle.year - 1, step=1)
    year_current =  st.number_input('Année actuelle', min_value=2014, max_value=date_actuelle.year, step=1)
    
with ca: 
    st.text('Entrez le chiffre d\'affaires')
    ca_minus_one =  st.number_input('Chiffre d\'affaires année de référence', min_value=0.0, step=0.01)
    ca_current =  st.number_input('Chiffre d\'affaires année actuelle', min_value=0.0, step=0.01)

# Choix des seuils pour les catégories de taux de croissance
st.sidebar.title('Paramètres des catégories de croissance')
croissance_elevee = st.sidebar.slider('Seuil pour croissance élevée (%)', min_value=0, max_value=50, value=20)
croissance_moderée = st.sidebar.slider('Seuil pour croissance modérée (%)', min_value=0, max_value=50, value=5)
declin_faible = st.sidebar.slider('Seuil pour déclin faible (%)', min_value=-30, max_value=50, value=-5)
declin_moderé = st.sidebar.slider('Seuil pour déclin modéré (%)', min_value=-30, max_value=50, value=-20)

# Comparaison et affichage des résultats
if st.button('Comparer'): 
    if year_minus_one >= year_current:
        st.error("L'année de référence doit être inférieure à l'année actuelle.")
    elif year_minus_one and year_current and ca_minus_one and ca_current:
        percent = ((ca_current - ca_minus_one) / ca_minus_one) * 100
        if percent > croissance_elevee:
            category = "Croissance élevée"
            st.success(f"Le chiffre d'affaires a augmenté de {ca_current - ca_minus_one:.2f} € entre {year_minus_one} et {year_current}. Le taux de croissance est de {percent:.2f} %, le taux de croissance est : {category}. ")
        elif percent > croissance_moderée:
            category = "Croissance modérée"
            st.warning(f"Le chiffre d'affaires a augmenté de {ca_current - ca_minus_one:.2f} € entre {year_minus_one} et {year_current}. Le taux de croissance est de {percent:.2f} %, le taux de croissance est : {category}. ")
        elif percent > 0:
            category = "Croissance faible"
            st.info(f"Le chiffre d'affaires a augmenté de {ca_current - ca_minus_one:.2f} € entre {year_minus_one} et {year_current}. Le taux de croissance est de {percent:.2f} %, le taux de croissance est : {category}. ")
        elif percent == 0:
            category = "Stable"
            st.info(f"Le chiffre d'affaires est resté stable entre {year_minus_one} et {year_current}. Le taux de croissance est de {percent:.2f} %, le taux de croissance est : {category}. ")
        elif percent > declin_faible:
            category = "Déclin faible"
            st.error(f"Le chiffre d'affaires a diminué de {ca_minus_one - ca_current:.2f} € entre {year_minus_one} et {year_current}. Le taux de croissance est de {percent:.2f} %, le taux de croissance est : {category}. ")
        elif percent > declin_moderé:
            category = "Déclin modéré"
            st.error(f"Le chiffre d'affaires a diminué de {ca_minus_one - ca_current:.2f} € entre {year_minus_one} et {year_current}. Le taux de croissance est de {percent:.2f} %, le taux de croissance est : {category}. ")
        else:
            category = "Déclin important"
            st.error(f"Le chiffre d'affaires a diminué de {ca_minus_one - ca_current:.2f} € entre {year_minus_one} et {year_current}. Le taux de croissance est de {percent:.2f} %, le taux de croissance est : {category}. ")

        # Création d'un DataFrame pour le graphique
        data = pd.DataFrame({
            'Année': [year_minus_one, year_current],
            'Chiffre d\'affaires': [ca_minus_one, ca_current]
        })

        # Affichage du graphique
        fig, ax = plt.subplots()
        sns.barplot(x='Année', y='Chiffre d\'affaires', data=data, ax=ax)
        ax.set_title('Chiffre d\'affaires par année')
        ax.set_ylabel('Chiffre d\'affaires (€)')
        ax.set_xlabel('Année')
        st.pyplot(fig)

        # Création d'un fichier Excel avec les données et le graphique
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            data.to_excel(writer, index=False, sheet_name='Données')
            workbook = writer.book
            worksheet = writer.sheets['Données']
            chart = workbook.add_chart({'type': 'column'})
            chart.add_series({
                'values': '=Données!$B$2:$B$3',
                'categories': '=Données!$A$2:$A$3',
            })
            worksheet.insert_chart('D2', chart)
        excel_buffer.seek(0)

        # Téléchargement des résultats (graphique + données)
        st.download_button(
            label="Télécharger les résultats",
            data=excel_buffer,
            file_name=f"resultats_{year_minus_one}_{year_current}.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )