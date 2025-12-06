
# **Banking Capstone Project**

## **DAY 1 — Architecture + Data Ingestion Layer**

### ** Goal**

Stand up storage + eventing + queue + initial ingestion function so that when a file lands in storage the system triggers an Azure Function and enqueues a message
---

## **Step 1 — Create ADLS Gen2 (Azure Data Lake Storage Gen2)**

1. Create a **Storage Account** with:

   * Hierarchical Namespace **Enabled** (ADLS Gen2)
2. Inside the storage account:

   * Create a **container** named `raw`
   * Upload the file: **customers.csv**

**✅ Validation:**
Azure Portal → Storage Accounts → Your Storage → Containers → `raw` → `customers.csv` is present.

---

## **Step 2 — Create the Function App (Event Grid Trigger)**

1. Create the Function App **locally** using:

   * Event Grid Trigger
2. Run locally for testing:

   ```
   func start
   ```

**Test** that the function runs locally without errors.

---

## **Step 3 — Deploy Event Grid Function to Azure**

1. Deploy the Function App from VS Code .
2. After deployment:

   * Event Grid trigger will appear under **Functions** in the portal.
   <img width="1600" height="735" alt="image" src="https://github.com/user-attachments/assets/e958e858-605c-4fe9-af44-b75728a1cbde" />


   
3. Add **Application Settings** in the Function App:

   * `AzureWebJobsStorage` → Storage account connection string
   * `queueconnection` → Connection string of the queue storage account

---

## **Step 4 — Create the Queue**

Inside your Storage Account:

* Go to **Queues**
* Create a queue named: `ingestion-queue`

**✅ Validation:**
Storage Account → Queues → `ingestion-queue` exists.

---

## **Step 5 — Create Event Grid Subscription**

1. Go to your **Container** (`raw`)
2. Create an **Event Grid Subscription**
3. Connect it to the **Azure Function (Event Grid Trigger)**

This ensures the function runs every time a file is uploaded.

---

## **Step 6 — Testing **

1. Upload a file to the `raw-atm` or `raw` container.
2. The Azure Function triggers automatically.
3. Check the queue:

   Storage Account → Queues → `ingestion-queue` → **Peek Messages**

   <img width="1600" height="774" alt="image" src="https://github.com/user-attachments/assets/cf495420-9b40-4eec-acad-10a3e3f51e04" />


You should see a **JSON message** containing:

* Blob URL
* Event time

------------------------------------------------------------------------------------------------
## **DAY 2 — Data Transformation Layer:**

Before starting Day2 : check these validations

1. In Blob storage account : It must contains the raw data of ( atm, upi, customers ) which is a bronze layers

2. Event Grid trigger : This function detects the new blobs in raw containers and the triggers the function in azure

3. Service Bus Queue : After the Event grid triggered in the azure , ingestion-queue receives the meta data from the eventgrid trigger

**In Transformation layer process**:--

1. Queue Trigger function : This function processes the data from the service bus queue

2. Cosmos DB : After that DB stores the cleaned and validated data in the OperationalDB containers


1) Queue Function got successfully deployed locally :

<img width="1600" height="884" alt="image" src="https://github.com/user-attachments/assets/bc2f9ff5-4814-4be0-8e8b-2d92c6813d95" />



<img width="1600" height="874" alt="image" src="https://github.com/user-attachments/assets/94a973be-4999-4c98-842d-0e319e055d45" />


2) Queue trigger function processess the date from the service bus queue

<img width="1600" height="774" alt="image" src="https://github.com/user-attachments/assets/7ab7aa72-dad6-4936-b1c5-41382ea6710f" />


3) Cosmos DB Container stores the validated data but unable to see the messages in the DB 


<img width="696" height="878" alt="image" src="https://github.com/user-attachments/assets/f0ef691e-9653-479a-a298-6d1d8e699bfb" />



