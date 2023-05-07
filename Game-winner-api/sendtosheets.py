import os
import json
import pandas as pd
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import gamewinner


# Set up Google Sheets API
SERVICE_ACCOUNT_FILE = 'Telegram-Bot\\telegram-bot-385920-102851e95fae.json'
SPREADSHEET_ID = '1cD_8bVUi6XSnYuZk6wvL0AfBo4fqS5hrls8ftc8D-1A'
RANGE_NAME = 'Games!A2:D'  
DATE_COL = 'Games!B2:B'

# Load Google Sheets API credentials
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets'])

# Create a Google Sheets API client
sheets_api = build('sheets', 'v4', credentials=credentials)


def log_data(data):
    # team_id = data.values.tolist()
    # game_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    # game_id = 
    # game_sequence = 

    # # Write to Google Sheets
    # values = [[game_id, game_date, game_sequence, team_id]]
    values = data.values.tolist()
    body = {'values': values}
    sheets_api.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=body).execute()

def get_latest_date():
    dates = sheets_api.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=DATE_COL).execute()
    values = dates.get('values',[])

    latest_date = None
    if values:
        latest_date = datetime.datetime.strptime(values[-1][0], '%Y-%m-%dT%H:%M:%S').date()

    return latest_date


def main():
    latest_date = get_latest_date()
    today = datetime.date.today()
    i_date = latest_date + datetime.timedelta(days=1)

    while i_date < today:
        data = gamewinner.fetch_nba_results(i_date)
        log_data(data)
        i_date += datetime.timedelta(days=1)

if __name__ == '__main__':
    main()

