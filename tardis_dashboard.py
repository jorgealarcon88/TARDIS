import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from dataset import StationData as sdt
from dataset import Predict as pred
from dataset import LateData as ld
from dataset import arrival_station_list as asl
from dataset import plot_poly_model as ppm

# --- Traductions (avec emojis) ---
translations = {
    "en": {
        "title": "🚄 Train Dashboard",
        "journey_data": "⏰ Journey data",
        "predictions": "🔮 Predictions",
        "users_reviews": "⭐ Users' reviews",
        "welcome_home": "🏠 Welcome to home page",
        "choose_window": "Choose the window you want to access",
        "select_dates": "Select the dates that you want to know",
        "select_stations": "Select station(s)",
        "select_station": "Select only one station to know the reasons of the late",
        "number_station_warning": "You have to select a number of station between 1 and 10",
        "dataset_missing": "Unable to display data because the dataset is not available.",
        "return_home": "🏠 Return to home page",
        "average_travel_time": "The travel time will be approximately",
        "scheduled_trains": "scheduled trains",
        "delayed_trains": "of them are delayed at departure",
        "accuracy_info": "This information is {pct}% accurate",
        "accuracy_warning": "This data may be inaccurate or implausible.",
        "error_processing_data": "An error occurred while processing journey data: {err}",
        "error_generating_predictions": "An error occurred while generating predictions: {err}",
        "select_departure": "Select a departure station",
        "select_arrival": "Select an arrival station",
        "predictions_welcome": "Welcome to predictions page !",
        "users_reviews_welcome": "Welcome to users' reviews page !",
        "col1": "Name",
        "col2": "Review before SNCP",
        "col3": "Review after SNCP",
        "col4": "Comment",
        "noé": "Noé Roberties",
        "lucas": "Lucas Scheffknecht",
        "marc": "Marc Grioche",
        "pavel": "Pavel de Wavrechin",
        "ugo": "Ugo Blanc",
        "nolhan": "Nolhan Scheinder",
        "juan": "Juan Pablo",
        "titouan": "Titouan Nguyen-dai",
        "groot": "Groot",
        "steve jobs": "Steve Jobs",
        "com1": "Very good transport company, worth using",
        "com2": "If I were a train, I'd want to be this one",
        "com3": "No complaints, the journey was perfect",
        "com4": "I recommend traveling with SNCP",
        "com5": "Awesome deer spotted along the way",
        "com6": "I was able to finish my Wolf3D during the trip. Very happy!",
        "com7": "My wife became happy thanks to SNCP. THANK YOU",
        "com8": "I'm too good-looking, but let's keep that a secret",
        "com9": "I'm Groot",
        "com10": "I'm very happy to have come up with new business ideas thanks to this trip",
        "credit": "Credit:<br> LOUVEL Roméo<br> LAGUNA Gaël<br> LEFEVRE Alexandre",
    },
    "fr": {
        "title": "🚄 données des trains",
        "journey_data": "⏰ Données",
        "predictions": "🔮 Prédictions",
        "users_reviews": "⭐ Avis utilisateurs",
        "welcome_home": "🏠 Bienvenue sur la page d'accueil",
        "choose_window": "Choisissez la fenêtre à accéder",
        "select_dates": "Sélectionnez les dates que vous souhaitez consulter",
        "select_stations": "Sélectionnez la ou les gares",
        "select_station": "Sélectionnez une seule gare pour connaître les causes des retards",
        "number_station_warning": "Vous devez sélectionner entre 1 et 10 gares",
        "dataset_missing": "Impossible d'afficher les données car les données sont indisponibles.",
        "return_home": "🏠 Retour à la page d'accueil",
        "average_travel_time": "Le temps de trajet sera d'environ",
        "scheduled_trains": "trains prévus",
        "delayed_trains": "d'entre eux sont en retard au départ",
        "accuracy_info": "Cette information est précise à {pct}%",
        "accuracy_warning": "Ces données peuvent être inexactes ou peu plausibles.",
        "error_processing_data": "Une erreur est survenue lors du traitement des données : {err}",
        "error_generating_predictions": "Une erreur est survenue lors de la génération des prédictions : {err}",
        "select_departure": "Sélectionnez une gare de départ",
        "select_arrival": "Sélectionnez une gare d'arrivée",
        "predictions_welcome": "Bienvenue sur la page des prédictions !",
        "users_reviews_welcome": "Bienvenue sur la page des avis utilisateurs !",
        "col1": "Nom",
        "col2": "Note avant la SNCP",
        "col3": "Note après la SNCP",
        "col4": "Commentaire",
        "noé": "Noé Roberties",
        "lucas": "Lucas Scheffknecht",
        "marc": "Marc Grioche",
        "pavel": "Pavel de Wavrechin",
        "ugo": "Ugo Blanc",
        "nolhan": "Nolhan Scheinder",
        "juan": "Juan Pablo",
        "titouan": "Titouan Nguyen-dai",
        "groot": "Groot",
        "steve jobs": "Steve Jobs",
        "com1": "Très bonne compagnie de transport, à utiliser",
        "com2": "Si j'avais été un train, j'aurais voulu être celui-ci",
        "com3": "Rien à dire, le trajet était parfait",
        "com4": "Je recommande de voyager avec la SNCP",
        "com5": "Super chevreuil croisé en chemin",
        "com6": "J'ai pu finir mon Wolf3d pendant le trajet. Très heureux !",
        "com7": "Ma femme est devenu heureuse grâce à la SNCP. MERCI",
        "com8": "Je suis tros beau mais il ne faut pas le dire",
        "com9": "Je s'appelle Groot",
        "com10": "Je suis très heureux d'avoir eu de nouvelles idées de business grâce à se trajet",
        "credit": "Crédit:<br> LOUVEL Roméo<br> LAGUNA Gaël<br> LEFEVRE Alexandre",
    },
     "es": {
        "title": "🇲🇽 donnéa del traino",
        "journey_data": "💃 Donnéas",
        "predictions": "🤠 Prédicta",
        "users_reviews": "🌯 utilisators Avio",
        "welcome_home": "🇲🇽 Bienvenido en la pago de accueila",
        "choose_window": "Selectionar la fenêtra para accédar",
        "select_dates": "Sélectionnar los dateos que vos souhaitos consultar",
        "select_stations": "Sélectionnar la o los garos",
        "select_station": "Sélectionnar una uniqua garo para connaîtrar los causeas del retardo",
        "number_station_warning": "Vosotros devos sélectionnar entre 1 y 10 garos",
        "dataset_missing": "Impossiblé d'affichar los donnéos car el de donnéos esta indisponiblé.",
        "return_home": "🇲🇽 Retoura à la pago de accueila",
        "average_travel_time": "El tiempo de trajero esta de environ",
        "scheduled_trains": "traino prévos",
        "delayed_trains": "de entro os sontos en retardé al départo",
        "accuracy_info": "Esta information esta précisementé al {pct}%",
        "accuracy_warning": "Esta donnéos puedo êstar inexacto o not mas plausiblé.",
        "error_processing_data": "Una erreura esta survenido durante el traitemento de los donnéos : {err}",
        "error_generating_predictions": "Una erreura esta survenido durante la générationa de la prédiction : {err}",
        "select_departure": "Sélectionnar une garo de départo",
        "select_arrival": "Sélectionnar una garo d'arrivado",
        "predictions_welcome": "Bienvenido en la pago des prédiction !",
        "users_reviews_welcome": "Bienvenido en la pago des avido utilisators !",
        "col1": "Nombre",
        "col2": "Nota avanto la SNCP",
        "col3": "Nota aprèso la SNCP",
        "col4": "Commentairo",
        "noé": "Noéo Roberto",
        "lucas": "Lucos Scheffknechto",
        "marc": "Marco Briocho",
        "pavel": "El rey del mundo",
        "ugo": "Ugo Blanco",
        "nolhan": "Brr Brr Patapim",
        "juan": "Juan Pablo",
        "titouan": "Titouan Nguyen-dai",
        "groot": "Grooto",
        "steve jobs": "Steve Jobs",
        "com1": "Muy bien tajecto",
        "com2": "Donde esta Balerina Cappucina ?",
        "com3": "Que calor en el traino",
        "com4": "Perfecto transporto en communo",
        "com5": "Que se paso ? Olden paso ? No no josé",
        "com6": "Puedo jugar la musica porque soy un DJ",
        "com7": "Ma famme devenido heureusa con esto trajecto. GRACIAS",
        "com8": "Soy perfecto, pero no habla de este",
        "com9": "Soy Groot",
        "com10": "Beaucoupo des ideas devenidos reales en este trajecto",
        "credit": "\"Una rondonta sin fuente se pasa de frente !\"<br>"
        "Crédito:<br> LOUVELO Roméoo<br> LAGUNO Gaëllo<br> LEFEVRO Alexandro",
    }
}

