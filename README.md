# Setup environment

```
pip install python-telegram-bot --upgrade
```
# Create new Telegram Bot
In telegram, search "BotFather".
Input "/newbot"

`Alright, a new bot. How are we going to call it? Please choose a name for your bot.`

Input the bot name e.g. "TG Testing Bot"

`Good. Now let's choose a username for your bot. It must end in ``bot``. Like this, for example: TetrisBot or tetris_bot.`
Input username end with "bot", e.g. "aaa_bot"

```
Done! Congratulations on your new bot. You will find it at t.me/aaa_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

Use this token to access the HTTP API:

bbb:ccc-ddd

Keep your token secure and store it safely, it can be used by anyone to control your bot.

For a description of the Bot API, see this page: https://core.telegram.org/bots/api`
```
Update the token to config.ini > [telegram] > token

# Getting the chat ID of the bot

Access http://t.me/aaa_bot

Click start button

Browse https://api.telegram.org/bot%http_api_token%

e.g. https://api.telegram.org/botbbb:ccc-ddd


The chat ID is found in 'chat' > 'id', e.g. 12345


Update the chat ID to config.ini > [telegram] > chatId

# Getting the chat ID of the Group

In Telegram, create a new Group, and add the bot @aaa_bot
Browse https://api.telegram.org/bot%http_api_token%/getUpdates

e.g. https://api.telegram.org/botbbb:ccc-ddd/getUpdates

The chat ID is found in 'chat' > 'id', e.g. 12345

Update the chat ID to config.ini > [telegram] > chatId

# Set up the Email account

In gmail, enable imap and generate the application password.

Update the username and password  to config.ini > [gmail] > username, password

# Run 

```
python emailToTelegram.py
```