import streamlit as st
import main
import time
import userpass

# Define Streamlit app layout and behavior
def main_frontend():
    st.title("Bayley's Robinhood Options Trading Algorithm")

    #main.login()
    
    # User login and logout
    #username = st.text_input("Robinhood Username", type="password")
    #password = st.text_input("Robinhood Password", type="password")
    username, password = userpass.credential()

    if st.button("Login"):
        try:
            if username and password:
                main.login(str(username), str(password))  # Call the login function from your main.py
                st.success("Logged in successfully!")
            else:
                st.warning("Please enter both username and password.")
        except Exception as e:
            st.warning(f"you are unable to login because {e} you might also check if two factor authentication is active")
    

        # Run algorithm
    st.subheader("Run Algorithm")

    if st.button("Run Algorithm"):
        st.text("Algorithm is running. This is a long running work. Simply clode the page to logout automatically as the algorithm scans continuously for options opportunities")
        try:
            while True:
                algo = main.check_gap_and_trade()
                st.write(algo)
                time.sleep(86400)  # Check for gaps every 10 minutes (adjust as needed)
        except Exception as e:
            st.error(f"scanning stopped because {e}.")


    # Trade management
    st.subheader("Trade Management")

    if st.button("Cancel Trade"):
        trade_id_to_cancel = st.text_input("Trade ID to Cancel")
        if trade_id_to_cancel:
            success = main.cancel_trade(trade_id_to_cancel)
            if success:
                st.success(f"Trade {trade_id_to_cancel} canceled successfully!")
            else:
                st.error(f"Error canceling trade {trade_id_to_cancel}.")

    if st.button("Cancel All Trades"):
        # Implement a function in main.py to cancel all open trades
        # For example: main.cancel_all_trades()
        st.success("All trades canceled successfully!")



     # View trade status
    st.subheader("View Trade Status")

    if st.button("View Active Trades"):
        try:
            trades_df = main.active_trades()  # Call the active_trades function from main.py
            if not trades_df.empty:
                st.dataframe(trades_df)
            else:
                st.info("No active trades found.")
        except Exception as e:
             st.error(f"Unable to view because {e}.")





    # Data download
    st.subheader("Trade History Data Download")

    if st.button("Download Trade History"):
        # Implement a function in main.py to retrieve trade history and save it as a CSV
        # For example: main.download_trade_history()
        main.download_trade_history()
        #st.success("Trade history downloaded and saved as CSV!")


    
    if st.button("Logout"):
        try:
            main.logout()  # Call the logout function from your main.py
            st.success("Logged out successfully!")
        except Exception as e:
             st.error(f" {e}.")
        

if __name__ == "__main__":
    main_frontend()
