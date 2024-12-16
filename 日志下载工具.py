import os
import requests
import datetime
import time
import json
from tkinter import messagebox, Tk, filedialog

# 初始化配置变量
API_KEY = None
SERVER_ID = None
directory = None
LOG_URL = None
STATUS_URL = None
HEADERS = None
DEBUG = True  # 调试模式开关


# 读取配置文件
def load_config():
    global API_KEY, SERVER_ID, LOG_URL, STATUS_URL, HEADERS
    try:
        with open("config.json", "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
            API_KEY = config.get("api_key")
            SERVER_ID = config.get("server_id")

  # 检查是否填写了必要配置
            if not API_KEY or not SERVER_ID:
                show_error("配置文件中缺少 API 密钥或服务器 ID，请检查 config.json 文件。")
                exit()

            # 初始化 URL 和请求头
            LOG_URL = f"https://api.exaroton.com/v1/servers/{SERVER_ID}/logs"
            STATUS_URL = f"https://api.exaroton.com/v1/servers/{SERVER_ID}"
            HEADERS = {"Authorization": f"Bearer {API_KEY}"}
            
            # 调试输出
            print(f"LOG_URL: {LOG_URL}")
            print(f"STATUS_URL: {STATUS_URL}")
            print(f"HEADERS: {HEADERS}")

    except FileNotFoundError:
        show_error("未找到配置文件 config.json，请创建文件并填写必要的配置。")
        exit()
    except json.JSONDecodeError:
        show_error("配置文件格式错误，请检查 config.json 文件内容。")
        exit()







# 检查服务器在线人数
def get_online_players():
    try:
        response = requests.get(STATUS_URL, headers=HEADERS)

        # 打印详细的响应内容，查看具体错误信息
        if DEBUG:
         print(f"请求URL: {STATUS_URL}")
         print(f"响应状态码: {response.status_code}")
         print(f"响应内容: {response.text}")  

        if response.status_code == 200:
            server_data = response.json().get("data", {})
            if DEBUG:
             print("调试信息: 服务器状态返回数据", server_data)  # 打印完整数据，用于调试
           
            # 检查服务器状态
            server_status = server_data.get("status")
            if server_status == 0:
                print("服务器处于关闭状态")
                return -2  # 返回特殊值表示服务器关闭
            
            # 检查在线人数
            players_info = server_data.get("players", {})
            return players_info.get("count", 0)
        else:
            print(f"HTTP 请求失败！状态码: {response.status_code}")
            print(f"错误内容: {response.text}")
            return -1  # 特殊值表示请求失败
    except Exception as e:
        show_error(f"获取服务器状态时发生错误: {e}")
        return -1

# 下载日志
def download_logs():
    global directory
    try:
        response = requests.get(LOG_URL, headers=HEADERS)
        if response.status_code == 200:
            log_data = response.json()["data"]
            log_content = log_data["content"]

            # 检查目录是否存在
            if not os.path.exists(directory):
                os.makedirs(directory)

            # 最近的日志路径
            latest_log_path = os.path.join(directory, "latest_log.txt")

            # 如果最新日志内容未变，跳过保存
            if os.path.exists(latest_log_path):
                with open(latest_log_path, "r", encoding="utf-8") as latest_log:
                    if latest_log.read() == log_content:
                        print("日志内容未更新，跳过保存。")
                        return

            # 生成带时间戳的文件名
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_path = os.path.join(directory, f"server_log_{SERVER_ID}_{timestamp}.txt")

            # 保存日志到本地文件
            with open(log_path, "w") as log_file:
                log_file.write(log_content)

            print(f"日志已成功保存为 {log_path}")
        else:
            show_error(f"无法获取日志: {response.status_code}")
    except Exception as e:
        show_error(f"下载日志时发生错误: {e}")

# 错误提示窗口
def show_error(message):
    print(f"错误: {message}")  # 仅打印错误信息

# 选择日志保存路径
def choose_directory():
    global directory
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    root.attributes("-topmost", True)  # 确保窗口置顶
    messagebox.showinfo("选择保存路径", "请选择日志保存的文件夹")
    directory = filedialog.askdirectory(title="选择日志保存路径")
    if not directory:
        show_error("未选择保存路径，程序将退出。")
        exit()
    root.destroy()

# 主循环
def main():
    global directory
    print("开始监控服务器状态...")
    while True:

     try:
            
        online_players = get_online_players()

        if online_players == -2:  # 服务器关闭
                print("服务器关闭，等待服务器重新启动...")

        elif online_players == 0: #无人在线
            print("服务器无人在线，开始下载日志...")
            download_logs()
        elif online_players > 0: #有人在线
            print(f"服务器当前在线人数: {online_players}，暂不下载日志。")
        else:
            print("获取服务器状态失败，稍后重试。")
     except Exception as e:
            print(f"主循环中发生错误: {e}")

        # 每隔2分半钟检查一次
     time.sleep(150)

if __name__ == "__main__":
     
    load_config()
    # 第一次启动时选择保存路径
    choose_directory()

    # 自动最小化 CMD 窗口
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)

    # 启动主逻辑
    main()
