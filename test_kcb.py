import logging
logging.basicConfig(level=logging.INFO)
import instock.core.stockfetch as stf

data = stf.fetch_stocks(None)
print(f'获取到 {len(data)} 条股票数据')
print(f'前10条股票代码：{list(data["code"].head(10))}')
star_data = data[data["code"].str.startswith("688")]
print(f'科创板股票（688开头）：{len(star_data)} 条')
if len(star_data) > 0:
    print(f'科创板股票前10条：{list(star_data["code"].head(10))}')
