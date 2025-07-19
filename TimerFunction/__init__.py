import json
import datetime
import yfinance as yf
import os
from azure.storage.blob import BlobServiceClient
import logging

import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    ticker_list = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]
    stock_data = {}

    for ticker in ticker_list:
        data = yf.Ticker(ticker)
        price = data.history(period="1d").tail(1)["Close"].values[0]
        stock_data[ticker] = float(price)

    blob_connection_string = os.environ["AZURE_STORAGE_CONNECTION"]
    blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
    container_name = "raw"

    now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    blob_name = f"stockdata-{now}.json"
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    blob_client.upload_blob(json.dumps(stock_data), overwrite=True)
    logging.info(f"Uploaded: {blob_name}")
