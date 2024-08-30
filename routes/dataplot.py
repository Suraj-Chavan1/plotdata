from dotenv import load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt
from azure.storage.blob import BlobServiceClient
from pandasai import Agent, SmartDataframe
from flask import Flask, request, jsonify, Blueprint

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
PANDASAI_API_KEY = os.getenv('PANDASAI_API_KEY')
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = os.getenv('AZURE_BLOB_CONTAINER_NAME')

# Set your PandasAI API key
os.environ['PANDASAI_API_KEY'] = PANDASAI_API_KEY




# URL to the CSV file on GitHub


def enter_url(url,input_chat):
    csv_url = url
# Load the CSV file into a DataFrame
    df = pd.read_csv(csv_url)

# Create a SmartDataframe with the DataFrame
    smart_df = SmartDataframe(df)

# Initialize the Agent with the SmartDataframe
    agent = Agent(smart_df)
    

# Query the agent to plot data about customers
    response = agent.chat(input_chat)
    

# Save the plot as a PNG file
    plot_file_name = "customer_data_plot.jpeg"
    plt.savefig(plot_file_name)
    plt.close()
    blob_url = upload_to_blob(plot_file_name, container_name, connection_string)
    return response, blob_url

# Upload the PNG file to Azure Blob Storage
def upload_to_blob(file_name, container_name, connection_string):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

    with open(file_name, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    # Generate the URL for the uploaded blob
    blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{file_name}"
    return blob_url
ppd = Blueprint('plotdata', __name__, url_prefix='/plotdata')

@ppd.route('/url_and_response', methods=['POST'])
def plotdata():
    url = request.json['url']
    input_chat = request.json['input_chat']
    
    response, blob_url = enter_url(url, input_chat)
    
    response_str = str(response)
    
    return jsonify({"response": response_str, "blob_url": blob_url})
