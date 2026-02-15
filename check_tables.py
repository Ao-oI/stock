import psycopg2

conn = psycopg2.connect(host='127.0.0.1', port=5432, database='tdx_stock', user='postgres', password='xjchilli')
cur = conn.cursor()

# List all tables
cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name""")
tables = [r[0] for r in cur.fetchall()]
print("=== All tables ===")
for t in tables:
    print(f"  {t}")

# Check row counts for key tables
key_tables = [
    'cn_stock_spot', 'cn_stock_selection', 'cn_stock_indicators', 
    'cn_stock_pattern', 'cn_stock_strategy_enter',
    'cn_stock_indicators_buy', 'cn_stock_indicators_sell'
]
print("\n=== Row counts ===")
for t in key_tables:
    try:
        cur.execute(f'SELECT count(*) FROM "{t}"')
        count = cur.fetchone()[0]
        print(f"  {t}: {count} rows")
    except Exception as e:
        conn.rollback()
        print(f"  {t}: NOT FOUND")

# Check column types for cn_stock_selection (macd_golden_fork)
print("\n=== cn_stock_selection column types (boolean fields) ===")
try:
    cur.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'cn_stock_selection' AND column_name LIKE '%golden%'
        ORDER BY ordinal_position
    """)
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}")
except Exception as e:
    print(f"  Error: {e}")
    conn.rollback()

conn.close()
