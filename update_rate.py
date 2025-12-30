import requests
import datetime
import os

def get_okx_rate():
    # 尝试使用国际备用接口
    url = "https://www.okx.com/api/v5/market/index-tickers?instId=USDT-CNY"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status() # 检查是否返回了 4xx 或 5xx 错误
        data = response.json()
        if data.get('code') == '0':
            return data['data'][0]['idxPx']
        else:
            print(f"API 返回错误: {data}")
    except Exception as e:
        print(f"请求失败: {e}")
    return None

def update_file(rate):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = "rate_history.md"
    
    # 检查文件是否存在
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("# USDT 兑人民币汇率历史 (OKX)\n\n")
            f.write("| 时间 | 汇率 (USDT/CNY) |\n| --- | --- |\n")
        f.write(f"| {now} | {rate} |\n")

if __name__ == "__main__":
    rate = get_okx_rate()
    if rate:
        update_file(rate)
        print(f"成功获取汇率: {rate}")
    else:
        print("未能获取汇率，不更新文件。")
        # 强制退出，让 GitHub Actions 知道这一步没成功
        exit(1)
