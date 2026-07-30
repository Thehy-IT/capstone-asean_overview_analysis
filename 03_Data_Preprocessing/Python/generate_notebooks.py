import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ANALYSIS_DIR = os.path.join(BASE_DIR, "04_Analysis")

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
        "country_df = pd.read_csv(os.path.join(cleaned_dir, 'Dim_Country.csv'))\n",
        "indicator_df = pd.read_csv(os.path.join(cleaned_dir, 'Dim_Indicator.csv'))\n",
        "date_df = pd.read_csv(os.path.join(cleaned_dir, 'Dim_Date.csv'))\n",
        "\n",
        "print('Fact Indicators Shape:', fact_df.shape)\n",
        "print('Dim Country Shape:', country_df.shape)\n",
        "print('Dim Indicator Shape:', indicator_df.shape)\n",
        "print('Dim Date Shape:', date_df.shape)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Summary Statistics & Record Counts per Country"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [
        "merged_df = fact_df.merge(country_df, on='CountryCode').merge(indicator_df, on='SeriesCode')\n",
        "print('Domain Distribution:')\n",
        "print(merged_df['Domain'].value_counts())\n",
        "\n",
        "print('\\nCountry Record Counts:')\n",
        "print(merged_df['CountryName'].value_counts())"
      ]
    }
  ],
  "metadata": {
    "language_info": { "name": "python" }
  },
  "nbformat": 4,
  "nbformat_minor": 2
}

# 2. BUILD Statistics.ipynb
stats_nb = {
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "# Statistical Analysis - ASEAN Development Metrics\n",
        "**Project:** Capstone ASEAN Overview Analysis (2015-2025)\n",
        "\n",
        "Statistical descriptive analysis, growth rate computations, and cross-indicator insights."
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
        "indicator_df = pd.read_csv(os.path.join(cleaned_dir, 'Dim_Indicator.csv'))\n",
        "\n",
        "# GDP Analysis (NY.GDP.MKTP.CD)\n",
        "gdp_df = fact_df[fact_df['SeriesCode'] == 'NY.GDP.MKTP.CD']\n",
        "print('GDP Summary Statistics (USD):')\n",
        "print(gdp_df['Value'].describe())"
      ]
    }
  ],
  "metadata": {
    "language_info": { "name": "python" }
  },
  "nbformat": 4,
  "nbformat_minor": 2
}

with open(os.path.join(ANALYSIS_DIR, "EDA.ipynb"), "w", encoding="utf-8") as f:
    json.dump(eda_nb, f, indent=2)

with open(os.path.join(ANALYSIS_DIR, "Statistics.ipynb"), "w", encoding="utf-8") as f:
    json.dump(stats_nb, f, indent=2)

print("EDA.ipynb and Statistics.ipynb created successfully!")
