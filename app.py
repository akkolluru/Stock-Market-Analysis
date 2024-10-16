from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

def generate_plot(tickerSymbol, start_date, end_date):
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)
    tickerDf['MA50'] = tickerDf['Close'].rolling(window=50).mean()
    tickerDf['MA200'] = tickerDf['Close'].rolling(window=200).mean()

    plt.figure(figsize=(12, 6))
    plt.plot(tickerDf['Close'], label='Close Price')
    plt.plot(tickerDf['MA50'], label='50-Day Moving Average')
    plt.plot(tickerDf['MA200'], label='200-Day Moving Average')
    plt.title('Stock Price Analysis for ' + tickerSymbol)
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return plot_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tickerSymbol = request.form['ticker']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        plot_url = generate_plot(tickerSymbol, start_date, end_date)
        return redirect(url_for('plot', plot_url=plot_url))
    else:
        company_tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB', 'TSLA', 'NVDA']
        return render_template('index.html', company_tickers=company_tickers)

@app.route('/plot')
def plot():
    plot_url = request.args.get('plot_url')
    return render_template('plot.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
