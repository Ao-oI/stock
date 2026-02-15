
import requests

def test_encoding():
    url = "http://82.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": 1, "pz": 50, "po": "1", "np": "1", "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2", "invt": "2", "fid": "f12",
        "fs": "m:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048",
        "fields": "f12",
        "_": "1623833739532",
    }
    
    print("--- Test 1: No Accept-Encoding set manually ---")
    s1 = requests.Session()
    # s1.headers.update({'User-Agent': 'Test'})
    r1 = s1.get(url, params=params)
    print(f"Content-Encoding: {r1.headers.get('Content-Encoding')}")
    try:
        r1.json()
        print("JSON Decode: Success")
    except:
        print("JSON Decode: Failed")

    print("\n--- Test 2: Accept-Encoding set manually ---")
    s2 = requests.Session()
    s2.headers.update({'Accept-Encoding': 'gzip, deflate, br'})
    r2 = s2.get(url, params=params)
    print(f"Content-Encoding: {r2.headers.get('Content-Encoding')}")
    try:
        r2.json()
        print("JSON Decode: Success")
    except:
        print("JSON Decode: Failed")
        print(f"Text starts with: {r2.text[:20]}")

if __name__ == "__main__":
    test_encoding()
