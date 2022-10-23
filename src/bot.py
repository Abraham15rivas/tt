## IMPORT 
import logging
import sys
import os
import argparse
from dotenv import load_dotenv
from os import getenv
from pathlib import Path

from core.telegrambot import TelegramBot

import ccxt
from core.exchange import CryptoExchange
from core.tradeexecutor import TradeExecutor

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


#IMPORT ENV FILE 
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

# ENV VAR
telegram_tkn = os.getenv("TOKEN")
ALLOWED_USER_ID = getenv("ALLOWED_USER_ID")
parser = argparse.ArgumentParser(description="INT Transformation")
parser.add_argument("--user-id", required=False, type=int, default=ALLOWED_USER_ID)
args = parser.parse_args()
user_id = args.user_id
print(user_id)

print('python', sys.version)
print('CCXT Version:', ccxt.__version__)
print('Please wait while the program is loading...')

if not user_id:
    logger.warning('user_id not set, you will not be able to control the bot')

exchange_id1 = getenv("EXCHANGE1")
exchange_id1_api = getenv("EXCHANGE1YOUR_API_KEY")  
exchange_id1_secret = getenv("EXCHANGE1YOUR_SECRET") 


#EXCHANGE1 from variable id
exchange_id = exchange_id1
exchange_class = getattr(ccxt, exchange_id)
ccxt_ex_1 = exchange_class({
    'apiKey': exchange_id1_api,
    'secret': exchange_id1_secret,
})


#BOT
if __name__ == "__main__":
    #"Start the bot."
    
    #ex1 setup
    exchange1 = CryptoExchange(ccxt_ex_1)
    balance1 = exchange1.free_balance
    print (balance1)
    print ("ex1 setup done")
    trade_executor = TradeExecutor(exchange1)

    #bot setup
    telegram_bot = TelegramBot(telegram_tkn, user_id, trade_executor)

    # Run the bot
    telegram_bot.start_bot()






