# Banking-capstone

DAY 1 — ARCHITECTURE + DATA INGESTION LAYER
Goal: Stand up storage + eventing + queue + initial ingestion function so that when a file lands in storage the system triggers an Azure Function and enqueues a message

Step 1 — Create ADLS Gen2 (Storage Account with hierarchical namespace)
-- After successful creation of the storgae account
   - create the container inside the storage account as raw
     - inside the raw add the customers.csv file
       
Validation:
In Azure Portal → Storage Accounts → confirm Data lake storage Gen2 enabled.->containers -> Customers.csv

Step 2: - Create the Function App in Azure 
= create the function app locally (event grid trigger )
-Func start 
- Test run locally
  
Step 3: - Deploy Event Grid Function to Azure
- After deploying the function app, Event grid Trigger will reflect into functions 
- Then configure the application settings in function app
   - Add connection string : Azurewebjobstorage (storage account)
   - Add connection string : queueconnection (storage account for the queue )

step 4: - Create the queue inside the storage account 
Validation: Storage account - > Queue -> +Queue -> Ingestion-queue

step 5 : - Create the Event grid Subcription for the container 
 - Using the azure funtion 

Step 6 : - For Testing - upload the test file inside the container 
- Upload a test file to raw-atm container via Portal 
- Check the queue peek messages will appear to see the JSON message.






