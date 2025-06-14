import requests
from telegram import Bot
from datetime import datetime
import pytz
import schedule
import time

# === Configuration ===
API_KEY = 'afbe2f66fdbf06b384a26ab0dc6bfcd2'
BOT_TOKEN = '7247636228:AAECovXvglovAqimj4SBPpCmmthdFyEX1dg'
CHANNEL_ID = '@winwise4'  # Replace with your channel username or chat ID
PLAY_STORE_LINK = 'https://play.google.com/store/apps/details?id=com.winwise.pro'

# === Initialize Bot ===
bot = Bot(token=BOT_TOKEN)

def get_all_leagues():
    url = 'https://api-football-v1.p.rapidapi.com/v3/leagues'
    headers = {
        'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
        'x-rapidapi-key': API_KEY
    }
    params = {'season': '2025'}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    leagues = data.get('response', [])
    league_ids = [league['league']['id'] for league in leagues]
    return league_ids

def get_predictions_all_leagues():
    league_ids = get_all_leagues()
    all_matches = []
    for league_id in league_ids:
        url = 'https://api-football-v1.p.rapidapi.com/v3/predictions'
        headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': API_KEY
        }
        params = {
            'league': str(league_id),
            'season': '2025'
        }
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()
            matches = data.get('response', [])
            all_matches.extend(matches)
        except Exception as e:
            print(f"Failed to fetch predictions for league {league_id}: {e}")
        # Optional: add a short delay here if API rate limits are hit
        # time.sleep(0.5)
    return all_matches

def format_and_send():
    tz = pytz.timezone('Africa/Nairobi')
    today = datetime.now(tz).strftime('%Y-%m-%d')

    matches = get_predictions_all_leagues()

    if not matches:
        bot.send_message(chat_id=CHANNEL_ID, text=f"⚠️ No predictions available for {today}.")
        return

    msg = f"🎯 *Today's AI Bet Predictions* ({today}):\n\n"

    count = 0
    for match in matches:
        if count >= 10:  # Limit output to 10 matches
            break
        try:
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            prediction = match['predictions']['winner']['name'] if match['predictions']['winner'] else "Draw"
            msg += f"🔸 {home} vs {away} → *{prediction}*\n"
            count += 1
        except Exception:
            continue

    msg += f"\n📲 [Get our App on Play Store]({PLAY_STORE_LINK})"
    bot.send_message(chat_id=CHANNEL_ID, text=msg, parse_mode='Markdown')

def job():
    print(f"Running scheduled job at {datetime.now(pytz.timezone('Africa/Nairobi'))}")
    format_and_send()

if __name__ == '__main__':
    # Schedule the job every day at 23:00 EAT
    schedule.every().day.at("23:00").do(job)

    print("Scheduler started, waiting to post at 23:00 EAT every day...")

    while True:
        schedule.run_pending()
        time.sleep(30)  # Check every 30 seconds
