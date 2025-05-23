# TARDIS Train Dashboard

The TARDIS Train Dashboard is a data analysis and visualization tool designed to process, clean, and analyze train delay data. It provides insights into train schedules, delays, and their causes, and offers predictive modeling for future delays. The project is implemented using Python, leveraging libraries like Pandas, NumPy, and Streamlit for data processing and visualization.

---

## Table of Contents

1. [Approach](#approach)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Project Structure](#project-structure)

---

## Approach

The project is divided into three main components:

1. **Data Cleaning and Preprocessing**:
   - Implemented in [`tardis_eda.ipynb`](tardis_eda.ipynb), this notebook processes the raw dataset (`dataset.csv`) by:
     - Removing invalid or inconsistent data (e.g., negative values, non-numeric entries).
     - Cleaning specific columns like "Number of scheduled trains," "Average delay," and "Percentage delays due to various causes."
     - Using Levenshtein's algorithm to correct station names and services with typos.
     - Generating a cleaned dataset (`cleaned_dataset.csv`) for further analysis.

2. **Data Analysis and Visualization**:
   - Implemented in [`tardis_dashboard.py`](tardis_dashboard.py), this Streamlit-based application provides:
     - Interactive visualizations of train schedules, delays, and their causes.
     - Predictive modeling for train delays based on historical data.
     - Multilingual support (English, French, and Spanish) for user interaction.

3. **Predictive Modeling**:
   - Implemented in [`tardis_model.ipynb`](tardis_model.ipynb), this notebook:
     - Trains polynomial regression models to predict delays based on historical data.
     - Visualizes the relationship between scheduled trains and delayed trains.
     - Provides metrics like RMSE and R² for model evaluation.

---

## Installation

Follow these steps to set up the project:

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.8+ installed. Install the required packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare the Dataset**:
   - Place the raw dataset (`dataset.csv`) in the `assets/` directory.
   - Run the data cleaning notebook [`tardis_eda.ipynb`](tardis_eda.ipynb) to generate `cleaned_dataset.csv`.

---

## Usage

### 1. **Run the Dashboard**:
   Launch the Streamlit dashboard to explore and analyze the data:
   ```bash
   streamlit run tardis_dashboard.py
   ```

   The dashboard provides the following features:
   - **Journey Data**: Visualize train schedules and delays.
   - **Predictions**: Predict future delays based on departure and arrival stations.
   - **User Reviews**: View user feedback on train services.

### 2. **Train Predictive Models**:
   Open [`tardis_model.ipynb`](tardis_model.ipynb) in Jupyter Notebook to:
   - Train polynomial regression models.
   - Evaluate model performance using RMSE and R² metrics.

### 3. **Analyze Data**:
   Use [`tardis_eda.ipynb`](tardis_eda.ipynb) to:
   - Explore the raw dataset.
   - Clean and preprocess data for analysis.

---

## Project Structure

```
assets/
    dataset.csv          # Raw dataset
img/
    ...                  # Images used in the dashboard
requirements.txt         # Python dependencies
tardis_dashboard.py      # Streamlit dashboard implementation
tardis_eda.ipynb         # Data cleaning and preprocessing notebook
tardis_model.ipynb       # Predictive modeling notebook
```

---
