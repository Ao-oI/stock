import psycopg2

conn = psycopg2.connect(host='127.0.0.1', port=5432, database='tdx_stock', user='postgres', password='xjchilli')
conn.set_isolation_level(0)  # Autocommit
cur = conn.cursor()

# Drop cn_stock_selection (has wrong boolean column types)
cur.execute('DROP TABLE IF EXISTS "cn_stock_selection"')
print("Dropped cn_stock_selection")

conn.close()
print("Done. Now re-run selection_data_daily_job to recreate with correct schema.")
