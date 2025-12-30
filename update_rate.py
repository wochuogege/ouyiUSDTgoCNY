import requests
import datetime
import os
import sys

def get_okx_rate():
    """
    从 OKX 获取 USDT/CNY 的指数价格
    尝试多个 API 端点以提高稳定性
    """
    # 备用域名列表，防止主域名在某些地区被拦截
    endpoints = [
        "https://www.okx.com/api/v5/market/index-tickers?instId=USDT-CNY",
        "https://aws.okx.com/api/v5/market/index-tickers?instId=USDT-CNY"
    ]
    
    for url in endpoints:
        try:
            print(f"正在尝试连接 API: {url}")
            # 设置 15 秒超时
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == '0' and data.get('data'):
                # idxPx 是 OKX 的指数价格（USDT 兑人民币汇率）
                rate = data['data'][0]['idxPx']
                return rate
            else:
                print(f"API 业务逻辑错误: {data}")
        except Exception as e:
            print(f"当前端点连接失败: {e}")
            continue # 尝试下一个端点
            
    return None

def update_file(rate):
    """
    将获取到的汇率写入或追加到 Markdown 文件中
    """
    # 获取当前北京时间 (UTC+8)
    utc_now = datetime.datetime.utcnow()
    beijing_now = (utc_now + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    
    file_path = "rate_history.md"
    file_exists = os.path.isfile(file_path)
    
    # 准备写入的内容
    # 如果文件不存在，先创建标题和表头
    header = ""
    if not file_exists:
        header = "# USDT 兑人民币汇率历史 (OKX 实时数据)\n\n"
        header += "> 数据来源：OKX API (USDT-CNY 指数价格)\n\n"
        header += "| 更新时间 (北京时间) | 1 USDT 等于 (CNY) |\n"
        header += "| :--- | :--- |\n"
    
    new_line = f"| {beijing_now} | **{rate}** |\n"
    
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            if not file_exists:
                f.write(header)
            f.write(new_line)
        print(f"数据已成功写入 {file_path}")
    except Exception as e:
        print(f"写入文件时出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    current_rate = get_okx_rate()
    
    if current_rate:
        print(f"成功获取汇率: {current_rate}")
        update_file(current_rate)
    else:
        print("所有 API 端点均请求失败，本次任务终止。")
        # 退出码 1 会让 GitHub Actions 标记此步骤为失败，方便你查收邮件提醒
        sys.exit(1)