# --- Chargement dataset ---
file_path = Path("cleaned_dataset.csv")
try:
    if file_path.exists() and file_path.stat().st_size > 0:
        csv = pd.read_csv(file_path)
    elif file_path.exists() and file_path.stat().st_size == 0:
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

# --- Config page ---
st.set_page_config(page_title="Train Dashboard", page_icon="🚄", layout="wide")  # <-- layout wide pour responsive

# --- Langue ---
lang = st.sidebar.selectbox("Select Language / Choisir la langue", options=["en", "fr", "es"], index=1)

# --- Navigation ---
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
                "PARIS VAUGIRARD", "PERPIGNAN", "POITIERS", "QUIMPER", "REIMS", "RENNES", "SAINT ETIENNE CHATEAUCREUX",
                "ST MALO", "ST PIERRE DES CORPS", "STRASBOURG", "STUTTGART", "TOULON", "TOULOUSE MATABIAU", "TOURCOING",
                "TOURS", "VALENCE ALIXAN TGV", "VANNES", "ZURICH"]

date_list = ["2018-01", "2018-12", "2019-01", "2019-12", "2020-01", "2020-12", "2021-01", "2021-12", "2022-01",
             "2022-12", "2023-01", "2023-12", "2024-01", "2024-12"]

def render_subpageA():
    st.title(translations[lang]["journey_data"])
    if csv is None:
        st.error(translations[lang]["dataset_missing"])
        return
    start_date, end_date = st.select_slider(translations[lang]["select_dates"], options=date_list, value=("2018-01", "2024-12"))
    choices = st.multiselect(translations[lang]["select_stations"], station_list)
    dates = [start_date, end_date]
    try:
        data = sdt(csv, dates)
        late_data = ld(csv, dates)

        if len(choices) > 10 or len(choices) == 0:
            st.warning(translations[lang]["number_station_warning"])
        else:
            data.station_scheduled_late(choices, lang)
            late_data.late_train_data(choices, lang)
            station = st.selectbox(translations[lang]["select_station"], choices)
            late_data.late_train_pct([station], lang)
    except Exception as e:
        st.error(translations[lang]["error_processing_data"].format(err=str(e)))
    st.button(translations[lang]["return_home"], on_click=go_to, args=('home',))

