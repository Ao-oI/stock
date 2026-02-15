import psycopg2

conn = psycopg2.connect(host='127.0.0.1', port=5432, database='tdx_stock', user='postgres', password='xjchilli')
cur = conn.cursor()

# Check row counts for all key tables
key_tables = [
    'cn_stock_spot', 'cn_stock_selection', 'cn_stock_indicators', 
    'cn_stock_pattern', 'cn_stock_strategy_enter',
    'cn_stock_strategy_keep_increasing', 'cn_stock_strategy_parking_apron',
    'cn_stock_strategy_backtrace_ma250', 'cn_stock_strategy_breakthrough_platform',
    'cn_stock_strategy_low_backtrace_increase', 'cn_stock_strategy_turtle_trade',
    'cn_stock_strategy_high_tight_flag', 'cn_stock_strategy_climax_limitdown',
    'cn_stock_strategy_low_atr',
    'cn_stock_indicators_buy', 'cn_stock_indicators_sell',
    'cn_stock_spot_buy'
]
print("=== Table Row Counts ===")
for t in key_tables:
    try:
        cur.execute(f'SELECT count(*) FROM "{t}"')
        count = cur.fetchone()[0]
        print(f"  {t}: {count} rows")
    except Exception as e:
        conn.rollback()
        print(f"  {t}: NOT FOUND")

# Check column types for cn_stock_selection (macd_golden_fork)
print("\n=== cn_stock_selection macd_golden_fork type ===")
try:
    cur.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'cn_stock_selection' AND column_name = 'macd_golden_fork'
    """)
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}")
except Exception as e:
    print(f"  Error: {e}")
    conn.rollback()

conn.close()
