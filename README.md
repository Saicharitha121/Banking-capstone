
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


3) Cosmos DB Container stores the validated data and inserted rows will appear in the cosmos DB 

Transcations records rows are inserted into the cosmos 
<img width="1600" height="782" alt="image" src="https://github.com/user-attachments/assets/45774e9c-6fb7-4023-bc65-8fb9a2692dee" />


UPI Event records are inserted into the cosmos

<img width="1600" height="781" alt="image" src="https://github.com/user-attachments/assets/7da41db7-51c0-40d0-95d8-1ffd5e0e4d8f" />

<img width="1600" height="773" alt="image" src="https://github.com/user-attachments/assets/7493936c-8987-4e85-912c-9776a230fd03" />


***PySpark Data Clean Pipeline** : 

After the Data got inserted into cosmosDB then the processed data is transformed into the Bronze, silver, Gold Delta layers using the pyspark Framework (code is given in the Pyspark_Dataclean_pipeline) 

<img width="1218" height="943" alt="image" src="https://github.com/user-attachments/assets/8285bf48-8adc-4e66-b914-8e5c21773958" />



### ** Bronze Layer is nothing but the raw layer ( which is before the tranformation )



<img width="1218" height="943" alt="image" src="https://github.com/user-attachments/assets/2012fcc7-eff7-4903-a2fc-56a898a16c41" />

<img width="1198" height="925" alt="image" src="https://github.com/user-attachments/assets/a6e426c9-e08d-4427-9403-e576771a32b9" />


<img width="1196" height="921" alt="image" src="https://github.com/user-attachments/assets/fedfe593-5c87-4245-ac71-edce092674f7" />


### **Silver layer Data :



<img width="1218" height="943" alt="image" src="https://github.com/user-attachments/assets/aa99d00d-7f7a-4b7f-872b-76fe825266a1" />



<img width="1600" height="811" alt="image" src="https://github.com/user-attachments/assets/1e33d0d8-8ca6-477e-838e-eec81653f891" />



<img width="1600" height="808" alt="image" src="https://github.com/user-attachments/assets/7f5311a6-9e44-45b9-a17b-0a470cdde073" />



<img width="1600" height="817" alt="image" src="https://github.com/user-attachments/assets/bc3fae9f-e5ef-4afc-80a5-0ec3e5a1adf7" />


### **Gold layer Data




<img width="1188" height="915" alt="image" src="https://github.com/user-attachments/assets/55ab9d48-70df-44e6-b02b-8142dec2dea5" />



<img width="1188" height="918" alt="image" src="https://github.com/user-attachments/assets/ffe5dfca-98d7-44b8-ac28-81a2d8be7fd3" />



<img width="1183" height="904" alt="image" src="https://github.com/user-attachments/assets/0ae9f0ab-443c-4667-92b8-5ced73d9e2ad" />



<img width="1195" height="918" alt="image" src="https://github.com/user-attachments/assets/1100fbf5-74cb-42fa-a4ef-ed769579c7a7" />



<img width="1196" height="918" alt="image" src="https://github.com/user-attachments/assets/b873c0f4-a5c3-477c-ad2c-14611f6fd397" />



-----------------------------------------------------------------------------------------------------------
### **DAY 3: -- ** Data Warehouse**

1. **Dimensional Model (Star Schema)** : ---

The final dimensional model created for the Banking Analytics Warehouse.

The model follows a Star Schema optimized for BI, reporting, and fraud analytics.

Included Dimensions:-----

* DimCustomer – SCD Type 2 with historical tracking

* DimAccount – Customer accounts and status

* DimBranch – ATM/Branch/UPI device locations

* DimProduct – Loan / Savings / Current account type mapping

* DimDate – Calendar table used for time-series reporting

**Included Fact Tables:------

*FactTransactions – All ATM + UPI transaction details

*FactFraudDetection – High-risk flagged activity

*FactCustomerActivity – Aggregated customer-level metrics


<img width="1182" height="703" alt="image" src="https://github.com/user-attachments/assets/1af6bfe4-d42f-4519-a491-54e4e0b1d99d" />



<img width="1198" height="696" alt="image" src="https://github.com/user-attachments/assets/68813bbc-4364-4d55-b89a-f7ffc516cd1c" />



<img width="1183" height="693" alt="image" src="https://github.com/user-attachments/assets/ba3a9d96-e694-4a9d-bfc2-cac745280733" />



<img width="1173" height="810" alt="image" src="https://github.com/user-attachments/assets/fea5c2f8-a12a-4c82-9bf6-1e1be9b01c38" />



