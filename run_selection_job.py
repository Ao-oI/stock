import os
import sys
import logging

cpath_current = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cpath_current)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', stream=sys.stdout)

import instock.job.selection_data_daily_job as sddj

print("Running selection data job...")
sddj.main()
print("Selection data job completed.")
