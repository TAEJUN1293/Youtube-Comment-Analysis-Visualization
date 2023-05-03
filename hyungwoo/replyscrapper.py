from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from collections import Counter
from konlpy.tag import Hannanum

def window_size_to_thin(driver):
    driver.maximize_window()
    driver.set_window_size("700", driver.get_window_size()["height"])

'''
    category         : str   (영상분류)
    id (pk)          : int   (영상 고유키)
   *title            : str   (제목)
    thumbnail        : str   (썸네일 url)
   *count_of_views   : int   (조회수)
   *comments         : list  (샘플댓글리스트)

    metadata{
        url              : str   (영상url)
       *count_of_comment : int   (전체댓글수)
       *scrap_count      : int   (샘플댓글수)
 '''

class Commentary():
    '''
    title            : str   (제목)
        -> .title
    count_of_views   : int   (조회수)
        -> .count_of_view
    comments         : list  (샘플댓글리스트)
        -> .comments
    count_of_comment : int   (전체댓글수)
        -> .count_of_comment
    scrap_count      : int   (샘플댓글수)
        -> .count_of_crawled

    위 thin함수 실행 후 (좌우얇은브라우저)
    driver와 url 주고 Commentary호출하면 끝.
    '''
    def __init__(self, driver, url="", scroll=3, scroll_time=0.7):
        '''
        드라이버 받아서 각 요소 생성하고,
        드라이버 소유권포기.
        :param driver:
        :param url:
        :param scroll: 총 스크롤 횟수
        :param scroll_time: 스크롤 사이 시간간격
        '''
        # scroll_once 후 대기시간 (second)
        self.SCROLL_WAIT_TIME = scroll_time
        # scroll_once 실행 횟수
        self.MAX_SCROLL_TIME = scroll

        # konlpy쓰고 출력문 정할 때 필요했던것
        # self.MOST = most

        self.driver = driver
        self.url = url
        self.title = ""
        self.count_of_view = 0
        self.comments = []
        self.count_of_comment = 0
        self.count_of_crawled = 0

        if url:
            self.driver.get(self.url)
            time.sleep(3)
            self.title = self.driver.find_element(By.XPATH, '//*[@id="title"]/h1').text
            self.count_of_view = self.get_count_of_views()
            self.scroll_once()
            time.sleep(3)
            if driver.find_elements(By.XPATH,'//*[@id="message"]')!=[]:
                self.count_of_comment = self.get_count_of_comments()

                print("get_comments..", end=" ")
                print(self.count_of_comment)
                try:
                    elements = self.get_elements()
                    self.comments = self.elements_to_comments(elements)
                except Exception as e:
                    print("Error:",e)

                self.count_of_crawled = len(self.comments)
                # print("get_frequency..", end=" ")
                # self.comment_frequency = self.get_frequency_for_comments()
            else:
                self.comments = ["댓글이 사용 중지되었습니다."]
        self.driver = None

    def __str__(self):
        if self.url=="":
            return None
        title = self.title
        views = self.count_of_view
        count_of_comment = self.count_of_comment
        crawled = self.count_of_crawled
        comments = self.comments[:5]

        return "{} 조회수 ({}), 댓글수 ({}), 샘플링수 ({}):\ncomments:\n{}"\
                .format(title, views, count_of_comment, crawled, "\n".join(comments))

    # konlpy까지 할 경우
    # def __str__(self):
    #     if self.url=="":
    #         return None
    #     title = self.title
    #     comments = self.count_of_comment_all
    #     views = self.count_of_view
    #     count = self.count_of_comment
    #     top_comments = self.comments[:3]
    #     # most_nouns = self.top_n(self.MOST)
    #     return "{} 조회수 ({}), 댓글 수 ({}), 수집한 댓글 ({}),:\ncomments:\n{}\nmost {} nouns:\n{}"\
    #         .format(title, views, comments, count, top_comments, self.MOST, most_nouns)

    # konlpy까지 할 경우
    # def is_instance(self):
    #     return (self.title!="" and self.url!="" and len(self.comments)!=0)

    # konlpy까지 할 경우
    # def top_n(self, n):
    #     if not self.is_instance():
    #         return None
    #     return self.comment_frequency.most_common(n)

    def deo_bogi(self):
        '''
        페이지 로드 후 더보기 버튼 누름
        -> 눌러야 조회수 잘보임..
        :return:
        '''
        button = self.driver.find_element(By.XPATH,'//*[@id="snippet"]')
        ActionChains(self.driver).click(button).perform()
        time.sleep(0.1)

    def get_count_of_views(self):
        '''
        조회수 따오기
        :return:
        '''
        self.deo_bogi()
        tmp = self.driver.find_element(By.XPATH,'//*[@id="info"]/span[1]').text
        views = tmp.split()[1][:-1].replace(",","")
        return int(views)

    def get_count_of_comments(self):
        '''
        전체 댓글 수 가져오기
        페이지 한번 내리고나서 할 것
        :return: 
        '''
        tmp = self.driver.find_element(By.XPATH,'//*[@id="count"]/yt-formatted-string/span[2]').text
        tmp = tmp.replace(",", "")
        return int(tmp)

    # konlpy까지 할 경우
    # def get_frequency_for_comments(self):
    #     if not self.is_instance():
    #         return None
    #     hannanum = Hannanum()
    #     print(len(self.comments))
    #     nouns_all = []
    #     for comment in self.comments:
    #         nouns = hannanum.nouns(comment)
    #         nouns_all.extend([noun for noun in nouns if (len(noun)>1 and "ㅋㅋ"not in noun and "ㅎㅎ"not in noun)])
    #     return Counter(nouns_all)

    def scroll_once(self):
        '''
        스크롤 한번 밑으로 내리기
        :return: 
        '''
        # 바닥까지 스크롤링 방법 두개
        self.driver.find_element(By.TAG_NAME, "body").send_keys("\ue010")
        # self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(self.SCROLL_WAIT_TIME)

    # def scroll_down(self):
    #     '''
    #     self.MAX_SCROLL_TIME 횟수대로 페이지 내림
    #     대기시간 self.SCROLL_WAIT_TIME
    #     0이면 바닥까지
    #     :return:
    #     '''
    #     if not self.driver:
    #         return
    #
    #     scrolling = self.MAX_SCROLL_TIME
    #     last_height = 0
    #     while 1:
    #         scrolling -= 1
    #         self.scroll_once()
    #         now_height = self.driver.execute_script("return document.documentElement.scrollHeight")
    #         if now_height == last_height or scrolling==0:
    #             break
    #         last_height = now_height

    def preprocess_comment_elements(self,elements):
        '''
        element상태의 댓글내용 가져와서
        .text 전환 후
        전처리해서 다시 리턴
        '''
        comments = []
        for element in elements:
            comment = element.text
            comment = comment \
                .replace("𝐏𝐥𝐚𝐲𝐥𝐢𝐬𝐭", "playlist") \
                .replace("\n", " ") \
                .replace("\t", " ") \
                .strip()
            comments.append(comment)
        return comments

    def get_elements(self):
        '''
        self.url 에서 댓글"만" 긁어오기
        comments:list
        '''
        if not self.driver:
            return

        scrolling = self.MAX_SCROLL_TIME
        last_height = 0
        # elements = []
        while 1:
            scrolling -= 1
            self.scroll_once()
            # element = self.driver.find_elements(By.ID, "content-text")
            # print(len(element))
            # elements.append(element)
            now_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            if now_height == last_height or scrolling==0:
                break
            last_height = now_height
        # 위 주석 4개 풀면 스크롤당, 얘는 한번에
        elements = [self.driver.find_elements(By.ID, "content-text")]
        return elements

    def elements_to_comments(self, elements):
        '''
        위 스크랩부분을 스크롤당으로 하면 분리하기위한 메서드
        '''
        comments = []
        for element in elements:
            comments.extend(self.preprocess_comment_elements(element))
        return comments