<img width="1183" height="763" alt="image" src="https://github.com/user-attachments/assets/541ca5b3-13d0-4feb-9358-f6b1f194e5c0" />



2) ***Silver to SQL Warehouse ETL Outputs


-   Silver layer data processed using PySpark

-    Data read from ADLS using SAS authentication

-    Dimensions loaded using INSERT + MERGE logic

-    Fact tables Analyzed with UPSERT/MERGE strategies

( The code has been given in the folder Pyspark_ETL_Jobs which is successfully executed using MERGE/UPSERT operations to efficiently load and update dimension and fact tables in the SQL Data Warehouse. ) 


3)  **Scheduled Data Synchronization 

The following screenshot show the automated data synchronization processes implemented using Timer-triggered Azure Functions. These jobs ensure that the SQL Data Warehouse remains continuously updated with the latest customer and account information from the upstream systems.



<img width="1600" height="873" alt="image" src="https://github.com/user-attachments/assets/10e08a7d-3d62-4d20-94b8-31d7bb80ed18" />

---------------------------------------------------------------------------------------------------------------------------

### *** Day 4:  Real-Time Alerts ***

**This module focuses on enabling real-time detection and alerting for suspicious banking activities. Whenever a high-value or unusual transaction flows into the system, the event-driven architecture immediately evaluates it and triggers alerts if required.


**Real-Time Alerts Working: --

-- For every transaction above the configured threshold (e.g., ₹50,000+), an event is instantly pushed to Azure Event Grid.

--If the transaction qualifies as suspicious, an alert entry is created in the FraudAlerts container in Cosmos DB.



<img width="1600" height="882" alt="image" src="https://github.com/user-attachments/assets/0116abd9-4216-464d-8a24-6f2463eca897" />



**The following output Says: ---

* Realtime event arrival in Event Grid

* Execution status of the Event Grid Trigger Azure Function

* Anomaly detection logs and flagged events

* Newly inserted fraud records in Cosmos DB (FraudAlerts)

*  Notification triggers sent via Service Bus Queue/Topic


-------------------------------------------------------------------------------------------

## ** Day 5 : -- Power BI Reporting **

**This phase focuses on building a complete BI and analytics layer on top of the SQL Data Warehouse. Power BI is connected directly to the SQL Server database to visualize business insights across operations, customer behavior, fraud patterns, and compliance needs.



*Report Working :

 - Power BI connects to the Azure SQL Data Warehouse as its primary data source.

 - According to the creation of the dashboards creating some relationships like

   

 * DimCustomer     -  FactTransactions   - CustomerSK = CustomerSK        
 
 * DimCustomer     - FactFraudDetection  - CustomerSK = CustomerSK                 
 
 * DimDate         - FactTransactions    - DateSK = TransactionDateSK (calculated) 
 
 * DimDate         -  FactFraudDetection - DateSK = AlertDateSK (calculated)       
 
 * DimProduct      -  FactTransactions   -  ProductType = TransactionType           
 
 * DimBranch       -  FactTransactions   -  BranchName = Source                     



_  After creating the realtionships creating the visuals based on the fact transcations data 



***Transaction Performance Dashboard



<img width="1368" height="809" alt="image" src="https://github.com/user-attachments/assets/0681b00b-ed30-463a-8a8e-f0e55ea42ad3" />



** This dashboard provides a complete view of daily banking transaction activity across all channels and branches.
It helps business teams monitor transaction volume, customer behavior, and branch-wise activity patterns.



Key points of visualization : ---

*Total Transactions: Shows the overall number of processed transactions.

*Avg Transaction Value: Helps analyze spending trends and patterns.

*Total Amount Processed: Summarizes the total  flow for the selected period.

*ATM Transactions: Indicates the distribution of ATM-related activities.

*Branch Distribution (Pie chart ): Visualizes how transactions are spread across different branches.

*Daily Trend: Shows transaction movement over days to understand peak periods.



*** Fraud Analytics Dashboard



<img width="752" height="735" alt="image" src="https://github.com/user-attachments/assets/0dd23447-8bee-4568-b2fc-8e85a7846693" />


*This dashboard focuses on identifying and analyzing fraudulent transactions detected by the real-time fraud monitoring system.

** Key Points of the visualization:---


*Total Fraud Alerts: Shows the overall number of fraud detections generated by Azure Functions.

*Total & Average Fraud Amount: Helps understand financial impact and severity.

*Top Customers by Fraud Amount: Identifies the highest-risk accounts for immediate investigation.

*Fraud Alerts by Alert Reason: Visualizes the root cause (e.g., High Value Transaction).

*Detailed Fraud Table: Provides transaction-level insights including Account Number, Transaction ID, Amount, and Alert Reason.













