import psycopg2

conn = psycopg2.connect(host='127.0.0.1', port=5432, database='tdx_stock', user='postgres', password='xjchilli')
cur = conn.cursor()

# Check dates in key tables
for table in ['cn_stock_selection', 'cn_stock_indicators', 'cn_stock_spot']:
    try:
        cur.execute(f'SELECT DISTINCT "date" FROM "{table}"')
        dates = [str(r[0]) for r in cur.fetchall()]
        print(f"{table} dates: {dates}")
    except Exception as e:
        print(f"{table}: Error - {e}")
        conn.rollback()

# Check if cn_stock_attention exists
try:
    cur.execute("SELECT count(*) FROM \"cn_stock_attention\"")
    print(f"cn_stock_attention: {cur.fetchone()[0]} rows")
except Exception as e:
    print(f"cn_stock_attention: Error - {e}")
    conn.rollback()

# Try the actual query that fails
try:
    cur.execute("""SELECT *, (SELECT "datetime" FROM "cn_stock_attention" WHERE "code"="cn_stock_selection"."code") AS "cdatetime" FROM "cn_stock_selection" WHERE "date" = '2026-02-13' ORDER BY "cdatetime" DESC LIMIT 3""")
    rows = cur.fetchall()
    print(f"Selection query result: {len(rows)} rows")
except Exception as e:
    print(f"Selection query ERROR: {e}")
    conn.rollback()

# Try without ordering subquery
try:
    cur.execute("""SELECT count(*) FROM "cn_stock_selection" WHERE "date" = '2026-02-13'""")
    print(f"Selection count (2026-02-13): {cur.fetchone()[0]}")
except Exception as e:
    print(f"Selection count (2026-02-13) ERROR: {e}")
    conn.rollback()

try:
    cur.execute("""SELECT count(*) FROM "cn_stock_selection" WHERE "date" = '2026-02-14'""")
    print(f"Selection count (2026-02-14): {cur.fetchone()[0]}")
except Exception as e:
    print(f"Selection count (2026-02-14) ERROR: {e}")
    conn.rollback()

conn.close()
