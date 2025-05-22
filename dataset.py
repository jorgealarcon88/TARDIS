# %% [markdown]
# Initializes the StationData object by processing a given CSV DataFrame and filtering it by a date range.
# 
# - Filters out rows where the "Date" column is missing.
# - Keeps only the rows where the "Date" falls within the specified range (date[0] to date[1]).
# - Aggregates train data (scheduled, cancelled, and late trains) for each departure station.
# - Creates a DataFrame summarizing the total number of scheduled, cancelled, and late trains per station.
# - Stores this summarized data in self.df.

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

class StationData:
    def __init__(self, csv, date):
        data = {}
        newcsv = csv.dropna(subset = "Date")
        newcsv = newcsv[(newcsv["Date"] >= date[0]) & (newcsv["Date"] <= date[1])]
        for i in range(len(newcsv)):
            station = newcsv.iloc[i]["Departure station"]
            scheduled = newcsv.iloc[i]["Number of scheduled trains"]
            cancelled = newcsv.iloc[i]["Number of cancelled trains"]
            late = newcsv.iloc[i]["Number of trains delayed at departure"]

            if pd.notna(station) and pd.notna(scheduled) and pd.notna(cancelled) and pd.notna(late):
                if station not in data:
                    data[station] = [0, 0, 0]
                data[station][0] += scheduled
                data[station][1] += cancelled
                data[station][2] += late
        self.df = pd.DataFrame.from_dict(
            data, orient='index', columns=['Scheduled', 'Cancelled', 'Late']
        ).reset_index()
        self.df = self.df.rename(columns={'index': 'Departure station'})


# %% [markdown]
# Generates a horizontal bar chart showing the number of scheduled, cancelled, and late trains for a given list of stations.
# 
# - Filters the internal DataFrame to include only rows corresponding to the stations in station_list.
# - Removes all other stations by setting them to NaN and dropping them.
# - Plots three horizontal bars per station (Scheduled, Cancelled, Late) with different colors.
# - Customizes the chart with labels, a title, and a legend for clarity.
# - Displays the final plot.

# %%
def station_scheduled_late(self, station_list, lang="en"):
    df = self.df.copy()
    df.loc[~df["Departure station"].isin(station_list), "Departure station"] = np.nan
    df = df.dropna(subset=["Departure station"])
    
    pos = np.arange(len(df["Departure station"]))
    width = 0.5
    plt.figure(figsize=(10, 6))

    plt.barh(pos + width / 3, df["Late"], width / 3, color='#6baed6', label={'en': 'Late', 'fr': 'Retardés', 'es':'retardo'}[lang])
    plt.barh(pos, df["Scheduled"], width / 3, color='#c6dbef', label={'en': 'Scheduled', 'fr': 'Programmés', 'es': 'programado'}[lang])
    plt.barh(pos - width / 3, df["Cancelled"], width / 3, color='#2171b5', label={'en': 'Cancelled', 'fr': 'Annulés', 'es': 'annulado'}[lang])

    plt.yticks(pos, df["Departure station"])
    plt.xlabel({'en': "Number of Trains", 'fr': "Nombre de trains", 'es': "Nombre de traino"}[lang], fontsize=14)
    plt.title({'en': "Scheduled, Cancelled, and Late Trains per Station",
               'fr': "Trains programmés, annulés et en retard par gare",
               'es':"Traino programado, annulado y en retardo para garo"}[lang], fontsize=15)
    plt.legend()
    return plt

StationData.station_scheduled_late = station_scheduled_late


# %% [markdown]
# Initializes the LateData object by processing a CSV DataFrame containing train delay information within a specified date range.
# 
# - Filters out rows with missing "Date" values and retains only those within the provided date range.
# - Iterates through each row and aggregates delay-related data per departure station:
#     - Total number of trains delayed at arrival.
#     - Number of trains delayed more than 15, 30, and 60 minutes.
#     - Cumulative counts and delay cause percentages (if available) for each station.
# - Computes average delay percentages per station for various causes:
#     - Passenger handling
#     - Station management
#     - Rolling stock
#     - Traffic management
#     - Infrastructure
#     - External causes
# - Stores the cleaned and summarized data in self.df, dropping intermediate cumulative fields used for calculations.

