
import psycopg2
from instock.lib.database import MYSQL_CONN_DBAPI

def check_db():
    conn_params = MYSQL_CONN_DBAPI.copy()
    try:
        conn = psycopg2.connect(**conn_params)
        with conn.cursor() as cur:
            tables = ["cn_stock_spot", "cn_stock_selection"]
            for table in tables:
                try:
                    cur.execute(f"SELECT count(*) FROM \"{table}\"")
                    count = cur.fetchone()[0]
                    print(f"Table {table}: {count} rows")
                except Exception as e:
                    print(f"Error checking {table}: {e}")
                    conn.rollback()
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    check_db()
