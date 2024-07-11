import os
import csv
import logging
from datetime import datetime

proxies = {
    'http': 'http://127.0.0.1:10809',
    'https': 'https://127.0.0.1:10809'
}


def dump_file(row, path):
    open_file = open(path, 'a', encoding='utf-8')
    writer = csv.writer(open_file, dialect='unix')
    writer.writerow(row)
    open_file.close()

def find_all_file(base):
    all_filenames = []
    for root, ds, fs in os.walk(base):
        # for name in fs:
        #     print(os.path.join(root, name))
        for name in fs:
            all_filenames.append(name)
    return all_filenames

def find_all_dir(base):
    all_dirnames = []
    for root, ds, fs in os.walk(base):
        # for name in fs:
        #     print(os.path.join(root, name))
        for name in ds:
            all_dirnames.append(name)
        break
    return all_dirnames

def create_path_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created path: {path}")
    else:
        print(f"Path already exists: {path}")

def get_formatted_date():
    today = datetime.today()
    today_str = today.strftime('%Y-%m-%d')
    return today_str

def get_formatted_time():
    """
    返回当前时间的字符串，格式为 'YYYY-MM-DD-HH:MM'。
    """
    # 获取当前时间
    now = datetime.now()
    # 格式化时间字符串
    formatted_time = now.strftime("%Y-%m-%d-%H:%M")
    return formatted_time

def setup_logger(name, log_file, level=logging.INFO):
    """为每个进程设置一个独立的日志记录器"""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 创建一个处理器，将日志写入指定的文件中
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    # 创建一个日志记录器，并添加处理器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# formatted_date = get_formatted_date()
formatted_date = '2024-07-10'
