import robin_stocks.robinhood as rs
import time
import config
from pyrh import Robinhood
import os
import pandas as pd
import streamlit as st
#USERNAME = "bayleynorwood3@gmail.com"
#PASSWORD = "Mustang2017"
"""
time_logged_in = 60 * 60 * 24 * days
    rs.authentication.login(username = config.USERNAME,
                            password = config.PASSWORD,
                            expiresIn = time_logged_in,
                            scope = 'internal',
                            by_sms = True,
                            store_session = 
                            )


"""

#rs.export.export_completed_option_orders(dir_path="Downloads", file_name=None)
def login(robin_user, robin_pass):

    #robin_pass = os.environ.get("robinhood_password")
    #robin_user = os.environ.get("robinhood_username")
    # basic login
    rs.login(username=robin_user,
            password=robin_pass,
            expiresIn=86400,
            by_sms=True)
        
def logout():
    rs.logout()


# bayleynorwood3@gmail.com Mustang2017




# Initialize your Robinhood API session
#rs.login(username="your_username", password="your_password")

# Define your filter criteria
min_market_cap = 1000000000  # $1B market cap
min_gap_percentage = 1.0  # 1% gap
min_price_continuation_percentage = 5.0  # 5% price continuation
max_position_size = 500  # Maximum position size in dollars
max_total_allocation = 5000  # Maximum total allocation in dollars
prior_gap_filled = False

def check_gap_and_trade():   
    global prior_gap_filled
    """
    for i in rs.stocks.find_instrument_data('health'):

        #print(i["symbol"])
        for cap in (rs.stocks.get_fundamentals(i["symbol"], info="market_cap")):
                    if float(cap) >= min_market_cap:
                        print(cap)
    """
    # Get a list of healthcare sector stocks
    #for i in rs.stocks.find_instrument_data('health'):
    #for i in rs.markets.get_top_movers():
        #print(i['symbol'])
    
    #healthcare_stocks = rs.markets.get_top_movers("health")
    healthcare_stocks = rs.stocks.find_instrument_data('health')
    # Sort healthcare stocks by market cap in descending order
    #healthcare_stocks.sort(key=lambda x: x['market_cap'], reverse=True)

    for stock in healthcare_stocks:
        symbol = stock['symbol']
        for cap in rs.stocks.get_fundamentals(stock["symbol"], info="market_cap"):
            market_cap = float(cap)
            #market_cap = float(stock['market_cap'])
            print("reach here 1")    
            # Filter by market cap
            if market_cap >= min_market_cap:        
                # Get historical data for the stock  
                historical_data = rs.stocks.get_stock_historicals(symbol, interval="day", span="year")

                # Calculate the gap
                today_open = float(historical_data[0]['open_price'])
                yesterday_close = float(historical_data[1]['close_price'])
                gap_percentage = ((today_open - yesterday_close) / yesterday_close) * 100
                print("reach here 2") 
                # Check if the gap meets the criteria
                if abs(gap_percentage) >= min_gap_percentage:
                    # Check price continuation
                    price_continuation_percentage = ((today_open - float(historical_data[2]['low_price'])) / float(historical_data[2]['low_price'])) * 100
                    print("reach here 3") 
                    if gap_percentage > 0 and price_continuation_percentage >= min_price_continuation_percentage:
                        # Buy call options with strike at the gap fill level
                        # Ensure that the total position size doesn't exceed max_total_allocation
                        print("reach here 4") 
                        print(not prior_gap_filled)
                        if not prior_gap_filled and (rs.account.get_account()["cash"] - max_position_size) >= 0:
                            # Implement option buying logic here
                            # Example: rs.options.order_buy_to_open(symbol, "call", expiration_date, strike_price, quantity)
                            rs.orders.order_buy_fractional_by_price(symbol=symbol,
                                            amountInDollars=max_position_size,
                                            timeInForce='gtc',
                                            extendedHours=False)
                            print("reach here 5") 
                        else:
                            print("Sorry!, No enough balance")
                            #pass
                    elif gap_percentage < 0 and price_continuation_percentage <= -min_price_continuation_percentage:
                        # Buy put options with strike at the gap fill level
                        # Ensure that the total position size doesn't exceed max_total_allocation
                        print("reach here 6")
                        if not prior_gap_filled and (rs.account.get_account()["cash"] - max_position_size) >= 0:
                            # Implement option buying logic here
                            # Example: rs.options.order_buy_to_open(symbol, "put", expiration_date, strike_price, quantity)
                            rs.orders.order_buy_fractional_by_price(symbol=symbol,
                                            amountInDollars=max_position_size,
                                            timeInForce='gtc',
                                            extendedHours=False)                      
                            #pass
                            print("reach here 7") 
                    
                    # Update prior_gap_filled
                    prior_gap_filled = True
                    print("reach here 8")
def download_trade_history():
    # Ensure that you have logged in
    if not login():
        return None
    
    # Use the export_completed_option_orders function to export trade history
    trade_history = rs.export.export_completed_option_orders()
    
    # Convert the trade history to a DataFrame
    trade_history_df = pd.DataFrame(trade_history)
    
    # Save the trade history to a CSV file
    remote_user_download_path = f"/path/to/remote/user/download/folder/trade_history.csv"
    trade_history_df.to_csv(remote_user_download_path, index=False)
    
    # Display a download link for the user
    st.success("Trade history has been downloaded. Click below to download:")
    st.write(f"[Download Trade History CSV](sandbox:/path/to/remote/user/download/folder/trade_history.csv)")

    


# Other code from your main.py...

# Define a function to cancel a specific trade by trade_id
def cancel_trade(trade_id):
    try:
        rs.orders.cancel_option_order(trade_id)
        return True
    except Exception as e:
        print(f"Error canceling trade {trade_id}: {str(e)}")
        return False

# Other code from your main.py...

                    

def main():
    rs.login()
    while True:
        check_gap_and_trade()
        time.sleep(600)  # Check for gaps every 10 minutes (adjust as needed)

if __name__ == "__main__":
    main()
    



