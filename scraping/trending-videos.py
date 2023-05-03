import os
import re
import time
import datetime
from dateutil.relativedelta import relativedelta
# selenium으로부터 webdriver 모듈을 불러옵니다.
from selenium import webdriver
from selenium.webdriver.common.by import By
# Explicit Wait을 위해 추가
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])


# 링크 경로
link_path_format = '{}_link.txt'
# 댓글 경로
comment_path_format = '{}_comment.txt'
# 인기 급상승 url
url = 'https://www.youtube.com/feed/trending{}'
# 최신, 음악, 게임, 영화
categories = {
    'recent': '',
    'music': '?bp=4gINGgt5dG1hX2NoYXJ0cw%3D%3D',
    'game': '?bp=4gIcGhpnYW1pbmdfY29ycHVzX21vc3RfcG9wdWxhcg%3D%3D',
    'movie': '?bp=4gIKGgh0cmFpbGVycw%3D%3D'
}


def save_as_file(file_path: str, content: list, overwrite: bool = False, encoding: str = 'utf-8'):
    """
    결과를 파일로 저장
    :params:
    - file_path: 파일 경로
    - content: 파일 내용
    - overwrite: True인 경우, 파일이 이미 존재하면 덮어씀
    - encoding: utf-8
    """
    mode, prev = ('w', '') if os.path.exists(file_path) and overwrite else ('a', '\n')
    with open(file_path, mode, encoding=encoding) as f:
        f.write(prev+'\n'.join(str(item) for item in content))


def get_timestamp(current_time: datetime.datetime, timestamp: str):
    numbers = re.sub(r'[^0-9]', '', timestamp)
    if '초' in timestamp:
        diff_time = current_time - relativedelta(seconds=int(numbers))
    elif '분' in timestamp:
        diff_time = current_time - relativedelta(minutes=int(numbers))
    elif '시간' in timestamp:
        diff_time = current_time - relativedelta(hours=int(numbers))
    elif '개월' in timestamp:
        diff_time = current_time - relativedelta(months=int(numbers))
    elif '년' in timestamp:
        diff_time = current_time - relativedelta(years=int(numbers))
    else:
        diff_time = current_time
    return diff_time.timestamp()


def get_links(url, file_path=None, wait_time=10):
    links = []
    with webdriver.Chrome(options=options) as driver:
        #크롬 드라이버에 url 주소 넣고 실행
        driver.get(url)
        element = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.ID, 'thumbnail')))

        # 링크 가져오기
        # thumbnails = driver.find_elements(By.ID, 'thumbnail')
        # links = [t.get_attribute('href') for t in thumbnails if t.get_attribute('href') is not None]

        # shorts 제외 video 링크만 가져오기
        # 게임의 경우 shorts가 리스트에 포함되어 있음
        videos = driver.find_elements(By.TAG_NAME, 'ytd-video-renderer')
        thumbnails = [v.find_element(By.ID, 'thumbnail') for v in videos]
        links = [t.get_attribute('href') for t in thumbnails if t.get_attribute('href') is not None and 'shorts' not in t.get_attribute('href')]
    if file_path is not None:
        save_as_file(file_path, links, overwrite=True)
    return links
    


def scroll_down(driver, scroll=2, scroll_wait_time=0.7):
    if not driver:
        return
    last_height = 0
    while 1:
        scroll -= 1
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(scroll_wait_time)
        now_height = driver.execute_script("return document.documentElement.scrollHeight")
        if now_height == last_height or scroll == 0:
            break
        last_height = now_height


def get_comments(url, file_path, scroll=2, wait_time = 30, scroll_wait_time=0.7):
    comments = []
    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        scroll_down(driver, scroll, scroll_wait_time)
        element = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.TAG_NAME, 'ytd-comment-renderer')))

        current_time = datetime.datetime.now()
        sections = driver.find_elements(By.TAG_NAME, 'ytd-comment-renderer')
        for section in sections:
            # TODO 예외 처리 추가 예정(selenium.common.exceptions.NoSuchElementException)
            author = section.find_element(By.ID, 'author-text')
            author = author.find_element(By.TAG_NAME, 'span')
            timestamp = section.find_element(By.CLASS_NAME, 'published-time-text')
            timestamp = timestamp.find_element(By.TAG_NAME, 'a')
            timestamp = get_timestamp(current_time, timestamp.text)
            comment = section.find_element(By.ID, 'content-text')
            comments.append({"author": author.text, "timestamp": timestamp, "comment": comment.text})
    if file_path is not None:
        save_as_file(file_path, comments)
    return comments


if __name__ == "__main__":
    for cat, path in categories.items():
        current_url = url.format(path)
        # 파일 저장 경로
        link_path = link_path_format.format(cat)
        comment_path = comment_path_format.format(cat)

        links = get_links(current_url, link_path)
        for link in links:
            get_comments(link, comment_path)

    """
    Test 코드
    특정 카테고리의 영상 n개의 댓글을 가져옴
    """
    # # 특정 카테고리만 가져옴
    # category = 'music'
    # # 영상 3개만 가져옴
    # n = 3

    # current_url = url.format(categories[category])
    # # 파일 저장 경로
    # link_path = link_path_format.format(category)
    # comment_path = comment_path_format.format(category)

    # links = get_links(current_url, link_path)
    # if len(links) > n:
    #     n = len(links)
    # for i in range(n):
    #     link = links[i]
    #     get_comments(link, comment_path)