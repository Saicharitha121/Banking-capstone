from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("Banking_Day3_Perfect_Clean").getOrCreate()

# 1. ADLS CONFIG

sas_token = "sv=2024-11-04&ss=bfqt&srt=sco&sp=rwdlacupyx&se=2025-12-09T14:11:41Z&st=2025-12-09T05:56:41Z&spr=https&sig=ULKbIFygtqazKhG1N%2BV4bCMHvd2th5cVdAhvyRt9Wds%3D"

account = "charithastorage123.dfs.core.windows.net"
spark.conf.set(f"fs.azure.account.auth.type.{account}", "SAS")
spark.conf.set(f"fs.azure.sas.token.provider.type.{account}", 
               "org.apache.hadoop.fs.azurebfs.sas.FixedSASTokenProvider")
spark.conf.set(f"fs.azure.sas.fixed.token.{account}", sas_token)


# 2. READ SILVER DATA

atm = spark.read.parquet("abfss://silver@charithastorage123.dfs.core.windows.net/atm_silver")
upi = spark.read.parquet("abfss://silver@charithastorage123.dfs.core.windows.net/upi_silver")
cust = spark.read.parquet("abfss://silver@charithastorage123.dfs.core.windows.net/cust_silver")


# 3. SQL CONFIG

jdbc_url = (
    "jdbc:sqlserver://charithaserver.database.windows.net:1433;"
    "database=charithadatabase;"
    "encrypt=true;trustServerCertificate=false;"
    "hostNameInCertificate=*.database.windows.net;"
)
props = {
    "user": "charitha",
    "password": "charitha@123",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}


# 4. DIM CUSTOMER (MERGE)

print("1/7 DIM CUSTOMER")

cust_clean = (
    cust.select("CustomerID", "Name", "Email", "Phone")
        .withColumn("StartDate", F.current_timestamp())
)

cust_clean.write.mode("overwrite").jdbc(jdbc_url, "Staging_DimCustomer", props)

spark.read.format("jdbc") \
     .option("url", jdbc_url) \
     .option("dbtable", "(EXEC usp_MergeDimCustomer) t") \
     .option("user", "charitha") \
     .option("password", "charitha@123") \
     .load()

print("DimCustomer → MERGED")


# 5. DIM ACCOUNT (MERGE)

print("2/7 DIM ACCOUNT")

accounts = (
    atm.select("AccountNumber", "CustomerID")
       .union(upi.select("AccountNumber", "CustomerID"))
       .distinct()
       .withColumn("Status", F.lit("active"))
)

accounts.write.mode("overwrite").jdbc(jdbc_url, "Staging_DimAccount", props)

spark.read.format("jdbc") \
     .option("url", jdbc_url) \
     .option("dbtable", "(EXEC usp_MergeDimAccount) t") \
     .option("user", "samanth") \
     .option("password", "Bunty5550#") \
     .load()

print("DimAccount → MERGED")


# 6. DIM BRANCH (INCREMENTAL)

print("3/7 DIM BRANCH")

atm_branches = (
    atm.filter("ATMID IS NOT NULL")
       .selectExpr("ATMID AS BranchID", "Location AS BranchName", "Location")
)

upi_branches = (
    upi.filter("DeviceID IS NOT NULL")
       .selectExpr("DeviceID AS BranchID", "'Digital/UPI' AS BranchName", "GeoLocation AS Location")
)

branch = atm_branches.union(upi_branches).distinct()

existing = spark.read.jdbc(jdbc_url, "DimBranch", props).select("BranchID")

branch.join(existing, "BranchID", "left_anti") \
      .write.mode("append").jdbc(jdbc_url, "DimBranch", props)

print("DimBranch → LOADED")


# 7. DIM DATE (INCREMENTAL)

print("4/7 DIM DATE")

dates = (
    atm.select(F.to_date("TxnTimestamp").alias("Date"))
       .union(upi.select(F.to_date("TxnTimestamp").alias("Date")))
       .distinct()
       .withColumn("DateSK", F.date_format("Date", "yyyyMMdd").cast("int"))
       .withColumn("Year", F.year("Date"))
       .withColumn("Month", F.month("Date"))
       .withColumn("Day", F.dayofmonth("Date"))
       .withColumn("Quarter", F.quarter("Date"))
)

existing_dates = spark.read.jdbc(jdbc_url, "DimDate", props).select("DateSK")

dates.join(existing_dates, "DateSK", "left_anti") \
     .write.mode("append").jdbc(jdbc_url, "DimDate", props)

print("DimDate → LOADED")


# 8. FACT TRANSACTIONS (MERGE)

print("5/7 FACT TRANSACTIONS")

current_sk = (
    spark.read.jdbc(jdbc_url, "DimCustomer", props)
         .filter("IsCurrent = 1")
         .select("CustomerID", "CustomerSK")
)

atm_tx = (
    atm.select(
        "TransactionID", "AccountNumber", "CustomerID",
        F.to_date("TxnTimestamp").alias("TransactionDate"),
        F.col("TransactionAmount").cast("decimal(18,2)").alias("Amount"),
        F.lit("WITHDRAWAL").alias("TransactionType"),
        F.lit("ATM").alias("Source"),
        F.lit(0).alias("IsSuspicious")
    )
)

upi_tx = (
    upi.select(
        "TransactionID", "AccountNumber", "CustomerID",
        F.to_date("TxnTimestamp").alias("TransactionDate"),
        F.col("TransactionAmount").cast("decimal(18,2)").alias("Amount"),
        "transaction_type",
        F.lit("UPI").alias("Source"),
        F.lit(0).alias("IsSuspicious")
    )
)

tx_raw = atm_tx.unionByName(upi_tx)

tx_staging = (
    tx_raw.join(current_sk, "CustomerID", "left")
          .select("TransactionID", "AccountNumber", "CustomerSK",
                  "TransactionDate", "Amount",
                  "TransactionType", "Source", "IsSuspicious")
)

tx_staging.write.mode("overwrite").jdbc(jdbc_url, "Staging_FactTransactions", props)

spark.read.format("jdbc") \
     .option("url", jdbc_url) \
     .option("dbtable", "(EXEC usp_MergeFactTransactions) t") \
     .option("user", "samanth") \
     .option("password", "Bunty5550#") \
     .load()

print("FactTransactions → UPSERTED")


# 9. FACT CUSTOMER ACTIVITY

print("6/7 FACT CUSTOMER ACTIVITY")

fact = spark.read.jdbc(jdbc_url, "FactTransactions", props)

activity = (
    fact.alias("f")
        .groupBy("CustomerSK")
        .agg(
            F.count("*").alias("TotalTransactions"),
            F.sum("Amount").alias("TotalAmount"),
            F.max("TransactionDate").alias("LastActivityDate"),
            F.sum(F.col("IsSuspicious").cast("int")).alias("SuspiciousCount")
        )
)

activity.write.mode("overwrite").jdbc(jdbc_url, "FactCustomerActivity", props)

print("FactCustomerActivity → SUCCESS")


# 10. FACT FRAUD DETECTION

print("7/7 FACT FRAUD DETECTION")

fraud = (
    fact.filter("Amount > 90000")
        .select(
            "TransactionID", "AccountNumber", "CustomerSK",
            F.current_timestamp().alias("AlertTimestamp"),
            F.lit("High Value Transaction").alias("AlertReason"),
            "Amount"
        )
)

fraud.write.mode("overwrite").jdbc(jdbc_url, "FactFraudDetection", props)

print("FactFraudDetection → SUCCESS")
