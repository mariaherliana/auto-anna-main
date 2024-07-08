# app.py
from flask import Flask, render_template
import pandas as pd
from src.csv_processing import process_console_csv, process_dashboard_csv, save_merged_csv
from src.CallDetail import CallDetail
from src.idn_area_codes import EMERGENCY_NUMBERS, PHONE_PREFIXES, INTERNATIONAL_PHONE_PREFIXES
from src.utils import parse_jakarta_datetime, convert_to_jakarta_time_iso, call_hash, classify_number, format_datetime_as_human_readable, format_timedelta, format_username, parse_call_memo, parse_iso_datetime
from src.FileConfig import Config, Files

app = Flask(__name__)

@app.route('/')
def index():
    # Extract the client name from the first Files object in the CONFIG list
    client_name = CONFIG[0].client

    # Call your existing script to process the CSV files
    call_details = {}
    call_details = process_dashboard_csv(CONFIG[0].dashboard, call_details)
    call_details = process_console_csv(CONFIG[0].console, call_details)

    # Convert the call_details dictionary to a DataFrame
    df = pd.DataFrame([call_detail.to_dict() for call_detail in call_details.values()])

    # Calculate the total call charge
    total_call_charge = sum(float(call_detail.call_charge) for call_detail in call_details.values())

    # Render the HTML template with the DataFrame and total call charge
    return render_template('index.html', data=df.to_dict(orient="records"), total_call_charge=total_call_charge, client_name=client_name)

if __name__ == '__main__':
    app.run()
