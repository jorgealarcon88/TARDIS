import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dataset import StationData as sdt
from dataset import Predict as pred
from dataset import LateData as ld
from dataset import arrival_station_list as asl
from dataset import plot_poly_model as ppm


csv = pd.read_csv("cleaned_dataset.csv")

# Initialized state at 'home'
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Switch window
def go_to(page_name):
    st.session_state.page = page_name

station_list = ["AIX EN PROVENCE TGV",
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
               "ZURICH"]

date_list = ["2018-01",
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
            "2024-12"]

# Every "render" functions define a window to show datas
def render_subpageA():
    st.set_page_config(page_title="Journey datas")
    st.title(f"⏰ Journey datas")
    start_date, end_date = st.select_slider(
        "Select the dates that you want to know",
        options=date_list,
        value=("2018-01", "2024-12"),
    )
    choices = st.multiselect("Select station(s)",
                station_list)
    dates = [start_date, end_date]
    data = sdt(csv, dates)
    late_data = ld(csv, dates)
    if (len(choices) > 10 or len(choices) == 0):
        st.write("You have to select a number of station between 1 and 10")
    else:
        data.station_scheduled_late(choices)
        late_data.late_train_data(choices)
        station = st.selectbox("Select only one station to know the reasons of the late", choices)
        late_data.late_train_pct([station])
    st.button("🏠 Return home page", on_click=go_to, args=('home',))

def render_subpageB():
    st.set_page_config(page_title="Predictions")
    st.title("🔮 Predictions")
    st.write("Welcome to predictions page !")
    departure = st.selectbox("Select a departure station", station_list)
    arrival = st.selectbox("Select an arrival station", asl(csv, [departure]))
    predict = pred(csv, [departure], [arrival])
    average = predict.moy("Average journey time")
    nb_trains = predict.moy("Number of scheduled trains")
    model = predict.model("Number of scheduled trains", "Number of trains delayed at departure")
    r2 = predict.r2("Number of scheduled trains", "Number of trains delayed at departure")
    rmse = predict.rmse("Number of scheduled trains", "Number of trains delayed at departure")
    st.subheader("The predictions are :")
    st.write(f"- The travel time will be approximately {int(average)}min on average.")
    st.write(f"- There is an average of {int(nb_trains)} scheduled trains, {int(model(nb_trains))} (±{int(rmse)}) of them are delayed at departure.")
    if r2 < 1 and r2 > -1:
        st.write(f"This information is {int(abs(r2) * 100)}% accurate")
    else:
        st.write(f"This data may be inaccurate or implausible.")
    ppm(predict.csv, "Number of scheduled trains", "Number of trains delayed at departure")
    st.button("🏠 Return home page", on_click=go_to, args=('home',))

# This page is a bonus, to show users' reviews
def render_subpageC():
    st.title("⭐ Users' reviews")
    st.write("Welcome to users' reviews page !")
    st.button("🏠 Return home page", on_click=go_to, args=('home',))
    st.write("<br><br><br><br><br><br><br><br><br><br><br><h5 style='text-align: center;'>Credit:<br> LOUVEL Roméo<br> LAGUNA Gaël<br> LEFEVRE Alexandre</h5>", unsafe_allow_html=True)
# Print home page
def home():
    st.title("🏠 Welcome to home page")
    st.subheader("Choose the window you want to access")

    # List of all page
    buttons = [
        ("Journey datas", "pageA"),
        ("Predictions", "pageB"),
        ("Users' reviews", "pageC"),
    ]
    # Create columns from the number of elements
    cols = st.columns(len(buttons))
    for col, (title, page) in zip(cols, buttons):
        with col:
            st.subheader(title)
            st.button(f"Access {title}", on_click=go_to, args=(page,))

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
main()

# Pour le LateData :
# - Initialiser avec (csv, [date1, date2])
# - Pour avoir le graph des retards moyens ("late_train_duration"), envoyer une liste de stations
# - Les raisons des retard ("late_train_pcp"), envoyer une seule station
#   parmi celles déjà selectionées

# Pour le predict:
# - Initialiser avec (csv, [station arrivé], [station départ])
# - Pour les station d'arrivé dispo ("arrival_station_list"), envoyer une (csv, station)
# - ".moy" --> Donne la moyenne d'un type de data trouvé dans cleaned_dataset.csv (ex: durée)
# - ".data(2 type de data)"
# ==> Récupère :
# ".model" --> courbe des datas
# ".rmse" --> Valeur de + ou - pour la précision
# ".r2" --> Taux de véracité entre 0 et 1 convertible en % en faisant x 100