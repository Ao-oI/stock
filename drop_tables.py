
import psycopg2
from instock.lib.database import MYSQL_CONN_DBAPI

def drop_tables():
    conn_params = MYSQL_CONN_DBAPI.copy()
    try:
        conn = psycopg2.connect(**conn_params)
        conn.set_isolation_level(0) # Autocommit
        with conn.cursor() as cur:
            tables_to_drop = [
                "cn_stock_selection",
                "cn_stock_indicators_buy",
                "cn_stock_indicators_sell",
                "cn_stock_strategy_enter",
                "cn_stock_strategy_keep_increasing",
                "cn_stock_strategy_parking_apron",
                "cn_stock_strategy_backtrace_ma250",
                "cn_stock_strategy_breakthrough_platform",
                "cn_stock_strategy_low_backtrace_increase",
                "cn_stock_strategy_turtle_trade",
                "cn_stock_strategy_high_tight_flag",
                "cn_stock_strategy_climax_limitdown",
                "cn_stock_strategy_low_atr"
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
