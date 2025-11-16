# Stock Market Analysis Platform

This project is a data analytics platform for analyzing stock market data. It includes functionalities for data ingestion, processing, technical analysis, predictive modeling, and visualization, now accessible via a Flask web application.

## Project Structure

```
.
├── data/                 # Directory for storing downloaded stock data
├── notebooks/            # Directory for Jupyter notebooks for exploratory analysis
├── src/                  # Source code directory
│   ├── __init__.py
│   ├── data_ingestion/     # Scripts for downloading data
│   │   ├── __init__.py
│   │   └── download_data.py
│   ├── data_processing/    # Scripts for data cleaning and preprocessing
│   │   ├── __init__.py
│   │   └── process_data.py
│   ├── modeling/           # Scripts for building and training models
│   │   ├── __init__.py
│   │   └── train_model.py
│   ├── technical_analysis/ # Scripts for calculating technical indicators
│   │   ├── __init__.py
│   │   └── indicators.py
│   └── visualization/      # Scripts for plotting and visualization
│       ├── __init__.py
│       └── plot_data.py
├── templates/            # HTML templates for the Flask web application
│   ├── base.html
│   ├── index.html
│   ├── top_movers.html
│   └── recommendations.html
├── app.py                # Flask web application entry point
├── main.py               # Main script to run the analysis pipeline
├── update_data.py        # Script to update data for the web application
├── requirements.txt      # Project dependencies
└── README.md             # This file
```

## Getting Started

### Prerequisites

*   Python 3.8 or higher
*   pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd stockmarketanalysis
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Analysis Pipeline (CLI)

To run the full analysis pipeline for a specific stock, use the `main.py` script.

```bash
python main.py --ticker <STOCK_TICKER> --start_date <YYYY-MM-DD> --end_date <YYYY-MM-DD>
```

**Example:**

```bash
python main.py --ticker AAPL --start_date 2020-01-01
```

This will:
1.  Download the historical data for the specified ticker.
2.  Preprocess the data.
3.  Calculate technical indicators.
4.  Train a simple predictive model.
5.  Display visualizations of the data and model predictions.

### Running the Web Application (Flask)

1.  **First, update the data for the web application:**
    ```bash
    python update_data.py
    ```
    This script downloads the latest data for market indices, popular stocks, and recommendation stocks.

2.  **Then, start the Flask development server:**
    ```bash
    python app.py
    ```
    The application will typically run on `http://127.0.0.1:5000/`. Open this URL in your web browser.

### Automating Daily Data Updates

To keep the web application's data fresh, you should run the `update_data.py` script daily. You can automate this using your operating system's task scheduler:

*   **Linux/macOS (using Cron):**
    1.  Open your crontab editor: `crontab -e`
    2.  Add a line like the following to run the script daily at a specific time (e.g., 3:00 AM):
        ```cron
        0 3 * * * /usr/bin/python /path/to/your/stockmarketanalysis/update_data.py >> /path/to/your/stockmarketanalysis/update_log.log 2>&1
        ```
        *Replace `/usr/bin/python` with the path to your Python interpreter (preferably within your virtual environment) and `/path/to/your/stockmarketanalysis/` with the actual path to your project directory.*

*   **Windows (using Task Scheduler):**
    1.  Open Task Scheduler (search for it in the Start menu).
    2.  Click "Create Basic Task..." and follow the wizard.
    3.  **Trigger:** Set it to "Daily" and choose a time.
    4.  **Action:** Select "Start a program".
    5.  **Program/script:** Enter the full path to your Python executable (e.g., `C:\Users\YourUser\stockmarketanalysis\venv\Scripts\python.exe`).
    6.  **Add arguments (optional):** Enter the full path to your `update_data.py` script (e.g., `C:\Users\YourUser\stockmarketanalysis\update_data.py`).
    7.  Finish the wizard.

## Disclaimer

The stock recommendations provided by this platform are based on simple technical analysis and should not be considered financial advice. Always conduct your own research and consult with a financial professional before making any investment decisions.