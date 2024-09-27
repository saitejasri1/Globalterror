# Comprehensive Terrorism Data Analysis Dashboard

## Overview
This project is a Streamlit-based dashboard for visualizing and analyzing global terrorism data. It provides interactive visualizations across multiple dimensions of terrorist activities, including temporal trends, geospatial patterns, attack characteristics, perpetrator profiles, and success/failure rates.
![Dashboard Screenshot](/Users/saitejasriyerramsetti/Documents/Globalterror/terror.png)
## Features

### 1. Temporal Analysis
- Trend of terrorist attacks over time
- Casualty trends analysis
- Pre- and post-major event comparisons (e.g., 9/11)
- Seasonal trend identification

### 2. Geospatial Analysis
- Regional hotspots identification
- Geopolitical trend visualization
- Geospatial clustering of terrorism "hot zones"
- Geographic distribution of attack types

### 3. Attack Type and Weapon Analysis
- Analysis of attack methods (e.g., bombings, assassinations, armed assaults)
- Weapon type trends over time and regions
- Success rates and casualty outcomes by attack method

### 4. Perpetrator and Target Analysis
- Profiles of most active terrorist groups
- Temporal patterns of group activities
- Target type frequency analysis (e.g., military, civilians, government)
- Cross-analysis of target types with attack success and casualty rates

### 5. Success/Failure Rates of Attacks
- Success rate trends over time
- Comparative analysis of success rates across attack types
- Factors influencing attack success (e.g., region, perpetrator group, weapon type)

## Requirements
- Python 3.7+
- Streamlit
- Plotly
- Dask
- Pandas
- NumPy
- Plotly-geo

For a complete list of dependencies, see `requirements.txt`.

## Setup
1. Clone this repository:
   ```
   git clone [your-repo-url]
   cd [your-repo-name]
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Ensure your dataset is in the correct location:
   `/Users/saitejasriyerramsetti/Documents/Globalterror/success_failure_data.csv`
   
   Or update the file path in the `load_data()` function in each script.

## Usage
To run the main dashboard:
```
streamlit run app.py
```

Navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

## Dashboard Components

### Temporal Analysis
- Time series plot of attack frequency
- Casualty trend visualization
- Comparative analysis tool for pre/post major events

### Geospatial Analysis
- Interactive world map with attack hotspots
- Regional comparison charts
- Geospatial distribution of attack types

### Attack and Weapon Analysis
- Attack method frequency charts
- Weapon type trend analysis
- Success rate comparison by attack method

### Perpetrator and Target Analysis
- Top terrorist groups by activity level
- Target type breakdown
- Group activity timeline

### Success/Failure Analysis
- Success rate trends over time
- Success rate by attack type, region, and perpetrator group
- Factors influencing attack success

## Data Source
[Provide detailed information about your data source here, including any necessary citations or acknowledgments]

## Project Structure
```
project/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Project dependencies
├── README.md               # This file
│
├── data/
│   └── success_failure_data.csv   # Main dataset
│
├── scripts/
│   ├── temporal_analysis.py       # Temporal analysis functions
│   ├── geospatial_analysis.py     # Geospatial analysis functions
│   ├── attack_analysis.py         # Attack and weapon analysis functions
│   ├── perpetrator_analysis.py    # Perpetrator and target analysis functions
│   └── success_analysis.py        # Success/failure analysis functions
│
└── utils/
    ├── data_loader.py             # Data loading and preprocessing utilities
    └── visualization_helpers.py   # Helper functions for creating visualizations
```

## Contributing
Contributions to improve the dashboard are welcome. Please feel free to submit a Pull Request or open an Issue for discussion.

## License
[Your chosen license]

## Authors
- Saitejasri Yerramsetti

## Contact
[Your contact information]

## Acknowledgments
[Any acknowledgments or credits you want to include]

---

Note: This project deals with sensitive data about global terrorism. Please use and interpret the visualizations responsibly and in the appropriate context. The goal of this dashboard is to provide insights for academic, policy, and security purposes, not to sensationalize or promote any ideology.