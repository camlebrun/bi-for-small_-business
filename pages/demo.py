import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from io import BytesIO
import os

# Configuration de la page
st.set_page_config(
    page_title="Outil de comparaison des chiffres d'affaires",
    page_icon="📊",
    layout="wide")

st.markdown(
    "<h1 style='text-align: center;'>Outil de comparaison des chiffres d'affaires</h1>",
    unsafe_allow_html=True)

# Définition du chemin vers le fichier CSV
file_path = "times_series.csv"

# Vérification de l'existence du fichier
if os.path.exists(file_path):
    st.write("Fichier trouvé :", file_path)
    # Lecture du fichier CSV
    df = pd.read_csv(file_path, usecols=["Date", "Sales Revenue"])
    min_val = df["Sales Revenue"].min().round(2)
    min_date = df.loc[df["Sales Revenue"].idxmin()]["Date"]
    max_val = df["Sales Revenue"].max().round(2)
    max_date = df.loc[df["Sales Revenue"].idxmax()]["Date"]
    mean_val = df["Sales Revenue"].mean().round(2)
    mean_date = df.iloc[df['Sales Revenue'].sub(
        mean_val).abs().idxmin()]["Date"]
    median_val = df["Sales Revenue"].median().round(2)
    median_date = df.iloc[df['Sales Revenue'].sub(
        median_val).abs().idxmin()]["Date"]

else:
    st.error("Fichier introuvable :", file_path)
    st.stop()
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["Sales Revenue"],
        mode='lines',
        name="CA",
        hovertemplate="CA: %{y}<extra></extra>"))
tab1, tab2, tab3, tab4 = st.tabs(
    ["Données importés", "Statistiques général", "Série temporelle", "Télécharger les données"])


with tab1:
    st.markdown(
        "<h3 style='text-align: center;'>Vue globale des données</h3>",
        unsafe_allow_html=True)

    right, left = st.columns(2)
    with right:
        st.plotly_chart(fig, use_container_width=True)

    with left:
        st.dataframe(df, use_container_width=True, hide_index=True)

with tab2:
    st.markdown(
        "<h3 style='text-align: center;'>Statistiques sur le CA</h3>",
        unsafe_allow_html=True)

# EDA
    st.write(
        """
        <style>
        [data-testid="stMetricDelta"] svg {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    col_r, col_l = st.columns(2)
    with col_l:
        st.metric(label="Minimum du CA", value=f"{min_val}€", delta=min_date)
        st.metric(label="Maximum du CA", value=f"{max_val}€", delta=max_date)

        # st.write(f"**Maximum du CA:** {max_val:.2f} pour la data du {min_date}")

    with col_r:
        st.metric(label="Moyenne du CA", value=f"{mean_val}€", delta=mean_date)
        st.metric(
            label="Médiane du CA",
            value=f"{median_val}€",
            delta=median_date)

    # Create date inputs with the minimum and maximum dates as default values
    min_date = st.date_input(
        "Date de début",
        value=datetime.strptime(
            df["Date"].min(),
            "%Y-%m-%d"))
    min_date_formated = min_date.strftime("%Y-%m-%d")
    max_date = st.date_input(
        "Date de fin",
        value=datetime.strptime(
            df["Date"].max(),
            "%Y-%m-%d"))
    max_date_formated = max_date.strftime("%Y-%m-%d")
    if min_date > max_date:
        st.error("La date de début ne peut pas être supérieure à la date de fin.")
        st.stop()
    else:
        st.success(
            f"La date de début est {min_date_formated} et la date de fin est {max_date_formated}.")
        filtered_df = df[df["Date"].between(
            min_date_formated, max_date_formated)]
        min_val = filtered_df["Sales Revenue"].min().round(2)
        min_date = filtered_df.loc[filtered_df["Sales Revenue"].idxmin(
        )]["Date"]
        max_val = filtered_df["Sales Revenue"].max().round(2)
        max_date = filtered_df.loc[filtered_df["Sales Revenue"].idxmax(
        )]["Date"]
        mean_val = filtered_df["Sales Revenue"].mean().round(2)
        mean_date = filtered_df.iloc[filtered_df['Sales Revenue'].sub(
            mean_val).abs().idxmin()]["Date"]
        median_val = filtered_df["Sales Revenue"].median().round(2)
        median_date = filtered_df.iloc[filtered_df['Sales Revenue'].sub(
            median_val).abs().idxmin()]["Date"]
        col_r, col_l = st.columns(2)
        with col_l:
            st.metric(
                label="Minimum du CA",
                value=f"{min_val}€",
                delta=min_date)
            st.metric(
                label="Maximum du CA",
                value=f"{max_val}€",
                delta=max_date)
        with col_r:
            st.metric(
                label="Moyenne du CA",
                value=f"{mean_val}€",
                delta=mean_date)
            st.metric(
                label="Médiane du CA",
                value=f"{median_val}€",
                delta=median_date)


with tab3:
    st.markdown(
        "<h3 style='text-align: center;'>Choix de la fênetre</h3>",
        unsafe_allow_html=True)
    st.info("La fenêtre est le nombre de mois pour la comparaison, par exemple si vous choisissez 3, vous allez comparer les 3 derniers mois avec les 3 mois précédents")

    # Division de la page en deux colonnes
    window_size_str = st.number_input(
        "Entrez le nombre de mois pour la comparaison",
        min_value=1,
        value=3,
        step=1)
    try:
        window_size = int(window_size_str)
        if window_size <= 0:
            st.error("Veuillez entrer un nombre de mois valide (supérieur à zéro).")
            st.stop()
    except ValueError:
        st.error("Veuillez entrer un nombre entier de mois.")
        st.stop()

    fig = go.Figure()

    # Ajout du graphique de ligne pour les CA
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Sales Revenue"],
            mode='lines',
            name="CA",
            hovertemplate="CA: %{y}<extra></extra>"))

    # Ajout du graphique à barres pour la Évolution du CA
    growth_column_name = f"Évolution du CA ({window_size}-Période Fenêtre)"
    df[growth_column_name] = df['Sales Revenue'].diff(periods=window_size)
    bar_color = ['green' if diff >
                 0 else 'red' for diff in df[growth_column_name]]

    fig.add_trace(
        go.Bar(
            x=df["Date"],
            y=df[growth_column_name],
            name="Évolution du CA",
            marker_color=bar_color,
            hovertemplate=f"Évolution du CA: %{{y}}<br>Périodes: {df['Date'].iloc[0]} - {df['Date'].iloc[window_size]}<extra></extra>"))

    # Mise à jour du layout du graphique
    fig.update_layout(
        title="CA et Évolution du CA",
        xaxis_title="Date",
        yaxis_title="Valeur")
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Données')

        # Create a chart
        workbook = writer.book
        worksheet = writer.sheets['Données']
        chart = workbook.add_chart({'type': 'line'})

        # Configure the chart data
        chart.add_series({
            # Assuming 'Sales Revenue' is in column B
            'values': '=Données!$B$2:$B$' + str(len(df) + 1),
            # Assuming 'Date' is in column A
            'categories': '=Données!$A$2:$A$' + str(len(df) + 1),
            'name': 'CA',
        })

        # Insert the chart into the worksheet
        worksheet.insert_chart('D2', chart)

    excel_buffer.seek(0)

    # Téléchargement des résultats (graphique + données)
    st.download_button(
        label="Télécharger les résultats",
        data=excel_buffer,
        file_name="resultats.xlsx",
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
