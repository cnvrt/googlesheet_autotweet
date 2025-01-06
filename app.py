from dotenv import load_dotenv
import os
import time
import gspread
import pickle
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from webdriver_manager.chrome import ChromeDriverManager

# Setup Flask
app = Flask(__name__)

# Google Sheets API configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
DRIVER_PATH = '/usr/bin/chromedriver'   #get path using this "which chromedriver" command in ubuntu terminal
# X login credentials
xuser = os.getenv('X_USERNAME')
xpass = os.getenv('X_PASSWORD')

def auth_google_sheet():
    return service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)

def pickle_save_auth():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds:
        if creds and creds.expired:
            creds.refresh(Request())
        else:
            creds = auth_google_sheet()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def read_sheet(SHEET_ID):
    creds = pickle_save_auth()
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID)
    return sheet.sheet1.col_values(1)

def post_tweet(tweet_content):
    options = Options()
    options.add_argument("--headless")  # Optional: Run in headless mode (no UI)
    options.add_argument("--no-sandbox")  # Fix for some environments (like Docker or VM)
    options.add_argument("--disable-dev-shm-usage")  # Fix for Docker containers
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    login_need=True
    if os.path.exists('cookies.pkl'):
        login_need=False
    if login_need:
        driver.get('https://x.com/i/flow/login')
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.NAME, 'text'))
        )
        time.sleep(1)
        username = driver.find_element(By.NAME, 'text')
        username.send_keys(xuser)
        username.send_keys(Keys.RETURN)
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.NAME, 'password'))
        )
        time.sleep(2)
        password = driver.find_element(By.NAME, 'password')
        password.send_keys(xpass)
        password.send_keys(Keys.RETURN)
    else:
        driver.get('https://x.com')
        with open("cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        # driver.refresh()
        driver.get('https://x.com/home')
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.DraftEditor-root'))
    )
    # time.sleep(2)
    # tweet_box = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Tweet text"]')
    editor_root = driver.find_element(By.CSS_SELECTOR, 'div.DraftEditor-root')
    tweet_box = editor_root.find_element(By.CSS_SELECTOR, 'div.public-DraftEditor-content')
    # for tweet_new in tweet_content:
    #     tweet_box.send_keys(tweet_new)
    tweet_box.send_keys(tweet_content)
    tweet_box.send_keys(Keys.RETURN)
    tweet_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="tweetButtonInline"]')
    tweet_button.click()
    with open("cookies.pkl", "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    # time.sleep(10)
    driver.quit()

@app.route('/')
def index():
    return "Welcome to the Tweet Poster App!"

@app.route('/sheetid/<slug>')
def sheetid(slug):
	return read_sheet(slug)

@app.route('/sheetid/<slug>/post-tweets', methods=['GET'])
def post_tweets(slug):
    # x_user = request.args.get('x_username')
    tweets = read_sheet(slug)
    
    if not tweets:
        return jsonify({"message": "No tweets found in the Google Sheet."}), 400

    for tweet in tweets:
        tweet_content = tweet
        post_tweet(tweet_content)
        print(f"Tweet posted: {tweet_content}")

    return jsonify({"message": f"Successfully posted {len(tweets)} tweet(s)."}), 200

if __name__ == '__main__':
    app.run(debug=True)
 