import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dataset import StationData as sdt

csv = pd.read_csv("cleaned_dataset.csv")

# Initialized state at 'home'
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Switch window
def go_to(page_name):
    st.session_state.page = page_name

# Every "render" functions define a window to show datas
def render_subpageA():
    st.title(f"📄 First graph")
    newcsv = csv.dropna(subset = "Number of trains delayed at arrival")
    newcsv = newcsv.dropna(subset = "Number of scheduled trains")
    x = newcsv["Number of scheduled trains"]
    y = newcsv["Number of trains delayed at arrival"]
    train_x = x[:(int)(len(newcsv) * (80 / 100))]
    train_y = y[:(int)(len(newcsv) * (80 / 100))]
    test_x = x[(int)(len(newcsv) * (80 / 100)):]
    test_y = y[(int)(len(newcsv) * (80 / 100)):]
    scheduled_delayedarr = np.poly1d(np.polyfit(train_x, train_y, 3))
    plt.scatter(x, y)
    st.pyplot(plt)
    st.button("⬅️ Retour à l'accueil", on_click=go_to, args=('home',))

def render_subpageB():
    st.title(f"📄 Test Stations")
    choices = st.multiselect("Select station(s)",
                ["AIX EN PROVENCE TGV",
               "ANGERS SAINT LAUD",
               "ANGOULEME",
               "ANNECY",
               "ARRAS",
               "AVIGNON TGV",
               "BARCELONA",
               "BELLEGARDE (AIN)",
               "BESANCON FRANCHE COMTE TGV",
               "BORDEAUX ST JEAN",
               "BREST",
               "CHAMBERY CHALLES LES EAUX",
               "DIJON VILLE",
               "DOUAI", 
               "DUNKERQUE", 
               "FRANCFORT", 
               "GENEVE", 
               "GRENOBLE", 
               "ITALIE", 
               "LA ROCHELLE VILLE", 
               "LAUSANNE", 
               "LAVAL", 
               "LE CREUSOT MONTCEAU MONTCHANIN", 
               "LE MANS", 
               "LILLE", 
               "LYON PART DIEU", 
               "MACON LOCHE", 
               "MADRID", 
               "MARNE LA VALLEE", 
               "MARSEILLE ST CHARLES", 
               "METZ", 
               "MONTPELLIER", 
               "MULHOUSE VILLE", 
               "NANCY", 
               "NANTES", 
               "NICE VILLE", 
               "NIMES", 
               "PARIS EST", 
               "PARIS LYON", 
               "PARIS MONTPARNASSE", 
               "PARIS NORD", 
               "PARIS VAUGIRARD", 
               "PERPIGNAN", 
               "POTIIERS", 
               "QUIMPER", 
               "REIMS", 
               "RENNES", 
               "SAINT ETIENNE CHATEAUCREUX", 
               "ST MALO", 
               "ST PIERRE DES CORPS", 
               "STRASBOURG", 
               "STUTTGART", 
               "TOULON", 
               "TOULOUSE MATABIAU", 
               "TOURCOING", 
               "TOURS", 
               "VALENCE ALIXAN TGV", 
               "VANNES", 
               "ZURICH"])
    st.write(f"Your selection is : {choices}")
    st.button("⬅️ Retour à l'accueil", on_click=go_to, args=('home',))

