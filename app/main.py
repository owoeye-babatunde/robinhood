import robin_stocks.robinhood as rs
import time
#import config
#from pyrh import Robinhood
import os
import pandas as pd
from datetime import date, timedelta

#import streamlit as st


#def login():

 #   robin_pass = os.environ.get("robinhood_password")
 #   robin_user = os.environ.get("robinhood_username")
    # basic login
 #   rs.login(username=robin_user,
 #           password=robin_pass,
  #          expiresIn=86400,
  #          by_sms=True)



def login_with_2fa(username, password, twofa_code=None):
    try:
        # Initialize the Robinhood API session
        login_params = {
            "username": username,
            "password": password,
            "by_sms": True  # Set by_sms to True to receive SMS for 2FA
        }

        # Include the 2FA code if provided
        if twofa_code:
            login_params["mfa_code"] = twofa_code

        # Perform the login
        login_response = rs.login(**login_params)

        # Check if the login was successful
        if "access_token" in login_response:
            return True, "Login successful."
        else:
            return False, "Login failed: Authentication token not received."

    except Exception as e:
        return False, f"Login failed: {str(e)}"




    

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


# Define your filter criteria
min_market_cap = 1000000000  # $1B market cap
min_gap_percentage = 1.0  # 1% gap
min_price_continuation_percentage = 5.0  # 5% price continuation
max_position_size = 500  # Maximum position size in dollars
max_total_allocation = 5000  # Maximum total allocation in dollars
prior_gap_filled = False
total_open_position = 0

#account_number1 = "143774412"
#account_number2 = "5UD77441"

def check_gap_and_trade():
    global prior_gap_filled, total_open_position
    to_return = None
   
 
    healthcare_stocks = rs.stocks.find_instrument_data('health')
    cash_balance = float(rs.load_account_profile()["cash"])
    expiration_date = date.today() + timedelta(days=100)

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
                #print("Historical data: ", historical_data)

                # Calculate the gap
                today_open = float(historical_data[0]['open_price'])
                yesterday_close = float(historical_data[1]['close_price'])
                gap_percentage = ((today_open - yesterday_close) / yesterday_close) * 100
                print("reach here 2") 
                # Check if the gap meets the criteria
                if abs(gap_percentage) >= min_gap_percentage:
                    # Check price continuation
                    price_continuation_percentage = ((today_open - float(historical_data[2]['low_price'])) / float(historical_data[2]['low_price'])) * 100
                    print("gap cont percent", price_continuation_percentage) 
                    if gap_percentage > 0 and price_continuation_percentage >= min_price_continuation_percentage:
                        # Buy call options with strike at the gap fill level
                        # Ensure that the total position size doesn't exceed max_total_allocation
                        print("reach here 4") 
                        #print(not prior_gap_filled, "2")
                        if ( max_position_size >= cash_balance):        #not prior_gap_filled and 
                            # Implement option buying logic here
                            # Example: rs.options.order_buy_to_open(symbol, "call", expiration_date, strike_price, quantity)
                            print("Trade is here!!")
                            strike_price = today_open * 1.05
                            quantity_to_buy = min(max_position_size / strike_price, cash_balance / strike_price)
                            
                            
                            order_response = rs.orders.order_buy_option_limit(positionEffect="open",
                                                              creditOrDebit="debit",
                                                                price=strike_price,
                                                                  symbol=symbol,
                                                                    quantity=quantity_to_buy,
                                                                      expirationDate=expiration_date.strftime("%Y-%m-%d"),
                                                                        strike=strike_price,
                                                                          optionType='both',
                                                                            account_number=None,
                                                                              timeInForce='gtc',
                                                                                jsonify=True)
                            
                            # Calculate the take profit price as 50% above the strike price
                            take_profit_price = strike_price * 1.5

                            # Place a limit order to sell the option when the take profit price is reached
                            take_profit_order_response = rs.orders.order_sell_option_limit(
                                        positionEffect="close",
                                         creditOrDebit="credit",
                                          price=take_profit_price,
                                           strike_price=take_profit_price,
                                            symbol=symbol,
                                             quantity=quantity_to_buy,  # Same quantity as the buy order
                                              expirationDate=expiration_date.strftime("%Y-%m-%d") # Same expiration date as the buy order
                                   
                                                )
                                
                            
                                                      
                        
                            
                            total_open_position += 1
                            
                            prior_gap_filled = True
                            #print("reach here 5") 
                        else:
                            #print(rs.account.get_account()["cash"])
                            print("Triggering condition satisfied, but your current balance is", rs.load_account_profile()["cash"], "Which is less than", max_position_size)
                            #pass
                    elif gap_percentage < 0 and price_continuation_percentage <= -min_price_continuation_percentage:
                        # Buy put options with strike at the gap fill level
                        # Ensure that the total position size doesn't exceed max_total_allocation
                        #print("negative gap cont percent", price_continuation_percentage)
                        strike_price = today_open * 0.95

                        # Calculate the quantity of options to sell(buy a put option) to stay within the $500 limit
                        quantity_to_buy = min(max_position_size / strike_price, cash_balance / strike_price)


                        # Place a limit order to buy the put option with the calculated expiration date
                        buy_put_order_response = rs.orders.order_buy_option_limit(
                            positionEffect="open",  # For opening a new option position
                            creditOrDebit="debit",
                            price=strike_price,
                            symbol=symbol,
                            quantity=quantity_to_buy,
                            expirationDate=expiration_date.strftime("%Y-%m-%d"),  # Format the date as YYYY-MM-DD
                        )

                        # Calculate the take profit price as 50% of the strike price
                        take_profit_price = strike_price * 0.5

                        # Place a limit order to sell the put option when the take profit price is reached
                        take_profit_order_response = rs.orders.order_sell_option_limit(
                            positionEffect="close",  # For closing an existing option position
                             creditOrDebit="credit",
                              price=take_profit_price,
                               symbol=symbol,
                                quantity=quantity_to_buy,  # Same quantity as the buy order
                                 expirationDate=expiration_date.strftime("%Y-%m-%d"),  # Same expiration date as the buy order
                            )
                                                                            

                            
                            
                        total_open_position += 1
                        
                        prior_gap_filled = True                      
                        #pass
                            
                    
                    # Update prior_gap_filled
                    #prior_gap_filled = True
                    
    else:

        to_return = f"Market scanned by algorithm, {total_open_position} options order was trigered, and total profile balance is {rs.load_account_profile()['cash']}. Algorithm is scanning for possible future opportunity...."
    #return rs.load_account_profile()["cash"]
    return to_return

