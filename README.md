# Devman lessons listener

Sends notification to user when the lesson has been reviewed by mentor.

---

### How to execute:

- Download or clone <a href="https://github.com/Ash2803/devman-bot" target="_blank">repo</a>;
- You must have Python 3.6 or higher already installed;
- Create the virtual environment using command:

```
python3 -m venv venv
```

- Install the requirements using command:

```
pip install -r requirements.txt
```

### Get review results


At first, you need to get your auth token from Devman. 
Create a bot and get your token from [BotFather](https://telegram.me/BotFather).
Also you need to specify your chat_id, you can find it [here](https://telegram.me/userinfobot).
Then create environment variables `AUTH_TOKEN`, `TG_BOT_TOKEN` and `TG_CHAT_ID`.

- Execute the script:

```
python lessons.py
```

### Project Goals

The code is written for educational purposes at online-course for web-developers [dvmn.org](https://dvmn.org/)