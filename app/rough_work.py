import robin_stocks.robinhood as rs
import time
#import config
#from pyrh import Robinhood
import os
from main import login, logout
import pandas as pd

login()
""" 
#account_number1 = "143774412"
symbol = "TMO"
order = rs.orders.order_buy_fractional_by_price(symbol=symbol,
                                            account_number = account_number1,
                                            amountInDollars=float(rs.load_account_profile()["cash"]),
                                            timeInForce='gfd',
                                            extendedHours=False)
print(order)
                            
                          # Calculate the take profit price
take_profit_price = order.price * 1.5
                            
rs.orders.order_sell_option_limit(positionEffect = 'close',
                                                      creditOrDebit='credit', 
                                                      price=take_profit_price, 
                                                      symbol=symbol, 
                                                      quantity=1,  
                                                      optionType='both', 
                                                      account_number=account_number1)





                                                          
    if st.button("Login"):
        try:
            if username and password:
                main.login(str(username), str(password))  # Call the login function from your main.py
                st.success("Logged in successfully!")
            else:
                st.warning("Please enter both username and password.")
        except Exception as e:
            st.warning(f"you are unable to login because {e} you might also check if two factor authentication is active")
    
    

                                                
"""

#rom pyrh import Robinhood





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
















#import robin_stocks as rs
import os

# Other code from your main.py...

# Define a function to download trade history as CSV
def download_trade_history():
    # Ensure that you have logged in
    if not login():
        return None

    # Define the directory and file name for the CSV
    dir_path = "trade_history"  # Change to your desired directory

    # Create the directory if it doesn't exist
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Download the trade history as a CSV
    try:
        rs.export.export_completed_option_orders(dir_path)
        return os.path.join(dir_path, file_name=None)
    except Exception as e:
        print(f"Error downloading trade history: {str(e)}")
        return None









logout()
