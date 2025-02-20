#%%
import os
import re
import json
import requests
from bs4 import BeautifulSoup


MAX_ITEMS = 10
url = f"https://ppg.ly.gov.tw/ppg/api/v1/publication?size={MAX_ITEMS}&page=1&sortCode=01&queryType=0"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
res = requests.get(url, headers=headers)

soup = BeautifulSoup(res.text, "html.parser")
# text to json
res_json = json.loads(soup.text)

total_page = res_json["totalPages"]
for each_page in range(1, total_page + 1):
    print(f"~~~~~第 {each_page} 頁~~~~~~")
    url = f"https://ppg.ly.gov.tw/ppg/api/v1/publication?size={MAX_ITEMS}&page={each_page}&sortCode=01&queryType=0"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    res_json = json.loads(soup.text)
    
    for index, each_data in enumerate(res_json["items"]):
        file_url = each_data['attachments'][0]['link']
        file_name = each_data["title"]

        print(f"【{each_page}-{index + 1}】")
        print(f"公報名稱：{file_name}")
        print(f"公報檔案網址：{file_url}")
        
        # 正則表達式來提取卷的數字
        match = re.search(r"第(\d+)卷", file_name)
        if match:
            print("卷數:", match.group(1))
        else:
            print("Error: 未找到卷數")
        print("===")
        
        # 按照卷數建立資料夾
        folder_name = f"download/{match.group(1)}"
        os.makedirs(folder_name, exist_ok=True)
        
        # 如果檔案已經存在，就不再下載
        if os.path.exists(f"{folder_name}/{file_name}.pdf"):
            print("檔案已經存在，跳過！")
            continue
        else:
            print("下載中...")
            try:
                # download file
                dfile = requests.get(file_url, headers=headers)
                with open(f"{folder_name}/{file_name}.pdf", "wb") as f:
                    f.write(dfile.content)
                print(f"下載成功！")
            except Exception as e:
                print(f"Error: {e}")
                print("下載失敗，跳過！")

