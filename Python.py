import requests
from telegram import Bot
from datetime import datetime
import pytz

# === Configuration ===
API_KEY = 'afbe2f66fdbf06b384a26ab0dc6bfcd2'
BOT_TOKEN = '7247636228:AAECovXvglovAqimj4SBPpCmmthdFyEX1dg'
CHANNEL_ID = '@winwise4'  # Replace with actual channel username or numeric ID (e.g. -1001234567890)
PLAY_STORE_LINK = 'https://play.google.com/store/apps/details?id=com.winwise.pro'

# === Initialize Bot ===
bot = Bot(token=BOT_TOKEN)

def get_predictions():
    url = 'https://api-football-v1.p.rapidapi.com/v3/predictions'
    headers = {
        'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
        'x-rapidapi-key': API_KEY
    }
    params = {
        'league': '39',  # English Premier League
        'season': '2025'
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def format_and_send():
    tz = pytz.timezone('Africa/Nairobi')
    today = datetime.now(tz).strftime('%Y-%m-%d')

    data = get_predictions()
    matches = data.get('response', [])

    if not matches:
        bot.send_message(chat_id=CHANNEL_ID, text=f"⚠️ No predictions available for {today}.")
        return

    msg = f"🎯 *Today's AI Bet Predictions* ({today}):\n\n"

    for match in matches[:5]:  # Limit to first 5 predictions
        try:
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            prediction = match['predictions']['winner']['name'] if match['predictions']['winner'] else "Draw"
            msg += f"🔸 {home} vs {away} → *{prediction}*\n"
        except Exception as e:
            continue

    msg += f"\n📲 [Get our App on Play Store]({PLAY_STORE_LINK})"
    bot.send_message(chat_id=CHANNEL_ID, text=msg, parse_mode='Markdown')

if __name__ == '__main__':
    format_and_send()
