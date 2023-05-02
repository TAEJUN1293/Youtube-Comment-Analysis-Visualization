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
'''
1. 드라이버 띄워놓고,
2. window_size_to_thin(driver) 실행 후
    -- 작은 창으로하면 영상은 일정수까지만 로딩되기때문에 이용함
3. commentary = Commentary(driver, url="", scroll=, scroll_time=, most=)
    url: 긁어올 url주소
    scroll: 스크롤 횟수 (0이면 맨 밑까지)
        (스크롤 한번에 위치는 상관없고 로드되는 댓글 수는 20개)
    scroll_time: 스크롤 사이 대기시간 (second)
    most: konlpy를 이용할 때, 빈도순위 몇까지 저장할지

4. 이후 commentary에서 클래스변수 사용해서 결과값 받을 수 있음
    (이하 cmt)
    cmt.top_n(n) : konlpy결과 most(n)까지의 Counter출력
    cmt.url      : 가져온 영상의 url
    cmt.title    : 영상 제목
    cmt.comments : 모든 코멘트 list
    cmt.count_of_view : 영상 조회수 (str)
    cmt.count_of_comment : 영상 댓글 수 (int)
    cmt.count_of_comment_all : 수집한 댓글 수 (int)
    
    print(cmt) 출력형식:
    "{} 조회수 ({}), 댓글 수 ({}), 수집한 댓글 ({}),:\ncomments:\n{}\nmost {} nouns:\n{}"
'''

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
count_of_url = len(urls)

contents = []

for i, url in enumerate(urls):
    print("progress.. (%d/%d)"%(i, count_of_url))
    commentary = Commentary(driver, url=url, scroll=10, scroll_time=0.4, most=30)
    contents.append(commentary)

for i in contents:
    print("="*60)
    print(i)
