import sys, os

# !{sys.executable} -m pip install -U -q pandas mysql-connector-python yfinance

import mysql.connector
import pandas as pd

# Get variables
DB_HOSTNAME = os.getenv('DBHOSTNAME', 'kidzeal.com')
DB_NAME = os.getenv('ASTOCK', 'iamkittu_astock')
DB_USERNAME = os.getenv('DBUSERNAME', 'iamkittu_astock')
DB_PASSWORD = os.getenv('DBUSERPWD', 'astock.guru')


bloomberg_url = "www.bloomberg.com/profile/company/{}:US"
sec_rss_url = "www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&output=atom"

# Parse sec data
ct_df = pd.read_json ('https://www.sec.gov/files/company_tickers.json', orient='index')


db_connection = mysql.connector.connect(
  host=DB_HOSTNAME,
  database=DB_NAME,
  user=DB_USERNAME,
  password=DB_PASSWORD
)
cursor = db_connection.cursor()


company_ticker_upsert = "INSERT INTO COMPANY_TICKERS (cik, cik_str, ticker, name) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE cik=%s"

company_ticker_data = ()

INSERT INTO table (id, name, age) VALUES(1, "A", 19) ON DUPLICATE KEY UPDATE    
name="A", age=19


 (`id`, ``, `modifiedOn`, `active`, `cik`, ``, ``, ``, `website`, `bloomberg_url`, `rss_url`) VALUES (NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '1', NULL, NULL, NULL, NULL, NULL, NULL, NULL)


query = "SELECT cik, name FROM COMPANY_TICKERS"
myresult = cursor.execute(query)

for (cik, name) in cursor:
  print("CIK: {},  name: {} ".format(cik, name))

cursor.close()
db_connection.close()