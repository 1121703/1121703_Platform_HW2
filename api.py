import requests
import json
import csv
import urllib3

# 忽略 SSL 驗證警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 你的 API 網址
url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-A0021-001?Authorization=rdec-key-123-45678-011121314"

try:
    # 執行 GET 請求
    response = requests.get(url, verify=False)
    
    if response.status_code == 200:
        data = response.json()
        
        # 1. 儲存 JSON 檔案 (這部分已經確認可以成功)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("成功儲存資料至 data.json")

        # 2. 儲存 CSV 檔案
        # 根據您的資料結構：data['records']['TideForecasts'] 是一個列表
        # 列表中的每個項目都有一個 'Location' 字典
        tide_forecasts = data.get('records', {}).get('TideForecasts', [])

        if tide_forecasts:
            with open('data.csv', 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                # 寫入標題
                writer.writerow(['站點名稱', '站點代碼', '緯度', '經度'])
                
                for entry in tide_forecasts:
                    location = entry.get('Location', {})
                    name = location.get('LocationName')
                    sid = location.get('LocationId')
                    lat = location.get('Latitude')
                    lon = location.get('Longitude')
                    
                    if name: # 確保有抓到資料才寫入
                        writer.writerow([name, sid, lat, lon])
            
            print("成功儲存資料至 data.csv")
        else:
            print("找不到 TideForecasts 資料，請檢查 JSON 結構")
            
    else:
        print(f"請求失敗，狀態碼：{response.status_code}")

except Exception as e:
    print(f"發生錯誤：{e}")