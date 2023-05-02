from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from konlpy.tag import Hannanum
from collections import Counter
import time


from replyscrapper import *

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
window_size_to_thin(driver)
urls_str = '''https://www.youtube.com/watch?v=SzNFCim9nDE
https://www.youtube.com/watch?v=jATxBhsJz6c
https://www.youtube.com/watch?v=puSKd6d1vdA
https://www.youtube.com/watch?v=UO5N-LV3gAA
https://www.youtube.com/watch?v=yOlBsus_Hno
https://www.youtube.com/watch?v=sH2pXruvCZI
https://www.youtube.com/watch?v=aeJOyqdsMlU
https://www.youtube.com/watch?v=J3MS8wbHvGo
'''

urls = urls_str.split()
count_of_urls = len(urls)

contents = []

for i, url in enumerate(urls):
    print("progress.. (%d/%d)"%(i, count_of_urls))
    commentary = Commentary(driver, url=url, scroll=10, scroll_time=0.4, most=30)
    contents.append(commentary)
    #content = get_title_and_comments(driver, url)
    #contents.append(content)

for i in contents:
    print("="*60)
    print(i)

# commentary = Commentary(driver,
#                         url='https://www.youtube.com/watch?v=3aRtJHfsN4g',
#                         scroll=0, scroll_time=0.5,most=30
#                         )
# print(commentary)

# Commentary(driver, url="https://www.youtube.com/watch?v=J3MS8wbHvGo", scroll=10, scroll_time=0.5, most=30)
#

#for i in range(count_of_urls):
#    print("{}: {} / 댓글 수: {}\n{}".format(i+1,))

#save_to_csv(contents)
