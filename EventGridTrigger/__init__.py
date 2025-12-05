import logging
import json
import azure.functions as func

def main(event: func.EventGridEvent, outputQueueItem: func.Out[str]):
    logging.info("Event Grid Trigger executed.")

    data = event.get_json()
    blob_url = data.get("url")
    event_time = event.event_time.isoformat()

    message = {
        "blob_url": blob_url,
        "event_time": event_time,
        "validated": True
    }

    outputQueueItem.set(json.dumps(message))
    logging.info(f"Message pushed to queue: {message}")
