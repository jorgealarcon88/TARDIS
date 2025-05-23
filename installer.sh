#!/bin/bash

sudo apt install python3
sudo apt install jupyter

jupyter nbconvert --to script tardis_eda.ipynb
python3 tardis_eda.py

python3 -m venv .venv

source .venv/bin/activate
pip install -r requirements.txt

streamlit run tardis_dashboard.py