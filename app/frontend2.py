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

    #username, password = userpass.credential()
    #twofa_code = st.text_input("2FA Code")



    # Create a Streamlit app
    st.title("Robinhood Login")

    # Input fields for username, password, and 2FA code
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    twofa_code = st.text_input("2FA Code")

    # Login button
    if st.button("Login"):
        if not username or not password:
            st.error("Username and password are required.")
        else:
            # Attempt the login with username and password
            login_successful, login_message = main.login_with_2fa(username, password)

            if login_successful:
                st.success(login_message)
            elif "Two-factor authentication code is required." in login_message:
                if not twofa_code:
                    st.error(login_message)
                else:
                    # Retry the login with the 2FA code
                    login_successful, login_message = main.login_with_2fa(username, password, twofa_code)
                    if login_successful:
                        st.success(login_message)
                    else:
                        st.error(login_message)
            else:
                st.error(login_message)









        # Run algorithm
    st.subheader("Run Algorithm")

    if st.button("Run Algorithm"):
        st.text("Algorithm is running. This is a long running work. Simply close the page to logout automatically as the algorithm scans continuously for options opportunities")
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

    if st.button("Cancel All algo Trades"):
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



    
    if st.button("Logout"):
        try:
            main.logout()  # Call the logout function from your main.py
            st.success("Logged out successfully!")
        except Exception as e:
             st.error(f" {e}.")
        

if __name__ == "__main__":
    main_frontend()