# %%
class LateData():
    def __init__(self, csv, date):
        data = {}
        newcsv = csv.dropna(subset=["Date"])
        newcsv = newcsv[(newcsv["Date"] >= date[0]) & (newcsv["Date"] <= date[1])]
        for i in range(len(newcsv)):
            row = newcsv.iloc[i]
            station = row["Departure station"]
            trainlate = row["Number of trains delayed at arrival"]
            late15 = row["Number of trains delayed > 15min"]
            late30 = row["Number of trains delayed > 30min"]
            late60 = row["Number of trains delayed > 60min"]
            if pd.notna(station) and pd.notna(trainlate) and pd.notna(late15) and pd.notna(late30) and pd.notna(late60):
                if station not in data:
                    data[station] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                data[station][0] += trainlate
                data[station][1] += late15
                data[station][2] += late30
                data[station][3] += late60
                data[station][4] += 1
                if pd.notna(row.get("Total Pct", None)):
                    data[station][5] += row.get("Pct delay due to passenger handling (crowding, disabled persons, connections)", 0)
                    data[station][6] += row.get("Pct delay due to station management and equipment reuse", 0)
                    data[station][7] += row.get("Pct delay due to rolling stock", 0)
                    data[station][8] += row.get("Pct delay due to traffic management", 0)
                    data[station][9] += row.get("Pct delay due to infrastructure", 0)
                    data[station][10] += row.get("Pct delay due to external causes", 0)
        df = pd.DataFrame.from_dict(data, orient='index', 
            columns=[
                'trainlate', 'late15', 'late30', 'late60', 'count',
                'sum_passenger', 'sum_station', 'sum_stock', 
                'sum_management', 'sum_infra', 'sum_others'
            ]).reset_index().rename(columns={'index': 'station'})
        df["pct_passenger"] = df["sum_passenger"] / df["count"]
        df["pct_station"] = df["sum_station"] / df["count"]
        df["pct_stock"] = df["sum_stock"] / df["count"]
        df["pct_management"] = df["sum_management"] / df["count"]
        df["pct_infra"] = df["sum_infra"] / df["count"]
        df["pct_others"] = df["sum_others"] / df["count"]
        self.df = df.drop(columns=["count", "sum_passenger", "sum_station", "sum_stock", "sum_management", "sum_infra", "sum_others"])


# %% [markdown]
# Displays a stacked horizontal bar chart showing the distribution of train delay durations for a given list of stations.
# 
# - Filters the internal DataFrame to include only rows for the specified stations.
# - Calculates the number of trains delayed:
#     - Less than 15 minutes
#     - Between 15 and 30 minutes
#     - Between 30 and 60 minutes
#     - More than 60 minutes
# - Converts these counts into percentages of total delayed trains for each station.
# - Creates a stacked horizontal bar chart for each station to visualize delay duration categories.
# - Adds a legend and axis labels for clarity.

