import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient
import os, json, csv, io
from urllib.parse import urlparse

COSMOS_URL = os.environ["COSMOS_URL"]
COSMOS_KEY = os.environ["COSMOS_KEY"]
STORAGE_CONN = os.environ["AzureWebJobsStorage"]

cosmos_client = CosmosClient(COSMOS_URL, credential=COSMOS_KEY)
database = cosmos_client.get_database_client("bank_ops_db")

def main(msg: func.ServiceBusMessage):
    logging.info("QueueProcessor (Service Bus) triggered.")

    body = msg.get_body().decode("utf-8")
    event = json.loads(body)

    blob_url = event["data"]["url"]
    logging.info(f"Blob URL: {blob_url}")

    # read blob
    blob_service = BlobServiceClient.from_connection_string(STORAGE_CONN)
    parsed = urlparse(blob_url)
    container_name = parsed.path.split('/')[1]
    blob_name = '/'.join(parsed.path.split('/')[2:])

    blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)
    content = blob_client.download_blob().readall().decode("utf-8")

    reader = csv.DictReader(io.StringIO(content))

    for row in reader:
        # determine type
        if "atm" in blob_name.lower():
            container = database.get_container_client("ATMTransactions")
        elif "upi" in blob_name.lower():
            container = database.get_container_client("UPIEvents")
        else:
            logging.error("Unknown file type")
            continue

        if not row.get("transactionId"):
            logging.error("Missing transactionId, skipping.")
            continue

        container.upsert_item(row)

    logging.info("QueueProcessor completed.")
