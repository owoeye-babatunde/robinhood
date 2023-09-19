import robin_stocks.robinhood as rs
import time
import config
from pyrh import Robinhood
import os


import os 

robin_user = os.environ.get("robinhood_username")
robin_pass = os.environ.get("robinhood_password")
print(robin_user, robin_pass)

rs.login(username=robin_user,
         password=robin_pass,
         expiresIn=86400,
         by_sms=False)

rs.logout()

