import os
import json
import logging
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, ApplicationBuilder, ContextTypes

# Set up Telegram bot
API_TOKEN = '6286278769:AAEVAjUdDTCR3pzzyLQRHbXP5f9PHAwMOBE'

# Set up Google Sheets API
SERVICE_ACCOUNT_FILE = 'Telegram-Bot\\telegram-bot-385920-102851e95fae.json'
SPREADSHEET_ID = '1cD_8bVUi6XSnYuZk6wvL0AfBo4fqS5hrls8ftc8D-1A'
RANGE_NAME = 'Log!A2:C'  # Change this to match the range you want to write to

# Load Google Sheets API credentials
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets'])

# Create a Google Sheets API client
sheets_api = build('sheets', 'v4', credentials=credentials)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
print(SERVICE_ACCOUNT_FILE)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def call(update: Update, context: ContextTypes.DEFAULT_TYPE):
    team_name = update.message.text
    date_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    user = update.effective_user.full_name

    # Write to Google Sheets
    values = [[date_time, user, team_name]]
    body = {'values': values}
    sheets_api.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=body).execute()

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{user} calls "{team_name}".')

def main():
    application = ApplicationBuilder().token(API_TOKEN).build()
    start_handler = CommandHandler('start', start)
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    call_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), call)

    application.add_handler(start_handler)
    # application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(call_handler)
    application.run_polling()
    # dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, record_team))

    # updater.start_polling()
    # updater.idle()

if __name__ == '__main__':
    main()

