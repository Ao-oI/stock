
import requests
import time
import os

def test_fetch():
    print(f"HTTP_PROXY: {os.environ.get('HTTP_PROXY')}")
    print(f"HTTPS_PROXY: {os.environ.get('HTTPS_PROXY')}")
    url = "https://data.eastmoney.com/dataapi/xuangu/list"
    # Basic fields for test
    sty = "SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,CHANGE_RATE"
    params = {
        "sty": sty,
        "filter": '(MARKET in ("上交所主板","深交所主板","深交所创业板"))(NEW_PRICE>0)',
        "p": 1,
        "ps": 50,
        "source": "SELECT_SECURITIES",
        "client": "WEB"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://data.eastmoney.com/xuangu/",
        "Origin": "https://data.eastmoney.com",
        "Cookie": "st_si=78948464251292; st_psi=20260205091253851-119144370567-1089607836; st_pvi=07789985376191; st_sp=2026-02-05%2009%3A11%3A13; st_inirUrl=https%3A%2F%2Fxuangu.eastmoney.com%2FResult; st_sn=12; st_asi=20260205091253851-119144370567-1089607836-webznxg.dbssk.qxg-1",
        "Accept-Encoding": "gzip, deflate, br, zstd"
    }

    try:
        print(f"Requesting {url}...")
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"Status Code: {resp.status_code}")
        print(f"Content Type: {resp.headers.get('Content-Type')}")
        print(f"URL: {resp.url}")
        
        if resp.status_code == 200:
            try:
                data = resp.json()
                print("JSON decode success.")
                if "result" in data and "data" in data["result"]:
                    print(f"Got {len(data['result']['data'])} items.")
                else:
                    print(f"Unexpected JSON structure: {data.keys()}")
            except Exception as e:
                print(f"JSON decode failed: {e}")
                print(f"Response text (first 500 chars):\n{resp.text[:500]}")
        else:
             print(f"Response text (first 500 chars):\n{resp.text[:500]}")
             
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_fetch()
