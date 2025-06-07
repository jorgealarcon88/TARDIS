import streamlit as st
import pandas as pd
import requests

city_metro_prices = {
    "Paris": 2.15,
    "Lyon": 2.00,
    "Marseille": 1.80,
    "Lille": 1.80,
    "Toulouse": 1.80,
    "Rennes": 1.70,
    "Bordeaux": 1.80,
    "Strasbourg": 1.90,
    "Nantes": 1.80,
    "Nice": 1.70,
    "Montpellier": 1.60,
    "Grenoble": 1.80
}

# Dictionnaire de traductions
translations = {
    "fr": {
        "title": "✈️ Planificateur d'activités",
        "activity": "Activité",
        "auto_price": "Estimer prix",
        "duration": "Durée",
        "half_day": "½ journée",
        "full_day": "1 journée",
        "estimated_price": "💰 Prix estimé",
        "price": "Prix (€)",
        "add": "Ajouter",
        "registered_activities": "📋 Activités enregistrées",
        "metro_tickets": "🎟️ Nombre de ticket de métro",
        "summary_title": "✅ Résumé des activités sélectionnées",
        "total_activities": "💰 **Total activités :**",
        "total_metro": "➕ **Ticket de métro :**",
        "total_final": "🔢 **Total final :**",
        "total_duration": "⏱️ **Durée totale:**",
        "delete_selected": "🗑️ Supprimer la sélection",
        "add_activities_first": "Ajoutez des activités pour commencer.",
        "return_home": "🏠 Retour à la page d'accueil",
        "ticket_price": "💸 prix du ticket",
        "select_city": "🌍 Ville",
        "cities": {
            "Paris": "Paris",
            "Lyon": "Lyon",
            "Marseille": "Marseille",
            "Lille": "Lille",
            "Toulouse": "Toulouse",
            "Rennes": "Rennes",
            "Bordeaux": "Bordeaux",
            "Strasbourg": "Strasbourg",
            "Nantes": "Nantes",
            "Nice": "Nice",
            "Montpellier": "Montpellier",
            "Grenoble": "Grenoble",
            "Barcelone": "Barcelona",
            "Madrid": "Madrid",
            "Bruxelles": "Brussels",
            "Londres": "London"
        }
    },
    "es": {
        "title": "🇦🇩 Planificator del activita",
        "activity": "Activita",
        "auto_price": "Estimar prio",
        "duration": "Duréo",
        "half_day": "½ journéo",
        "full_day": "1 journéo",
        "estimated_price": "💶 Prio estimado",
        "price": "Prio (€)",
        "add": "Ajoutar",
        "registered_activities": "🏖️ Activitas enregistréeo",
        "metro_tickets": "🍹 Nombre de sangria",
        "summary_title": "😎 Résuméo de los activitas sélectionnar",
        "total_activities": "💶 **Totalo activitéo :**",
        "total_metro": "🍹 **Totalo de sangria:**",
        "total_final": "⚽ **Total de finale :**",
        "total_duration": "☀️ **Total de duréo :**",
        "delete_selected": "🍊 Supprimar la sélection",
        "add_activities_first": "Ajoutar los activitas para commencar.",
        "return_home": "🇲🇽 Retoura à la pago de accueila",
        "ticket_price": "🍹 prio de la sangria",
        "select_city": "🌍 Cudad",
        "cities": {
            "Paris": "Paris",
            "Lyon": "Lyon",
            "Marseille": "Marseille",
            "Lille": "Lille",
            "Toulouse": "Toulouse",
            "Rennes": "Rennes",
            "Bordeaux": "Bordeaux",
            "Strasbourg": "Strasbourg",
            "Nantes": "Nantes",
            "Nice": "Nice",
            "Montpellier": "Montpellier",
            "Grenoble": "Grenoble",
            "Barcelone": "Barcelona",
            "Madrid": "Madrid",
            "Bruxelles": "Brussels",
            "Londres": "London"
        }
    },
    "en": {
        "title": "✈️ Activity Planner",
        "activity": "Activity",
        "auto_price": "Estimate price",
        "duration": "Duration",
        "half_day": "½ day",
        "full_day": "1 day",
        "estimated_price": "💰 Estimated price",
        "price": "Price (€)",
        "add": "Add",
        "registered_activities": "📋 Registered Activities",
        "metro_tickets": "🎟️ Number of metro tickets",
        "summary_title": "✅ Summary of selected activities",
        "total_activities": "💰 **Total activities :**",
        "total_metro": "➕ **Metro tickets :**",
        "total_final": "🔢 **Final total :**",
        "total_duration": "⏱️ **Total duration :**",
        "delete_selected": "🗑️ Delete selected",
        "add_activities_first": "Add activities to get started.",
        "return_home": "🏠 Return to home page",
        "ticket_price": "💸 ticket price",
        "select_city": "🌍 City",
        "cities": {
            "Paris": "Paris",
            "Lyon": "Lyon",
            "Marseille": "Marseille",
            "Lille": "Lille",
            "Toulouse": "Toulouse",
            "Rennes": "Rennes",
            "Bordeaux": "Bordeaux",
            "Strasbourg": "Strasbourg",
            "Nantes": "Nantes",
            "Nice": "Nice",
            "Montpellier": "Montpellier",
            "Grenoble": "Grenoble",
            "Barcelone": "Barcelona",
            "Madrid": "Madrid",
            "Bruxelles": "Brussels",
            "Londres": "London"
        }
    }
}

