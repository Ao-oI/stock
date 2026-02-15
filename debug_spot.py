
import requests
import time

def test_fetch_spot():
    # URL from stock_hist_em.py
    url = "http://82.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": 1,
        "pz": 50,
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f12",
        "fs": "m:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048",
        "fields": "f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f14,f15,f16,f17,f18,f20,f21,f22,f23,f24,f25,f26,f37,f38,f39,f40,f41,f45,f46,f48,f49,f57,f61,f100,f112,f113,f114,f115,f221",
        "_": "1623833739532",
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://quote.eastmoney.com/"
    }

    try:
        print(f"Requesting {url}...")
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"Status Code: {resp.status_code}")
        print(f"Content Type: {resp.headers.get('Content-Type')}")
        
        if resp.status_code == 200:
            try:
                data = resp.json()
                print("JSON decode success.")
                if "data" in data and "diff" in data["data"]:
                    print(f"Got {len(data['data']['diff'])} items.")
                else:
                    print(f"Unexpected JSON structure or empty data.")
            except Exception as e:
                print(f"JSON decode failed: {e}")
                print(f"Response text (first 500 chars):\n{resp.text[:500]}")
        else:
             print(f"Response text (first 500 chars):\n{resp.text[:500]}")
             
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_fetch_spot()
