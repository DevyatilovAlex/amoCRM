import configparser
from telethon.sync import TelegramClient
from telethon import connection
from pprint import pprint

# Для корректного переноса даты и время в json
from datetime import datetime, date

# Классы для работы с группами
from telethon.tl.functions.channels import GetChannelsRequest
from telethon.tl.types import ChannelParticipantsSearch


# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значение внутренним переменным
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)
client.start()

for dialog in list(client.iter_dialogs())[:10]:
    print(dialog.title)
    print(client.get_entity(dialog.title))
