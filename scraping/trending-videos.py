import os
# selenium으로부터 webdriver 모듈을 불러옵니다.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
# Explicit Wait을 위해 추가
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 인기 급상승 url
url = 'https://www.youtube.com/feed/trending{}'
# 최신, 음악, 게임, 영화
categories = {
    'recent': '',
    'music': '?bp=4gINGgt5dG1hX2NoYXJ0cw%3D%3D',
    'game': '?bp=4gIcGhpnYW1pbmdfY29ycHVzX21vc3RfcG9wdWxhcg%3D%3D',
    'movie': '?bp=4gIKGgh0cmFpbGVycw%3D%3D'
}
# 링크 저장할 경로
link_path = '{}_link.txt'
# 기다리는 시간
wait_time = 10

for cat, path in categories.items():
    current_path = link_path.format(cat)
    current_url = url.format(path)
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        #크롬 드라이버에 url 주소 넣고 실행
        driver.get(current_url)
        element = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.ID, 'thumbnail')))

        # 링크 가져오기
        thumbnails = driver.find_elements(By.ID, 'thumbnail')
        links = [t.get_attribute('href') for t in thumbnails if t.get_attribute('href') is not None]

        # shorts 제외 video 링크만 가져오기
        # 게임의 경우 shorts가 리스트에 포함되어 있음
        # videos = driver.find_elements(By.TAG_NAME, 'ytd-video-renderer')
        # thumbnails = [v.find_element(By.ID, 'thumbnail') for v in videos]
        # links = [t.get_attribute('href') for t in thumbnails if t.get_attribute('href') is not None]

        # text 파일로 링크 저장
        mode = 'w' if os.path.exists(current_path) else 'a'
        with open(current_path, mode) as f:
            f.write('\n'.join(links))