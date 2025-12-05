
# **Banking Capstone Project**

## **DAY 1 — Architecture + Data Ingestion Layer**

### ** Goal**

Set up the ingestion pipeline so that when a file lands in Azure Storage, an **Event Grid Trigger** fires an **Azure Function**, which then pushes a message into an **Azure Queue**.

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

1. Deploy the Function App from VS Code or CLI.
2. After deployment:

   * Event Grid trigger will appear under **Functions** in the portal.
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

## **Step 6 — Testing the Pipeline**

1. Upload a file to the `raw-atm` or `raw` container.
2. The Azure Function triggers automatically.
3. Check the queue:

   Storage Account → Queues → `ingestion-queue` → **Peek Messages**

You should see a **JSON message** containing:

* Blob URL
* Event time

Let me know if you want a **DAY 2 README**, an **architecture diagram**, or a **full folder structure** for GitHub!
