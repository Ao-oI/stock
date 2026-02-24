import sys
import os
sys.path.insert(0, "/app")

# 设置项目路径
cpath_current = os.path.dirname(os.path.dirname("/app"))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)

import logging
import datetime
import instock.job.execute_daily_job as edj

print(f'开始执行完整数据采集: {datetime.datetime.now()}')
logging.basicConfig(level=logging.INFO)
edj.main()
print(f'完成数据采集: {datetime.datetime.now()}')