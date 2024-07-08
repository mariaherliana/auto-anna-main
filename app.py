from flask import Flask, render_template
import pandas as pd
from src.csv_processing import process_console_csv, process_dashboard_csv, save_merged_csv
from src.CallDetail import CallDetail
from src.idn_area_codes import EMERGENCY_NUMBERS, PHONE_PREFIXES, INTERNATIONAL_PHONE_PREFIXES
from src.utils import parse_jakarta_datetime, convert_to_jakarta_time_iso, call_hash, classify_number, format_datetime_as_human_readable, format_timedelta, format_username, parse_call_memo, parse_iso_datetime

app = Flask(auto-anna-main)

@app.route('/')
def index():
  # Call the existing script to process the CSV files
  call_details = {}
  call_details = process_dashboard_csv("path/to/dashboard.csv", call_details)
  call_details = process_console_csv("path/to/console.csv", call_details)

  # Convert the call_details dictionary to a DataFrame
  df = pd.DataFrame([call_detail.to_dict() for call_detail in call_details.values()])

  # Render the HTML template with the DataFrame
  return render_template('index.html', data=df.to_dict(orient="records"))

if __name__ == '__main__':
  app.run()
