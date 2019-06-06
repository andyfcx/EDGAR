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


def string_clean(string):
    return ' '.join(string.replace('\n',' ').replace('\t',' ').split())

def extract(url):
    headers = {
    'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13"
}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")

    p_list = soup.find_all('p')
    p_list = [ string_clean(item.text) for item in p_list] # Clean the data

    ebitda = parse("EBITDA", p_list, res)
    ebit = parse("EBIT", p_list, res)

    # result2 = re.findall("EBIT", string_clean(res.text), re.IGNORECASE)
    # EBIT_pattern = re.compile("EBIT", re.IGNORECASE)
    # match2 = list(filter(EBIT_pattern.search, p_list))
    # print("Count of EBIT", len(result2))
    return ebitda, ebit

def parse(keyword, p_list, res):
    result1 = re.findall(keyword, string_clean(res.text), re.IGNORECASE)
    word_count = len(result1)

    keyword_pattern = re.compile(keyword, re.IGNORECASE)
    match1 = list(filter(keyword_pattern.search, p_list))
    
    paragraph = match1[0] if match1 else ""
    print(f"Count of {keyword}", len(result1))
    return (word_count, paragraph)

def test():
    ebida, ebit = extract("https://www.sec.gov/Archives/edgar/data/3116/000115752310001572/0001157523-10-001572.txt")
    print(ebida)
    print(ebit)

def main():
    
    init = pd.read_excel("./test-url.xls")
    url_col_name = init.columns[0]
    
    if not os.path.isfile("tmp_url_list"):
        url_list = list(init[url_col_name])
        done_list = []
    else:
        print("Use cached urls")
        with open("tmp_url_list") as f:
            url_list = f.read()

    EBITDA_wordcount = []
    EBITDA_paragraph = []
    EBIT_wordcount = []
    EBIT_paragraph = []

    for url in url_list:
        try:
            ebitda, ebit = extract(url)

            done_list.append(url)
            url_list.remove(url)
            t = randint(1,3)
            sleep(t)
            print(f"Sleep for {t} secs.")
            
        except Exception:
            with open('tmp_url_list','w') as f:
                for item in url_list:
                    f.write(f"{item}\n")
                print("Exception Handled, saved unfinished works")
            raise Exception
        EBITDA_wordcount.append(ebitda[0])
        EBITDA_paragraph.append(ebitda[1])
        EBIT_wordcount.append(ebit[0])
        EBIT_paragraph.append(ebit[1])
        
    init["EBITDA_wordcount"] = EBITDA_wordcount
    init["EBITDA_paragraph"] = EBITDA_paragraph
    init["EBIT_wordcount"] = EBIT_wordcount
    init["EBIT_paragraph"] = EBIT_paragraph

    init.to_csv("EBITDA.csv", index=False)

if __name__ == "__main__":
    main()
    # test()