import pandas as pd


if __name__ == '__main__':
    # 读取xlsx文件
    xlsx_file = pd.read_excel('国家缩写.xlsx', sheet_name='Sheet1')  # 替换 'your_file.xlsx' 和 'Sheet1' 为实际的文件名和工作表名

    # 将数据保存为csv文件
    xlsx_file.to_csv('country.csv', index=True)  # 替换 'country.csv' 为你想要保存的csv文件名
