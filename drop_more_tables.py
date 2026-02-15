
import psycopg2
from instock.lib.database import MYSQL_CONN_DBAPI

def drop_tables():
    conn_params = MYSQL_CONN_DBAPI.copy()
    try:
        conn = psycopg2.connect(**conn_params)
        conn.set_isolation_level(0) # Autocommit
        with conn.cursor() as cur:
            tables_to_drop = [
                "cn_stock_indicators",
                "cn_stock_pattern"
            ]
            for table in tables_to_drop:
                try:
                    cur.execute(f"DROP TABLE IF EXISTS \"{table}\"")
                    print(f"Dropped table: {table}")
                except Exception as e:
                    print(f"Error dropping {table}: {e}")
                    
        conn.close()
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    drop_tables()
