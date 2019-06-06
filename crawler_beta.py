import requests
from bs4 import BeautifulSoup
import re, os 
import pandas as pd
from time import sleep
from random import randint

# Done [Step 1] 我目前的dataset中有一個變數url (幾千筆)，
# 變數內容是一堆美國上市公司在SEC EDGAR網站上傳文件的「網址」(含html原始碼)，如附檔( .xls中url這個變數)。
# Done [Step 2] 我想要在這些網址(url)中，搜尋幾個特定字眼，如:EBITDA、EBIT等。

# [Step 3] 接著創造一個變數是: 這個字眼在該網頁內出現的「頻率(次數) 」。
# Done [Step 4] (optional) 如果能夠再多創造一個變數，
# 將這個字眼在網頁內出現的那個段落也擷取出來的話更好。當該字眼不只出現一次時，
# 擷取它第一次出現位置的那個段落。這個步驟難度若很高的話就算了。


headers = {
    'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13"
}

EBITDA_pattern = re.compile("EBITDA", re.IGNORECASE)
EBIT_pattern = re.search("EBIT", re.IGNORECASE)

init = pd.read_excel("./test-url.xls")
url_col_name = init.columns[0]

if not os.path.isfile("tmp_url_list"):
    url_list = list(init[url_col_name])
    done_list = []
else:
    print("Use cached urls")
    with open("tmp_url_list") as f:
        url_list = f.read()


def extract(url):
    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.text)
    p_list = soup.find_all('p')
    p_list = [item.text.replace('\n','') for item in p_list]

    result1 = list(filter(EBITDA_pattern.search, p_list))
    result2 = list(filter(EBIT_pattern.search, p_list))

    for i, item in enumerate(p_list):
        if 'EBITDA' in item:
            print(i)
            print(p_list[i])
    
    ebida = result1[0] if result1 else ""
    ebit = result2[0] if result2 else ""

    return ebida, ebit
    
for url in url_list:
    try:
        extract(url)
        done_list.append(url)
        url_list.remove(url)

        sleep(randint(3,8))
    except Exception:
        with open('tmp_url_list','w') as f:
            for item in url_list:
                f.write(f"{item}\n")
            print("Exception Handled, saved unfinished works")
        raise Exception
            