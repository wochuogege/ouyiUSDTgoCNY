import requests
import datetime
import os

def get_okx_rate():
    # 使用 OKX 公开的指数价格接口 (此处以 USDT/CNY 为例)
    url = "https://www.okx.com/api/v5/market/index-tickers?instId=USDT-CNY"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data['code'] == '0':
            rate = data['data'][0]['idxPx']
            return rate
    except Exception as e:
        print(f"获取汇率失败: {e}")
    return None

def update_file(rate):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"| 时间 | 汇率 (USDT/CNY) |\n| --- | --- |\n| {now} | {rate} |\n"
    
    # 如果文件不存在，写入表头；如果存在，追加内容
    file_path = "rate_history.md"
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
        print(f"成功更新汇率: {rate}")
