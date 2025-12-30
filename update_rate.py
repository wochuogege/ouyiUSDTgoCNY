import requests
import datetime
import os
import sys

def get_okx_exchange_rate():
    """
    直接获取 OKX 官方系统参考汇率 (USD/CNY)
    这是 OKX 计算法币价值的基础，与 USDT 价格极度接近
    """
    url = "https://www.okx.com/api/v5/market/exchange-rate"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        
        if data.get('code') == '0':
            # 遍历数据找到 usdCny
            for item in data.get('data', []):
                if 'usdCny' in item:
                    return item['usdCny']
        else:
            print(f"API 报错: {data.get('msg')}")
    except Exception as e:
        print(f"网络连接失败: {e}")
    return None

def write_to_file(rate):
    # 计算北京时间
    beijing_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    file_path = "rate_history.md"
    
    # 构建内容
    if not os.path.exists(file_path):
        content = "# USDT/CNY 汇率监控 (OKX参考价)\n\n| 时间 | 汇率 |\n| :--- | :--- |\n"
    else:
        content = ""
        
    content += f"| {beijing_time} | **{rate}** |\n"
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(content)
    print(f"成功记录: {beijing_time} - {rate}")

if __name__ == "__main__":
    rate = get_okx_exchange_rate()
    if rate:
        write_to_file(rate)
    else:
        print("未能获取数据")
        sys.exit(1)