# %%
def late_train_duration(self, station_list, lang="en"):
    df = self.df.copy()
    df.loc[~df["station"].isin(station_list), "station"] = np.nan
    df = df.dropna(subset=["station"])
    
    df["total"] = df["trainlate"]
    df["late15_only"] = df["late15"] - df["late30"]
    df["late30_only"] = df["late30"] - df["late60"]
    df["late60_only"] = df["late60"]
    df["lateless15min"] = df["trainlate"] - df["late15"]
    
    df = df[df["total"] > 0]
    
    df["late15_pct"] = df["late15_only"] / df["total"] * 100
    df["late30_pct"] = df["late30_only"] / df["total"] * 100
    df["late60_pct"] = df["late60_only"] / df["total"] * 100
    df["lateless15min_pct"] = df["lateless15min"] / df["total"] * 100

    pos = np.arange(len(df["station"]))
    plt.figure(figsize=(10, 6))

    plt.barh(pos, df["lateless15min_pct"], color='#c6dbef', label={'en': 'Delay < 15 min', 'fr': 'Retard < 15 min', 'es': 'Retardo de < 15 min'}[lang])
    plt.barh(pos, df["late15_pct"], color='#9ecae1', label={'en': 'Delay ≥ 15 min', 'fr': 'Retard ≥ 15 min', 'es': 'Retardo de ≥ 15 min'}[lang], left=df["lateless15min_pct"])
    plt.barh(pos, df["late30_pct"], color='#6baed6', label={'en': 'Delay ≥ 30 min', 'fr': 'Retard ≥ 30 min', 'es': 'Retardo de ≥ 30 min'}[lang], left=df["lateless15min_pct"] + df["late15_pct"])
    plt.barh(pos, df["late60_pct"], color='#2171b5', label={'en': 'Delay ≥ 60 min', 'fr': 'Retard ≥ 60 min', 'es': 'Retardo de ≥ 60 min'}[lang], left=df["lateless15min_pct"] + df["late15_pct"] + df["late30_pct"])

    plt.yticks(pos, df["station"])
    plt.xlabel({'en': "Percentage of delayed trains (%)", 'fr': "Pourcentage de trains en retard (%)", 'es':"Pourcentago de traino en retardo (%)"}[lang], fontsize=14)
    plt.legend()
    return plt

LateData.late_train_data = late_train_duration


# %% [markdown]
# Displays a pie chart for each station in the provided list, showing the distribution of delay causes as percentages.
# 
# - Filters the internal DataFrame to include only the selected stations.
# - For each station:
#     - Retrieves average delay percentages by cause (passenger, station management, rolling stock, traffic management, infrastructure, external).
#     - Skips the station if all values are missing or zero.
#     - Displays a pie chart with the proportional contribution of each delay cause.
# - Adds labels, a title, and formatting for better readability.
# - Prints a message if no matching stations are found or if a station lacks delay cause data.

# %%
def late_train_pct(self, station_list, lang="en"):
    df = self.df.copy()
    df = df[df["station"].isin(station_list)]
    if df.empty:
        st.write({"en": "No matching station found in the data.",
                  "fr": "Aucune station correspondante dans les données.",
                  "es": "Nada de stationes correspondante en los donnéos."}[lang])
        return
    for _, row in df.iterrows():
        station = row["station"]
        x = [row["pct_passenger"], row["pct_station"], row["pct_stock"], row["pct_management"], row["pct_infra"], row["pct_others"]]
        if all(np.isnan(x)) or sum(x) == 0:
            st.write({
                "en": f"No delay cause data available for {station}.",
                "fr": f"Aucune donnée sur les causes de retard pour {station}.",
                "es": f"Nada donneo en la cosa de retardo para {station}."
            }[lang])
            continue
        
        labels = {
            "en": ["Passenger Delay", "Station Management", "Rolling Stock", "Traffic Management", "Infrastructure", "External"],
            "fr": ["Retard passagers", "Gestion gare", "Matériel roulant", "Gestion trafic", "Infrastructure", "Externe"],
            "es": ["Retardo passagero", "Gestiona del garo", "Matériel roulando", "Gestiona trafico", "Infrastructura", "External"]
        }[lang]
        
        colors = plt.get_cmap('Blues')(np.linspace(0, 1, len(x)))

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(
            x, labels=labels, colors=colors, autopct='%1.1f%%',
            wedgeprops={"linewidth": 1, "edgecolor": "white"},
            startangle=140
        )
        ax.set_title({
            "en": f"Distribution of Delay Causes for {station}",
            "fr": f"Répartition des causes de retard pour {station}",
            "es": f"Repartition de los cosas de retardo para {station}"
        }[lang])
        return fig

LateData.late_train_pct = late_train_pct


# %% [markdown]
# This init method filters the input DataFrame to keep only the rows where the "Arrival station" and "Departure station" match the specified values. It replaces unmatched stations with NaN and drops any rows with missing values in those columns. The cleaned DataFrame is then stored as an instance attribute.

# %%
import numpy as np

class Predict():
    def __init__(self, csv, arrival_station, departure_station):

        csv = csv.copy()
        csv.loc[~csv["Arrival station"].isin(arrival_station), "Arrival station"] = np.nan
        csv.loc[~csv["Departure station"].isin(departure_station), "Departure station"] = np.nan

        csv = csv.dropna(subset=["Arrival station", "Departure station"])

        self.csv = csv



