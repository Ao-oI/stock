
import os
import sys
import logging
import datetime

# Add project path to sys.path
cpath_current = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cpath_current)

import instock.job.indicators_data_daily_job as gdj
import instock.job.klinepattern_data_daily_job as kdj
import instock.job.strategy_data_daily_job as sdj

# Configure logging to stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', stream=sys.stdout)

def main():
    print(f"Starting missing jobs at {datetime.datetime.now()}...")
    
    try:
        print("Running indicators job (gdj.main)...")
        gdj.main()
        print("Indicators job completed.")
    except Exception as e:
        print(f"Indicators job failed: {e}")
        logging.exception("Indicators job failed")

    try:
        print("Running kline pattern job (kdj.main)...")
        kdj.main()
        print("Kline pattern job completed.")
    except Exception as e:
        print(f"Kline pattern job failed: {e}")
        logging.exception("Kline pattern job failed")

    try:
        print("Running strategy job (sdj.main)...")
        sdj.main()
        print("Strategy job completed.")
    except Exception as e:
        print(f"Strategy job failed: {e}")
        logging.exception("Strategy job failed")
    
    print(f"All requested jobs finished at {datetime.datetime.now()}")

if __name__ == '__main__':
    main()