def render_subpageB():
    st.title(translations[lang]["predictions"])
    if csv is None:
        st.error(translations[lang]["dataset_missing"])
        return
    try:
        st.write(translations[lang]["predictions_welcome"])
        departure = st.selectbox(translations[lang]["select_departure"], station_list)
        arrival = st.selectbox(translations[lang]["select_arrival"], asl(csv, [departure]))
        predict = pred(csv, [departure], [arrival])

        average = predict.moy("Average journey time")
        nb_trains = predict.moy("Number of scheduled trains")
        model = predict.model("Number of scheduled trains", "Number of trains delayed at departure")
        r2 = predict.r2("Number of scheduled trains", "Number of trains delayed at departure")
        rmse = predict.rmse("Number of scheduled trains", "Number of trains delayed at departure")

        st.subheader(translations[lang]["average_travel_time"])
        hours = average // 60
        minutes = average % 60

        st.markdown(f"""
        - {translations[lang]['average_travel_time']} <span style='color:#2171b5'><b>{int(hours)} h {int(minutes)} min</b></span> {translations[lang]['scheduled_trains']},  
        - <span style='color:#2171b5'><b>{int(nb_trains)}</b></span> {translations[lang]['scheduled_trains']}, 
        <span style='color:#2171b5'><b>{int(model(nb_trains))}</b></span> (±<span style='color:#2171b5'><b>{int(rmse)}</b></span>) {translations[lang]['delayed_trains']}.
        """, unsafe_allow_html=True)

        if -1 < r2 < 1:
            st.markdown(f"<i>{translations[lang]['accuracy_info'].format(pct=int(abs(r2)*100))}</i>", unsafe_allow_html=True)
        else:
            st.warning(translations[lang]["accuracy_warning"])

        ppm(predict.csv, "Number of scheduled trains", "Number of trains delayed at departure",3 ,lang)  # ta fonction d'origine

    except Exception as e:
        st.error(translations[lang]["error_generating_predictions"].format(err=str(e)))

    st.button(translations[lang]["return_home"], on_click=go_to, args=('home',))

