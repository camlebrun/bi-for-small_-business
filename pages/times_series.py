import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="Comparaison des Revenus de Vente", page_icon=":bar_chart:", layout="wide")

# Titre de l'application
st.title("Comparaison des Revenus de Vente")

# Importer un fichier CSV ou Excel
dataframe = st.file_uploader(label="Importer un Fichier", type=['.csv', '.xlsx'])

if dataframe is not None:
    st.write("Fichier importé avec succès")
    df = pd.read_csv(dataframe) if dataframe.name.endswith('.csv') else pd.read_excel(dataframe)
    
    # Division de la page en deux colonnes
    param_l, param_r = st.columns(2)
    
    # Colonne gauche : Entrée de la taille de la fenêtre
    with param_l:
        window_size_str = st.text_input("Entrez le nombre de mois pour la taille de la fenêtre")
        try:
            window_size = int(window_size_str)
            if window_size <= 0:
                st.error("Veuillez entrer un nombre de mois valide (supérieur à zéro).")
                st.stop()
        except ValueError:
            st.error("Veuillez entrer un nombre entier de mois.")
            st.stop()

    # Colonne droite : Affichage du paramètre de la fenêtre sélectionnée
    with param_r:
        st.write("Paramètres de la fenêtre sélectionnée:", window_size)

    # Division de la page en deux colonnes
    left, right = st.columns(2)

    # Colonne gauche : Affichage du dataframe

    st.dataframe(df, use_container_width=True)

    # Colonne droite : Affichage du graphique

    fig = go.Figure()

    # Ajout du graphique de ligne pour les revenus de vente
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Sales Revenue"], mode='lines', name="Revenus de Vente",
                                hovertemplate="Revenus de Vente: %{y}<extra></extra>"))

    # Ajout du graphique à barres pour la croissance périodique
    growth_column_name = f"Croissance Périodique ({window_size}-Période Fenêtre)"
    df[growth_column_name] = df['Sales Revenue'].diff(periods=window_size)
    bar_color = ['green' if diff > 0 else 'red' for diff in df[growth_column_name]]

    fig.add_trace(go.Bar(x=df["Date"], y=df[growth_column_name], name="Croissance Périodique",
                            marker_color=bar_color,
                            hovertemplate=f"Croissance Périodique: %{{y}}<br>Périodes: {df['Date'].iloc[0]} - {df['Date'].iloc[window_size]}<extra></extra>"))

    # Mise à jour du layout du graphique
    fig.update_layout(title="Revenus de Vente et Croissance Périodique", xaxis_title="Date", yaxis_title="Valeur")
    st.plotly_chart(fig, use_container_width=True)

else:
    # Affichage d'une erreur si aucun fichier n'est importé
    st.error("Veuillez importer un fichier valide")
