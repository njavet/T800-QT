# T800-QT
A Telegram chat client based on PySide6 and Telethon

## setup
* setup a telegram developer account here: https://my.telegram.org/auth
* create an .env file in the T800-QT directory and put the telegram api keys in it:
```
API_ID=1324
API_HASH='12314'
```

* create a virtual environment and install the requirements
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

* start the app
```
python t800qt/app.py
```
