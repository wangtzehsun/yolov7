import os

# 指定資料夾路徑
folder_path = 'F:/水果實驗/dataset'

# 確保指定的路徑存在
if not os.path.exists(folder_path):
    print(f"指定的資料夾路徑 '{folder_path}' 不存在。")
else:
    # 列出資料夾內所有jpg檔案
    jpg_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]

    # 排序檔案列表
    jpg_files.sort()

    # 設定起始編號和跳號間隔
    start_number = 1
    skip_interval = 20  # 這裡設定為跳號20

    # 逐一改名
    for i, old_name in enumerate(jpg_files, start=start_number):
        new_name = f"{start_number}.jpg"
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f"將 {old_name} 改為 {new_name}")

        # 更新下一個編號
        start_number += skip_interval

print("完成改名。")
