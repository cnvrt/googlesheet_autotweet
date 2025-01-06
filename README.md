# googlesheet_autotweet
# Tweet Poster App

This project automates the process of reading tweets from a Google Sheet and posting them to X (formerly Twitter) using Flask, Selenium, and the Google Sheets API.

## Prerequisites

Ensure the following dependencies and tools are installed on your system:

1. Python 3.12 or later
2. Google Chrome browser
3. Chromedriver

## Steps to Set Up and Run the Application

1. **Install Python Virtual Environment Packages:**

   ```bash
   sudo apt install python3.12-venv
   sudo apt install python3-virtualenv
   ```

2. **Create a Virtual Environment:**

   ```bash
   virtualenv env --python=python3
   ```

3. **Update and Upgrade System Packages:**

   ```bash
   sudo apt update
   sudo apt upgrade
   ```

4. **Create and Activate Virtual Environment:**

   ```bash
   python -m venv ./venv
   source venv/bin/activate
   ```

5. **Install Python Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Install Google Chrome:**

   ```bash
   wget -P files/ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   sudo apt install -y ./files/google-chrome-stable_current_amd64.deb
   ```

7. **Install Chromedriver:**

   ```bash
   sudo apt install chromium-chromedriver
   ```

8. **Run the Application:**

   ```bash
   python app.py
   ```

## Environment Variables

Create a `.env` file in the project root directory with the following variables:

```plaintext
X_USERNAME=your_x_username
X_PASSWORD=your_x_password
```

## Google Sheets API Configuration

1. Enable the Google Sheets API for your project in the Google Cloud Console.
2. Download the `credentials.json` file and place it in the project root directory.
3. Ensure your Google Sheet ID is accessible and replace the placeholder in the code as needed.

## Application Endpoints

### Base URL:

`/`

**Response:**

```plaintext
Welcome to the Tweet Poster App!
```

### Read Google Sheet:

`/sheetid/<slug>`

- Replace `<slug>` with your Google Sheet ID.

### Post Tweets from Google Sheet:

`/sheetid/<slug>/post-tweets`

- Replace `<slug>` with your Google Sheet ID.
- This endpoint reads tweets from the sheet and posts them to X.

## Code Overview

The main application logic includes:

- **Google Sheets API integration** to read tweets.
- **Selenium automation** to log in to X and post tweets.
- **Flask routes** to handle API requests.

## Notes

- Ensure that `chromedriver` is installed and its path is correctly set in the `DRIVER_PATH` variable.
- The application supports login via cookies to avoid repeated logins.
- The Selenium Chrome driver runs in headless mode for efficiency.

## Disclaimer

This project is for educational purposes only. Ensure you comply with X's terms of service and API usage policies when deploying this application.