CSV_FILE = "activities.csv"

def charger_activites():
    try:
        df = pd.read_csv(CSV_FILE)
        if df.empty:
            return []
        return df.to_dict(orient="records")
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return []

def sauvegarder_activites(activites):
    columns = ["name", "price", "duration"]
    df = pd.DataFrame(activites, columns=columns)
    df.to_csv(CSV_FILE, index=False)

def go_to(page_name):
    st.session_state.page = page_name

def chat_with_ollama(prompt, model="llama3:8b", system="You are a travel planner for Paris"):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Erreur communication Ollama : {e}"

def estimer_prix_avec_ollama(nom_activite: str) -> float:
    prompt = (
        f"Give a realistic estimate in euros for the following activity: {nom_activite}."
        "Respond with a number only."
    )
    reponse = chat_with_ollama(prompt)
    try:
        estimation_str = reponse.strip()
        estimation = float(''.join(c for c in estimation_str if c in "0123456789.,").replace(",", "."))
        return estimation
    except Exception:
        st.error(f"Impossible d'extraire un nombre de la réponse Ollama : {reponse}")
        return 0.0

def planner_page(lang):
    t = translations[lang]

    st.title(t["title"])

    if "activities" not in st.session_state:
        st.session_state.activities = charger_activites()

    # Sélection de la ville avec traduction
    translated_city_names = [t["cities"][city] for city in city_metro_prices.keys()]
    translated_to_original = {t["cities"][k]: k for k in city_metro_prices.keys()}
    selected_translated_city = st.selectbox(t["select_city"], translated_city_names, key="selected_city")
    selected_city = translated_to_original[selected_translated_city]

    # Met à jour automatiquement le prix du ticket si la ville change
    if "last_selected_city" not in st.session_state or st.session_state.last_selected_city != selected_city:
        st.session_state.metro_price = city_metro_prices[selected_city]
        st.session_state.last_selected_city = selected_city

    with st.form("add_activity"):
        col1, col2, col3 = st.columns([3, 1, 2])
        with col1:
            name = st.text_input(t["activity"])
        with col2:
            auto_price = st.checkbox(t["auto_price"])
        with col3:
            duration_label = st.selectbox(t["duration"], [t["half_day"], t["full_day"]])
        duration = 0.5 if duration_label == t["half_day"] else 1.0

        price = 0.0
        if auto_price and name:
            price = estimer_prix_avec_ollama(name)
            st.write(f"{t['estimated_price']} : {price:.2f} €")
        else:
            price = st.number_input(t["price"], min_value=0.0, step=1.0, key="price_input")

        submitted = st.form_submit_button(t["add"])
        if submitted and name:
            st.session_state.activities.append({
                "name": name,
                "price": price,
                "duration": duration
            })
            sauvegarder_activites(st.session_state.activities)

    st.subheader(t["registered_activities"])
    selected_indexes = []

    col_ticket, col_price = st.columns([2, 1])
    with col_ticket:
        ticket_metro = st.number_input(t["metro_tickets"], min_value=0, step=1, key="ticket_metro")
    with col_price:
        st.session_state.metro_price = st.number_input(
            f"{t['ticket_price']}",
            min_value=0.0,
            step=0.1,
            value=st.session_state.metro_price
        )

    if st.session_state.activities:
        for i, act in enumerate(st.session_state.activities):
            cols = st.columns([4, 2, 2, 1])
            with cols[0]:
                st.write(act["name"])
            with cols[1]:
                new_price = st.number_input(
                    f"{t['price']}",
                    min_value=0.0,
                    step=1.0,
                    value=act["price"],
                    key=f"price_edit_{i}"
                )
            with cols[2]:
                default_index = 0 if act["duration"] == 0.5 else 1
                new_duration_label = st.selectbox(
                    f"{t['duration']}",
                    [t["half_day"], t["full_day"]],
                    index=default_index,
                    key=f"duration_{i}"
                )
            with cols[3]:
                checked = st.checkbox("✓", key=f"select_{i}")
                if checked:
                    selected_indexes.append(i)

            if new_price != act["price"]:
                st.session_state.activities[i]["price"] = new_price
                sauvegarder_activites(st.session_state.activities)

            new_duration = 0.5 if new_duration_label == t["half_day"] else 1.0
            if new_duration != act["duration"]:
                act["duration"] = new_duration
                sauvegarder_activites(st.session_state.activities)

        if selected_indexes:
            st.markdown(f"### {t['summary_title']}")
            selected_data = [st.session_state.activities[i] for i in selected_indexes]
            df = pd.DataFrame(selected_data)

            total_price_activities = df["price"].sum()
            total_duration = df["duration"].sum()
            total_price_metro = ticket_metro * st.session_state.metro_price
            total_price_final = total_price_activities + total_price_metro

            st.success(f"{t['total_activities']} {total_price_activities:.2f} €")
            st.success(f"{t['total_metro']} {total_price_metro:.2f} €")
            st.success(f"{t['total_final']} {total_price_final:.2f} €")
            st.success(f"{t['total_duration']} {total_duration} jour{'s' if total_duration > 1 else ''}")

            if st.button(t["delete_selected"]):
                for i in sorted(selected_indexes, reverse=True):
                    st.session_state.activities.pop(i)
                    sauvegarder_activites(st.session_state.activities)
                st.rerun()
    st.button(t["return_home"], on_click=go_to, args=("home",))