# %% [markdown]
# Returns a list of unique arrival stations for the specified departure stations.
# 
# Parameters:
# csv (DataFrame): A pandas DataFrame containing at least 'Departure station' and 'Arrival station' columns.
# departure_stations (list): A list of station names to filter the 'Departure station' column.
# 
# Returns:
# list: Unique, non-null arrival stations corresponding to the given departure stations.

# %%
def arrival_station_list(csv, departure_stations):
    newcsv = csv.copy()
    newcsv.loc[~newcsv["Departure station"].isin(departure_stations), "Departure station"] = np.nan
    newcsv = newcsv.dropna(subset=["Departure station", "Arrival station"])
    arrival_list = []
    for station in newcsv["Arrival station"]:
        if station not in arrival_list:
            arrival_list.append(station)
    
    return arrival_list


# %% [markdown]
# This moy function calculates the mean (average) of a specified column, ignoring missing values. If the column contains no valid data, it returns 0.

# %%
def moy(self, type):
    total = 0
    csv = self.csv.dropna(subset = type)
    for i in csv[type]:
        total += i
    if len(csv[type]) != 0:
        return total / len(csv[type])
    return 0
Predict.moy = moy

# %% [markdown]
# Trains a 3rd-degree polynomial regression model between two variables in the dataset.
# 
# Parameters:
# - type1 (str): Name of the column to use as the independent variable (X).
# - type2 (str): Name of the column to use as the dependent variable (Y).
# 
# Process:
# 1. Copies the CSV dataset and drops rows with missing values in either column.
# 2. Separates the data into X (input) and Y (output).
# 3. Splits the data: uses 80% for training.
# 4. Fits a 3rd-degree polynomial regression model on the training data.
# 
# Returns:
# - An np.poly1d object representing the trained polynomial regression model, 
#     which can be used to make predictions.
# 

# %%
def model(self, type1, type2):

    csv = self.csv.copy()
    csv = csv.dropna(subset=[type1, type2])
    x = csv[type1]
    y = csv[type2]

    split_index = int(len(x) * 0.8)
    train_x = x[:split_index]
    train_y = y[:split_index]

    return np.poly1d(np.polyfit(train_x, train_y, 3))

Predict.model = model


# %% [markdown]
# Calculates the R² score (coefficient of determination) of a 3rd-degree polynomial regression 
# model trained on specified dataset columns.
# 
# Parameters:
# - type1 (str): Name of the column used as the independent variable (X).
# - type2 (str): Name of the column used as the dependent variable (Y).
# 
# Process:
# 1. Copies the dataset and removes rows with missing values in the specified columns.
# 2. Splits the data into X (input) and Y (output).
# 3. Splits data: 80% for training, 20% for testing.
# 4. Trains a 3rd-degree polynomial regression model on the training data.
# 5. Makes predictions on the test set.
# 6. Computes the R² score comparing predicted and actual test values.
# 
# Returns:
# - A float representing the R² score of the model (values close to 1 indicate a good fit).

# %%
from sklearn.metrics import r2_score

def r2(self, type1, type2):
    
    csv = self.csv.copy()
    csv = csv.dropna(subset=[type1, type2])
    x = csv[type1]
    y = csv[type2]

    split_index = int(len(x) * 0.8)
    train_x = x[:split_index]
    train_y = y[:split_index]
    test_x = x[split_index:]
    test_y = y[split_index:]

    model = np.poly1d(np.polyfit(train_x, train_y, 3))
    return r2_score(test_y, model(test_x))

Predict.r2 = r2

# %% [markdown]
# Calculates the Root Mean Squared Error (RMSE) of a 3rd-degree polynomial regression 
# model between two dataset columns.
# 
# Parameters:
# - type1 (str): Name of the column used as the independent variable (X).
# - type2 (str): Name of the column used as the dependent variable (Y).
# 
# Process:
# 1. Copies the dataset and drops rows with missing values in the specified columns.
# 2. Extracts X and Y values.
# 3. Splits data: 80% for training, 20% for testing.
# 4. Trains a 3rd-degree polynomial regression model on the training data.
# 5. Predicts on the test set.
# 6. Calculates the RMSE between actual and predicted test values.
# 
# Returns:
# - A float representing the RMSE of the model (lower values indicate better predictions).