def download_trade_history():
    # Ensure that you have logged in
    import streamlit as st
    import userpass
    #username, password = userpass.user()
    if not userpass.user():
        
        st.warning("Login to access trade histories")
    else:

        
        # Convert the trade history to a DataFrame
        #trade_history_df = pd.DataFrame(trade_history)
        
        # Get the user's home directory
        try:

            user_home = os.path.expanduser("~")
            
            # Define the path to the download folder
            download_folder = os.path.join(user_home, "Downloads")
            
            # Define the full path for saving the CSV file
            #trade_history_path = os.path.join(download_folder, "trade_history.csv")
                    # Use the export_completed_option_orders function to export trade history
            trade_history = rs.export.export_completed_option_orders(dir_path=user_home)
                # Convert the trade history to a DataFrame
            #trade_history_df = pd.DataFrame(trade_history)
            
            # Save the trade history to a CSV file in the user's download folder
            #trade_history_df.to_csv(trade_history_path, index=False)
            
            # Display a download link for the user
            st.success("Trade history has been downloaded. Click below to download:")
            st.write(f"[Download Trade History CSV]({trade_history})")

        except Exception as e:
            st.warning(f"file not downloaded because {e}")




# Define the active_trades function
def active_trades():
    # Get a list of your active positions
    active_positions = rs.build_holdings()

    # Get a list of your open orders
    open_orders = rs.orders.get_all_open_option_orders()  

    # Create a list to store information about active trades
    active_trades_list = []

    # Loop through active positions and open orders to identify active trades
    for symbol, position in active_positions.items():
        active_trade = {
            "symbol": symbol,
            "quantity": float(position["quantity"]),
            "side": "Buy" if float(position["quantity"]) > 0 else "Sell",
            "price_paid_per_share": float(position["average_buy_price"]) if float(position["quantity"]) > 0 else float(position["average_sell_price"]),
            "trade_id": None,  # Trade ID is not provided in Robinhood's unofficial API
        }
        active_trades_list.append(active_trade)

    for order in open_orders:
        if order['side'] == 'buy':
            active_trade = {
                "symbol": order['symbol'],
                "quantity": float(order['quantity']),
                "side": "Buy",
                "price_paid_per_share": float(order['price']),
                "trade_id": order['id'],
            }
            active_trades_list.append(active_trade)
        elif order['side'] == 'sell':
            active_trade = {
                "symbol": order['symbol'],
                "quantity": float(order['quantity']),
                "side": "Sell",
                "price_paid_per_share": float(order['price']),
                "trade_id": order['id'],
            }
            active_trades_list.append(active_trade)

    # Create a DataFrame from the list of active trades and set the starting index to 1
    active_trades_df = pd.DataFrame(active_trades_list)
    active_trades_df.index = active_trades_df.index + 1  # Set starting index to 1

    return active_trades_df


# Define a function to cancel a specific trade by trade_id
def cancel_trade(trade_id):
    try:
        rs.orders.cancel_option_order(trade_id)
        return True
    except Exception as e:
        print(f"Error canceling trade {trade_id}: {str(e)}")
        return False


def main():
    rs.login()
    while True:
        check_gap_and_trade()
        time.sleep(86400)  # Check for gaps every day (adjust as needed)

if __name__ == "__main__":
    main()