def render_subpageC():
    st.title(f"📄 Test Date")
    start_date, end_date = st.select_slider(
        "Select the dates that you want to know",
        options=[
            "2018-01",
            "2018-12",
            "2019-01",
            "2019-12",
            "2020-01",
            "2020-12",
            "2021-01",
            "2021-12",
            "2022-01",
            "2022-12",
            "2023-01",
            "2023-12",
            "2024-01",
            "2024-12",
        ],
        value=("2018-01", "2024-01"),
    )
    choices = st.multiselect("Select station(s)",
                ["AIX EN PROVENCE TGV",
               "ANGERS SAINT LAUD",
               "ANGOULEME",
               "ANNECY",
               "ARRAS",
               "AVIGNON TGV",
               "BARCELONA",
               "BELLEGARDE (AIN)",
               "BESANCON FRANCHE COMTE TGV",
               "BORDEAUX ST JEAN",
               "BREST",
               "CHAMBERY CHALLES LES EAUX",
               "DIJON VILLE",
               "DOUAI", 
               "DUNKERQUE", 
               "FRANCFORT", 
               "GENEVE", 
               "GRENOBLE", 
               "ITALIE", 
               "LA ROCHELLE VILLE", 
               "LAUSANNE", 
               "LAVAL", 
               "LE CREUSOT MONTCEAU MONTCHANIN", 
               "LE MANS", 
               "LILLE", 
               "LYON PART DIEU", 
               "MACON LOCHE", 
               "MADRID", 
               "MARNE LA VALLEE", 
               "MARSEILLE ST CHARLES", 
               "METZ", 
               "MONTPELLIER", 
               "MULHOUSE VILLE", 
               "NANCY", 
               "NANTES", 
               "NICE VILLE", 
               "NIMES", 
               "PARIS EST", 
               "PARIS LYON", 
               "PARIS MONTPARNASSE", 
               "PARIS NORD", 
               "PARIS VAUGIRARD", 
               "PERPIGNAN", 
               "POTIIERS", 
               "QUIMPER", 
               "REIMS", 
               "RENNES", 
               "SAINT ETIENNE CHATEAUCREUX", 
               "ST MALO", 
               "ST PIERRE DES CORPS", 
               "STRASBOURG", 
               "STUTTGART", 
               "TOULON", 
               "TOULOUSE MATABIAU", 
               "TOURCOING", 
               "TOURS", 
               "VALENCE ALIXAN TGV", 
               "VANNES", 
               "ZURICH"])
    dates = [start_date, end_date]
    data = sdt(csv, dates)
    data.station_scheduled_late(choices)
    st.write(f"You selected this period :", dates[0], ",", dates[1])
    st.button("⬅️ Retour à l'accueil", on_click=go_to, args=('home',))

def render_subpageD():
    st.title(f"📄 Page D")
    st.write(f"Bienvenue sur la page Page D !")
    st.button("⬅️ Retour à l'accueil", on_click=go_to, args=('home',))

def render_subpageE():
    st.title(f"📄 Page E")
    st.write(f"Bienvenue sur la page Page E !")
    st.button("⬅️ Retour à l'accueil", on_click=go_to, args=('home',))

def render_subpageF():
    st.title(f"📄 Page F")
    st.write(f"Bienvenue sur la page Page F !")
    st.button("⬅️ Retour à l'accueil", on_click=go_to, args=('home',))

# Print home page
def home():
    st.title("🏠 Welcome to home page")
    st.subheader("Choose the window you want to access")

    buttons = [
        ("Page A", "pageA"),
        ("Page B", "pageB"),
        ("Page C", "pageC"),
        ("Page D", "pageD"),
        ("Page E", "pageE"),
        ("Page F", "pageF"),
    ]
    for i in range(0, len(buttons), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(buttons):
                title, page = buttons[i + j]
                with cols[j]:
                    st.subheader(title)
                    st.button(f"Accéder à {title}", on_click=go_to, args=(page,))

# Call functions when state change
def main():
    if st.session_state.page == 'home':
        home()
    elif st.session_state.page == 'pageA':
        render_subpageA()
    elif st.session_state.page == 'pageB':
        render_subpageB()
    elif st.session_state.page == 'pageC':
        render_subpageC()
    elif st.session_state.page == 'pageD':
        render_subpageD()
    elif st.session_state.page == 'pageE':
        render_subpageE()
    elif st.session_state.page == 'pageF':
        render_subpageF()
main()

# Données importantes :
# - Nombre de trains en retard en fonction du nombre de trains prévus
# ==> Camembert pour les causes des retards possibles
# - Nombre de trains en retard de 15 min en fonction du nombre de train en retard
# - Nombre de trains en fonctions des dates

# Graphes à intégrer :
# - Un graphe montrant les données imortantes, pas forcément beau mais très utile
# - Un camembert pour décrire les causes des retards
# - Une map intéractive qui montre les retards en fonction des gares sur un carte de france
# - 