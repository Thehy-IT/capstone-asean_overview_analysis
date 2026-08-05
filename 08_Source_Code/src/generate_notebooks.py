import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ANALYSIS_DIR = os.path.join(BASE_DIR, "04_Analysis")

os.makedirs(ANALYSIS_DIR, exist_ok=True)

# 1. BUILD EDA.ipynb
eda_nb = {
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "# Exploratory Data Analysis (EDA) - ASEAN Overview Analysis\n",
        "**Project:** Capstone ASEAN Overview Analysis (2015-2025)\n",
        "\n",
        "This notebook explores the cleaned datasets generated in `02_Data/Cleaned`."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [
        "import pandas as pd\n",
        "import os\n",
        "\n",
        "cleaned_dir = '../02_Data/Cleaned'\n",
        "fact_df = pd.read_csv(os.path.join(cleaned_dir, 'Fact_ASEAN_Indicators.csv'))\n",
        "dim_country = pd.read_csv(os.path.join(cleaned_dir, 'Dim_Country.csv'))\n",
        "dim_indicator = pd.read_csv(os.path.join(cleaned_dir, 'Dim_Indicator.csv'))\n",
        "dim_date = pd.read_csv(os.path.join(cleaned_dir, 'Dim_Date.csv'))\n",
        "\n",
        "print('=== FACT INDICATORS HEAD ===')\n",
        "display(fact_df.head())\n",
        "print(f'Total Fact Records: {len(fact_df)}')\n"
      ]
    }
  ],
  "metadata": {
    "language_info": { "name": "python" }
  },
  "nbformat": 4,
  "nbformat_minor": 2
}

def generate():
    eda_path = os.path.join(ANALYSIS_DIR, "EDA.ipynb")
    with open(eda_path, mode='w', encoding='utf-8') as f:
        json.dump(eda_nb, f, indent=2)
    print(f"Generated notebook: {eda_path}")

if __name__ == "__main__":
    generate()
