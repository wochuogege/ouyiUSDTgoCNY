import requests
import datetime
import os
import sys

def get_okx_exchange_rate():
    """获取 OKX 官方系统参考汇率"""
    url = "https://www.okx.com/api/v5/market/exchange-rate"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        if data.get('code') == '0':
            for item in data.get('data', []):
                if 'usdCny' in item:
                    return item['usdCny']
    except Exception as e:
        print(f"网络连接失败: {e}")
    return None

def write_to_files(rate):
    # 1. 更新 Markdown 文件 (包含说明和时间)
    beijing_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    md_path = "rate_history.md"
    md_content = f"""# 🚀 USDT/CNY 实时监控 (OKX)

| 项目 | 数据 |
| :--- | :--- |
| **当前汇率** | **{rate} CNY** |
| **最后更新** | {beijing_time} |
"""
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    # 2. 更新 TXT 文件 (只包含最新价格数字)
    txt_path = "price.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(str(rate))
    
    print(f"已同步更新 MD 和 TXT: {rate}")

if __name__ == "__main__":
    rate = get_okx_exchange_rate()
    if rate:
        write_to_files(rate)
    else:
        print("未能获取数据")
        sys.exit(1)
