import os
from neuralintents import BasicAssistant
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import mplfinance as mpf
import yfinance as yf

import pickle
import sys
import datetime as dt

with open('wallet.pkl', 'rb') as f:
    wallet = pickle.load(f)

def save_wallet():
    with open('wallet.pkl', 'wb') as f:
        pickle.dump(wallet, f)

def add_coin():
    ticker = input("Which coin do you want to add: ")
    amount = float(input("How many of the coin do you want to add: "))

    if ticker in wallet.keys():
        wallet[ticker] += amount
    else:
        wallet[ticker] = amount

    save_wallet()

def remove_coin():
    ticker = input("Which coin do you want to sell: ")
    amount = float(input("How many of the coin do you want to sell: "))

    if ticker in wallet.keys():
        if amount <= wallet[ticker]:
            wallet[ticker] -= amount
            save_wallet()
        else:
            print("You don't have enough coins")
    else:
        print(f"you don't own any coins of {ticker}")

def show_wallet():
    print("Your wallet:")
    for ticker in wallet.keys():
        print(f"You own {wallet[ticker]} {ticker}")


def wallet_worth():
    sum = 0
    for ticker in wallet.keys():
        # Adjusts ticker to include -USD for crypto
        adjusted_ticker = f"{ticker}-USD"  
        try:
            # Get the ticker object
            stock = yf.Ticker(adjusted_ticker)
            
            # Get real-time price data
            price_data = stock.history(period="1d")
            
            # Check if the data is not empty
            if not price_data.empty:
                price = price_data['Close'].iloc[0] 
                sum += price * wallet[ticker]
            else:
                print(f"Data for {ticker} is not available.")
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    
    print(f"Your wallet is worth {sum} USD")

def wallet_gains():
    starting_date = input("Enter a date for comparison (YYYY-MM-DD): ")
    curr_sum = 0
    prev_sum = 0

    try:
        for ticker in wallet.keys():
            adjusted_ticker = f"{ticker}-USD"  
            
            # Get the ticker object
            stock = yf.Ticker(adjusted_ticker)
            
            # Get historical price data including the current and the starting date
            data = stock.history(start=starting_date)
            
            if data.empty:
                print(f"No data available for {ticker}.")
                continue

            # Get current price
            price_now = data['Close'].iloc[-1] 
            
            # Get the price on the starting date
            try:
                price_then = data.loc[data.index == starting_date]['Close'].values[0] 
            except IndexError:
                print(f"No data available for {ticker} on {starting_date}.")
                continue

            curr_sum += price_now * wallet[ticker]
            prev_sum += price_then * wallet[ticker]
        
        # Calculate relative gains
        if prev_sum > 0:
            gains = (curr_sum - prev_sum) / prev_sum * 100
            print(f"Relative Gains: {gains:.2f}%")
        else:
            print("No previous sum available to calculate gains.")
    except Exception as e:
        print(f"Error calculating gains: {e}")


import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf

def plot_chart():
    ticker = input("Choose a cryptocurrency ticker you want to plot: ")
    starting_string = input("Choose a starting date (DD/MM/YYYY): ")

    plt.style.use('dark_background')

    # Convert the input date string to a datetime object
    start = dt.datetime.strptime(starting_string, "%d/%m/%Y")

    adjusted_ticker = f"{ticker}-USD"

    # Fetch the historical data using yfinance
    data = yf.Ticker(adjusted_ticker).history(start=start)

    # Check if data is available
    if data.empty:
        print(f"No data available for {ticker} from {starting_string}.")
        return

    # Plot the closing price data
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label=f'{ticker} Close Price', color='cyan')

    # Add titles and labels
    plt.title(f'{ticker} Price from {starting_string} to Today')
    plt.xlabel('Date')
    plt.ylabel('Close Price (USD)')
    plt.legend()

    plt.show()



def coin_price():
    ticker = input("Choose a ticker you want the price of: ")

    adjusted_ticker = f"{ticker}-USD"

    # Get the ticker object
    stock = yf.Ticker(adjusted_ticker)
    
    # Get historical price data including the current and the starting date
    data = stock.history(period="1d")
    if data.empty:
        print(f"No data available for {ticker}.")
        return
    # Get current price
    price_now = data['Close'].iloc[-1]  # Last available data point
    print(price_now)



    

def bye():
    print("Goodbye")
    sys.exit(0)

mappings = {
    'plot_chart' : plot_chart,
    'add_coin' : add_coin,
    'remove_coin' : remove_coin,
    'wallet_worth' : wallet_worth,
    'show_wallet' : show_wallet,
    'wallet_gains' : wallet_gains,
    'bye' : bye,
    'coin_price' : coin_price
}

# Create an assistant
assistant = BasicAssistant('intents.json', mappings)

assistant.fit_model(epochs=50)
assistant.save_model()
assistant.load_model()

# Run the assistant
while True:
    message = input("")
    assistant.process_input(message)