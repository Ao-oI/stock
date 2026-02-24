#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


import json
from abc import ABC
from tornado import gen
import logging
import datetime
import instock.lib.trade_time as trd
import instock.core.singleton_stock_web_module_data as sswmd
import instock.web.base as webBase

__author__ = 'myh '
__date__ = '2023/3/10 '


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, bytes):
            return "是" if ord(obj) == 1 else "否"
        elif isinstance(obj, datetime.date):
            delta = datetime.datetime.combine(obj, datetime.time.min) - datetime.datetime(1899, 12, 30)
            return f'/OADate({float(delta.days) + (float(delta.seconds) / 86400)})/'  # 86,400 seconds in day
            # return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)


# 获得页面数据。
class GetStockHtmlHandler(webBase.BaseHandler, ABC):
    @gen.coroutine
    def get(self):
        name = self.get_argument("table_name", default=None, strip=False)
        web_module_data = sswmd.stock_web_module_data().get_data(name)
        # 先检查表是否存在
        table_exists_sql = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{web_module_data.table_name}' AND table_schema = 'public')"
        table_exists = self.db.get(table_exists_sql)
        if table_exists:
            # 处理不同的返回格式
            if isinstance(table_exists, dict):
                # 如果返回的是字典，获取第一个值
                table_exists_value = next(iter(table_exists.values()))
            else:
                # 如果返回的是元组，获取第一个元素
                table_exists_value = table_exists[0]
            if table_exists_value:
                # 查询最新的可用数据日期
                sql = f"SELECT MAX(\"date\") FROM \"{web_module_data.table_name}\""
                result = self.db.get(sql)
                if result:
                    # 处理不同的返回格式
                    if isinstance(result, dict):
                        # 如果返回的是字典，获取第一个值
                        date_value = next(iter(result.values()))
                    else:
                        # 如果返回的是元组，获取第一个元素
                        date_value = result[0]
                    if date_value:
                        date_now_str = date_value.strftime("%Y-%m-%d")
                    else:
                        # 如果没有数据，使用默认日期
                        run_date, run_date_nph = trd.get_trade_date_last()
                        if web_module_data.is_realtime:
                            date_now_str = run_date_nph.strftime("%Y-%m-%d")
                        else:
                            date_now_str = run_date.strftime("%Y-%m-%d")
                else:
                    # 如果没有数据，使用默认日期
                    run_date, run_date_nph = trd.get_trade_date_last()
                    if web_module_data.is_realtime:
                        date_now_str = run_date_nph.strftime("%Y-%m-%d")
                    else:
                        date_now_str = run_date.strftime("%Y-%m-%d")
            else:
                # 如果表不存在，使用默认日期
                run_date, run_date_nph = trd.get_trade_date_last()
                if web_module_data.is_realtime:
                    date_now_str = run_date_nph.strftime("%Y-%m-%d")
                else:
                    date_now_str = run_date.strftime("%Y-%m-%d")
        else:
            # 如果表不存在，使用默认日期
            run_date, run_date_nph = trd.get_trade_date_last()
            if web_module_data.is_realtime:
                date_now_str = run_date_nph.strftime("%Y-%m-%d")
            else:
                date_now_str = run_date.strftime("%Y-%m-%d")
        self.render("stock_web.html", web_module_data=web_module_data, date_now=date_now_str,
                    leftMenu=webBase.GetLeftMenu(self.request.uri))


# 获得股票数据内容。
class GetStockDataHandler(webBase.BaseHandler, ABC):
    def get(self):
        name = self.get_argument("name", default=None, strip=False)
        date = self.get_argument("date", default=None, strip=False)
        web_module_data = sswmd.stock_web_module_data().get_data(name)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')

        if date is None:
            where = ""
        else:
            # where = f" WHERE `date` = '{date}'"
            where = f" WHERE \"date\" = %s"

        order_by = ""
        if web_module_data.order_by is not None:
            order_by = f" ORDER BY {web_module_data.order_by}"

        order_columns = ""
        if web_module_data.order_columns is not None:
            order_columns = f",{web_module_data.order_columns}"

        sql = f" SELECT *{order_columns} FROM \"{web_module_data.table_name}\"{where}{order_by}"
        try:
            data = self.db.query(sql,date)
            
            # 过滤掉流通市值大于500亿和ST类型的股票
            # 不对 ETF 数据进行过滤
            if data and web_module_data.table_name != 'cn_etf_spot':
                # 获取所有股票代码
                codes = [item['code'] for item in data if 'code' in item]
                if codes:
                    # 从 cn_stock_spot 表中获取这些股票的详细信息
                    codes_str = "','".join(codes)
                    spot_sql = f"SELECT code, name, free_cap FROM cn_stock_spot WHERE date = %s AND code IN ('{codes_str}')"
                    try:
                        spot_data = self.db.query(spot_sql, date)
                        # 创建一个字典来存储股票信息
                        stock_info = {}
                        for item in spot_data:
                            stock_info[item['code']] = item
                        
                        # 过滤数据
                        filtered_data = []
                        for item in data:
                            if 'code' in item and item['code'] in stock_info:
                                info = stock_info[item['code']]
                                # 检查是否是ST股票或流通市值大于500亿
                                is_st = info['name'].startswith('ST')
                                is_large_cap = info['free_cap'] > 50000000000
                                if not is_st and not is_large_cap:
                                    filtered_data.append(item)
                            else:
                                # 如果股票不在 cn_stock_spot 表中，保留它（例如科创板股票）
                                filtered_data.append(item)
                        data = filtered_data
                    except Exception as e:
                        logging.error(f"过滤数据异常：{e}")
                        
        except Exception as e:
            # 表不存在时返回空数据，避免500错误
            logging.error(f"GetStockDataHandler查询异常：{web_module_data.table_name}表{e}")
            data = []

        self.write(json.dumps(data, cls=MyEncoder))
