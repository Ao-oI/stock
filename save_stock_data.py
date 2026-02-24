import logging
import datetime
import pandas as pd
import instock.core.tablestructure as tbs
import instock.lib.database as mdb
import instock.core.stockfetch as stf

logging.basicConfig(level=logging.INFO)

# 使用 2025-02-13 这个日期
date = datetime.date(2025, 2, 13)
date_str = date.strftime("%Y-%m-%d")

logging.info(f"开始获取股票数据，日期：{date_str}")
data = stf.fetch_stocks(date)

if data is not None and len(data.index) > 0:
    logging.info(f"获取到 {len(data)} 条股票数据")
    
    table_name = tbs.TABLE_CN_STOCK_SPOT['name']
    logging.info(f"表名：{table_name}")
    
    # 删除老数据
    if mdb.checkTableIsExist(table_name):
        logging.info(f"表已存在，删除老数据")
        del_sql = f'DELETE FROM "{table_name}" where "date" = \'{date_str}\''
        mdb.executeSql(del_sql)
        cols_type = None
    else:
        logging.info(f"表不存在，准备创建")
        cols_type = tbs.get_field_types(tbs.TABLE_CN_STOCK_SPOT['columns'])
    
    # 插入数据
    logging.info(f"准备插入数据")
    mdb.insert_db_from_df(data, table_name, cols_type, False, '"date","code"')
    logging.info(f"数据插入完成")
    
    # 统计一下科创板股票
    star_data = data[data["code"].str.startswith("688")]
    logging.info(f"科创板股票（688开头）：{len(star_data)} 条")
else:
    logging.error(f"没有获取到股票数据")