# %%
from sklearn.metrics import mean_squared_error

def rmse(self, type1, type2):

    csv = self.csv.copy()
    csv = csv.dropna(subset=[type1, type2])
    x = csv[type1]
    y = csv[type2]

    split_index = int(len(x) * 0.8)
    train_x = x[:split_index]
    train_y = y[:split_index]
    test_x = x[split_index:]
    test_y = y[split_index:]

    model = np.poly1d(np.polyfit(train_x, train_y, 3))
    return np.sqrt(mean_squared_error(test_y, model(test_x)))

Predict.rmse = rmse

# %% [markdown]
# Plots a polynomial regression of specified degree between two columns of a DataFrame, 
# showing training data, test data, and the regression curve.
# 
# Parameters:
# - df (pd.DataFrame): The DataFrame containing the data.
# - col_x (str): Name of the column to use as the independent variable (x-axis).
# - col_y (str): Name of the column to use as the dependent variable (y-axis).
# - degree (int, optional): Degree of the polynomial regression (default is 3).
# - lang (str, optional): Language code for labels ('en', 'fr', 'es'). Default is 'en'.
# 
# Process:
# 1. Removes rows with missing values in the specified columns.
# 2. Splits the data into training set (80%) and test set (20%).
# 3. Trains a polynomial regression model of the specified degree on the training data.
# 4. Plots training points in blue, test points in orange, and the regression curve in red.
# 5. Displays titles, axis labels, and legends in the selected language.
# 6. Uses Streamlit to display the plot.
# 
# Returns:
# - The plot is return.

# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def plot_poly_model(df, col_x, col_y, degree=3, lang="en"):
    translations = {
        "title": {
            "en": f'Polynomial regression (degree {degree}) for Number of scheduled trains vs Number of trains delayed at departure',
            "fr": f'Régression polynomiale (degré {degree}) pour le nombre de trains prévus en fonction du nombre de trains en retard au départ',
            "es": f'Régression polynomiala (degréo {degree}) para el nombre de traios prévudo en fonctionas du nombre de traino en retardo al départo'
        },
        "xlabel": {
            "en": col_x,
            "fr": "nombre de trains prévus",
            "es": "nombre de traios prévudo"

        },
        "ylabel": {
            "en": col_y,
            "fr": "nombre de trains en retard au départ",
            "es": "nombre de trainos en retardo al départo"

        },
        "train_label": {
            "en": "Train data",
            "fr": "Données entraînement",
            "es": "Donnéos entraînemente"

        },
        "test_label": {
            "en": "Test data",
            "fr": "Données test",
            "es": "Donnéos testo"

        },
        "poly_label": {
            "en": f'Poly degree {degree}',
            "fr": f'Degré poly {degree}',
            "es": f'Degréo poly {degree}'
        }
    }

    data = df.dropna(subset=[col_x, col_y])
    
    x = data[col_x].values
    y = data[col_y].values

    split_idx = int(len(x) * 0.8)
    train_x, train_y = x[:split_idx], y[:split_idx]
    test_x, test_y = x[split_idx:], y[split_idx:]

    model = np.poly1d(np.polyfit(train_x, train_y, degree))
    
    x_line = np.linspace(min(x), max(x), 300)
    y_line = model(x_line)
    
    plt.figure(5)
    plt.scatter(train_x, train_y, color='blue', label=translations["train_label"][lang])
    plt.scatter(test_x, test_y, color='orange', label=translations["test_label"][lang])
    plt.plot(x_line, y_line, color='red', linewidth=2, label=translations["poly_label"][lang])
    
    plt.title(translations["title"][lang])
    plt.xlabel(translations["xlabel"][lang])
    plt.ylabel(translations["ylabel"][lang])
    plt.legend()
    plt.grid(True)

    return plt


