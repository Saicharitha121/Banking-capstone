import logging
import json
import azure.functions as func

def main(event: func.EventGridEvent) -> None:
    """
    Real-Time Fraud Detection Function
    Triggered by Azure Event Grid when a high-value transaction occurs
    """
    logging.info("=== FRAUD DETECTION FUNCTION TRIGGERED ===")
    
    try:
     
        event_data = event.get_json()
        logging.info(f"Event received: {json.dumps(event_data)}")
      
        tx = event_data.get('data', {})
        amount = float(tx.get('Amount', 0))
        transaction_id = tx.get('TransactionID')
        customer_id = tx.get('CustomerID')
        location = tx.get('Location', 'Unknown')
        transaction_type = tx.get('TransactionType', 'Unknown')

  
        is_fraud = False
        reasons = []

  
        if amount > 50000:
            is_fraud = True
            reasons.append(f"High value: ₹{amount:,.0f}")

   
        trusted_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune"]
        if location not in trusted_cities:
            is_fraud = True
            reasons.append(f"Suspicious location: {location}")

    
        if transaction_type == "WITHDRAWAL" and "UPI" in tx.get('Source', ''):
            is_fraud = True
            reasons.append("UPI cash withdrawal (rare pattern)")

     
        if is_fraud:
            alert = {
                "TransactionID": transaction_id,
                "CustomerID": customer_id,
                "Amount": amount,
                "Location": location,
                "Reason": " | ".join(reasons),
                "AlertLevel": "HIGH" if amount > 100000 else "MEDIUM",
                "Status": "Pending Review"
            }
            logging.warning(f"FRAUD ALERT RAISED: {alert}")
           
        else:
            logging.info(f"Transaction {transaction_id} passed fraud check")

    except Exception as e:
        logging.error(f"Error in fraud detection: {str(e)}")