def render_subpageC():
    st.title(translations[lang]["users_reviews"])
    st.write(translations[lang]["users_reviews_welcome"])
    data = pd.DataFrame({
        translations[lang]["col1"]: [translations[lang]["noé"], translations[lang]["lucas"], translations[lang]["marc"],
                translations[lang]["pavel"], translations[lang]["ugo"], translations[lang]["nolhan"],
                translations[lang]["juan"], translations[lang]["titouan"], translations[lang]["groot"],
                translations[lang]["steve jobs"]],
        translations[lang]["col2"]: ["3⭐", "1⭐", "4⭐", "1⭐", "2⭐", "1⭐", "0⭐", "1⭐", "4⭐", "2⭐"],
        translations[lang]["col3"]: ["5⭐", "5⭐", "5⭐", "5⭐", "5⭐", "5⭐", "5⭐", "5⭐", "5⭐", "5⭐"],
        translations[lang]["col4"]: [translations[lang]["com1"], translations[lang]["com2"], translations[lang]["com3"],
                translations[lang]["com4"], translations[lang]["com5"], translations[lang]["com6"],
                translations[lang]["com7"], translations[lang]["com8"], translations[lang]["com9"],
                translations[lang]["com10"]]
    })
    st.dataframe(data)
    st.button(translations[lang]["return_home"], on_click=go_to, args=('home',))
    st.markdown(f"<br><br><br><br><br><br><br><br><br><br><br><h5 style='text-align:center;'>{translations[lang]['credit']}</h5>", unsafe_allow_html=True)

def home():
    st.title(translations[lang]["welcome_home"])
    if csv is None:
        st.warning(translations[lang]["dataset_missing"])
        return

    st.subheader(translations[lang]["choose_window"])
    buttons = [
        (translations[lang]["journey_data"], "pageA"),
        (translations[lang]["predictions"], "pageB"),
        (translations[lang]["users_reviews"], "pageC"),
    ]
    cols = st.columns(len(buttons))
    for col, (title, page) in zip(cols, buttons):
        with col:
            st.subheader(title)
            st.button(f"{'Access' if lang == 'en' else 'Accéder à' if lang == 'fr' else 'Accedar a'} {title}", on_click=go_to, args=(page,))

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