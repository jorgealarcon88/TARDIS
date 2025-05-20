import streamlit as st
st.set_page_config(page_title="Train Dashboard", page_icon="🚄", layout="centered")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from dataset import StationData as sdt
from dataset import Predict as pred
from dataset import LateData as ld
from dataset import arrival_station_list as asl
from dataset import plot_poly_model as ppm
from pathlib import Path

file_path = Path("cleaned_dataset.csv")

try:
    if file_path.exists() and file_path.stat().st_size > 0:
        csv = pd.read_csv(file_path)
    elif file_path.stat().st_size == 0:
        csv = None
        st.error("The dataset is empty. Please check the contents of 'cleaned_dataset.csv'.")
    else:
        csv = None
        st.warning("The cleaned dataset could not be found. Please make sure the file 'cleaned_dataset.csv' exists.")
except pd.errors.ParserError:
    csv = None
    st.error("There was an error parsing the dataset. Please ensure 'cleaned_dataset.csv' is correctly formatted.")
except Exception as e:
    csv = None
    st.error(f"An unexpected error occurred while loading the dataset: {str(e)}")

if 'page' not in st.session_state:
    st.session_state.page = 'home'

def go_to(page_name):
    st.session_state.page = page_name

station_list = ["AIX EN PROVENCE TGV", "ANGERS SAINT LAUD", "ANGOULEME", "ANNECY", "ARRAS", "AVIGNON TGV", "BARCELONA",
                "BELLEGARDE (AIN)", "BESANCON FRANCHE COMTE TGV", "BORDEAUX ST JEAN", "BREST", "CHAMBERY CHALLES LES EAUX",
                "DIJON VILLE", "DOUAI", "DUNKERQUE", "FRANCFORT", "GENEVE", "GRENOBLE", "ITALIE", "LA ROCHELLE VILLE",
                "LAUSANNE", "LAVAL", "LE CREUSOT MONTCEAU MONTCHANIN", "LE MANS", "LILLE", "LYON PART DIEU", "MACON LOCHE",
                "MADRID", "MARNE LA VALLEE", "MARSEILLE ST CHARLES", "METZ", "MONTPELLIER", "MULHOUSE VILLE", "NANCY",
                "NANTES", "NICE VILLE", "NIMES", "PARIS EST", "PARIS LYON", "PARIS MONTPARNASSE", "PARIS NORD",
                "PARIS VAUGIRARD", "PERPIGNAN", "POTIIERS", "QUIMPER", "REIMS", "RENNES", "SAINT ETIENNE CHATEAUCREUX",
                "ST MALO", "ST PIERRE DES CORPS", "STRASBOURG", "STUTTGART", "TOULON", "TOULOUSE MATABIAU", "TOURCOING",
                "TOURS", "VALENCE ALIXAN TGV", "VANNES", "ZURICH"]

date_list = ["2018-01", "2018-12", "2019-01", "2019-12", "2020-01", "2020-12", "2021-01", "2021-12", "2022-01",
             "2022-12", "2023-01", "2023-12", "2024-01", "2024-12"]

def render_subpageA():
    st.title("\u23F0 Journey datas")
    if csv is None:
        st.error("Unable to display journey data because the dataset is not available.")
        return

    start_date, end_date = st.select_slider("Select the dates that you want to know", options=date_list, value=("2018-01", "2024-12"))
    choices = st.multiselect("Select station(s)", station_list)
    dates = [start_date, end_date]

    try:
        data = sdt(csv, dates)
        late_data = ld(csv, dates)

        if len(choices) > 10 or len(choices) == 0:
            st.warning("You have to select a number of station between 1 and 10")
        else:
            data.station_scheduled_late(choices)
            late_data.late_train_data(choices)
            station = st.selectbox("Select only one station to know the reasons of the late", choices)
            late_data.late_train_pct([station])
    except Exception as e:
        st.error(f"An error occurred while processing journey data: {str(e)}")

    st.button("\U0001F3E0 Return to home page", on_click=go_to, args=('home',))

def render_subpageB():
    st.title("\U0001F52E Predictions")
    if csv is None:
        st.error("Unable to display predictions because the dataset is not available.")
        return

    try:
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
        hours = average // 60
        minutes = average % 60

        st.markdown(f"""
        - The travel time will be approximately <span style='color:#2171b5'><b>{int(hours)} h {int(minutes)} min</b></span> on average.  
        - There is an average of <span style='color:#2171b5'><b>{int(nb_trains)}</b></span> scheduled trains, 
        <span style='color:#2171b5'><b>{int(model(nb_trains))}</b></span> (±<span style='color:#2171b5'><b>{int(rmse)}</b></span>) of them are delayed at departure.
        """, unsafe_allow_html=True)

        if -1 < r2 < 1:
            st.markdown(f"<i>This information is <span style='color:#2171b5'><b>{int(abs(r2) * 100)}%</b></span> accurate</i>", unsafe_allow_html=True)
        else:
            st.warning("This data may be inaccurate or implausible.")

        ppm(predict.csv, "Number of scheduled trains", "Number of trains delayed at departure")
    except Exception as e:
        st.error(f"An error occurred while generating predictions: {str(e)}")

    st.button("\U0001F3E0 Return to home page", on_click=go_to, args=('home',))

def render_subpageC():
    st.title("\u2B50 Users' reviews")
    st.write("Welcome to users' reviews page !")
    st.button("\U0001F3E0 Return to home page", on_click=go_to, args=('home',))
    st.write("""<br><br><br><br><br><br><br><br><br><br><br>
        <h5 style='text-align: center;'>Credit:<br> LOUVEL Roméo<br> LAGUNA Gaël<br> LEFEVRE Alexandre</h5>""", unsafe_allow_html=True)

def home():
    st.title("\U0001F3E0 Welcome to home page")

    if csv is None:
        st.warning("The cleaned dataset is not available. Please ensure it is uploaded and correctly formatted.")
        return

    st.subheader("Choose the window you want to access")
    buttons = [
        ("Journey datas", "pageA"),
        ("Predictions", "pageB"),
        ("Users' reviews", "pageC"),
    ]
    cols = st.columns(len(buttons))
    for col, (title, page) in zip(cols, buttons):
        with col:
            st.subheader(title)
            st.button(f"Access {title}", on_click=go_to, args=(page,))

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
