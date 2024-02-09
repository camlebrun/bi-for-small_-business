import streamlit as st


# Affichage du mode d'emploi
st.markdown(
    """
## Mode d'emploi de l'application de comparaison de chiffre d'affaires

### Introduction
Bienvenue dans l'application de comparaison de chiffre d'affaires ! Cette application vous permet de comparer le chiffre d'affaires entre deux années différentes et de visualiser les résultats sous forme de graphique. Vous pouvez également télécharger les données et le graphique au format Excel pour une utilisation ultérieure.

### Utilisation
1. **Sélectionnez les années et les chiffres d'affaires :**
   - Dans les zones de saisie prévues à cet effet, entrez les années de référence et actuelle, ainsi que les chiffres d'affaires correspondants.
   - Assurez-vous que l'année de référence est inférieure à l'année actuelle.

2. **Réglez les seuils pour les catégories de croissance :**
   - Utilisez les curseurs dans la barre latérale pour définir les seuils pour les différentes catégories de taux de croissance.

3. **Cliquez sur le bouton "Comparer" :**
   - Après avoir entré les données et réglé les seuils, cliquez sur le bouton "Comparer" pour obtenir l'analyse.

4. **Analysez les résultats :**
   - Les résultats s'affichent sous forme de message coloré indiquant la catégorie de croissance ou de déclin du chiffre d'affaires.
   - Un graphique montrant la comparaison du chiffre d'affaires entre les deux années est également affiché.

5. **Téléchargez les résultats :**
   - Si vous le souhaitez, vous pouvez télécharger les données et le graphique au format Excel en cliquant sur le bouton "Télécharger les résultats".

### Remarques
- Assurez-vous d'entrer des chiffres d'affaires valides et des années dans les plages autorisées.
- Utilisez les seuils de catégories de croissance pour personnaliser l'analyse en fonction de vos besoins.
- Le téléchargement des résultats vous permet d'enregistrer les données et les graphiques pour une utilisation ultérieure ou pour les partager avec d'autres parties prenantes.
"""
)
