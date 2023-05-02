from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from collections import Counter
from konlpy.tag import Hannanum

# id="overlays"
# ytd-thumbnail-overlay-time-status-renderer
# class="style-scope ytd-thumbnail"
# overlay-style="DEFAULT" / "SHORTS"

def window_size_to_thin(driver):
    driver.maximize_window()
    driver.set_window_size("700", driver.get_window_size()["height"])


class Commentary():
    def __init__(self, driver, url="", scroll=2, scroll_time=0.7, file_name="", most=10):
        '''

        :param url:
        open to (url) and
        :param scroll:
        '''
        self.SCROLL_WAIT_TIME = scroll_time
        self.MAX_SCROLL_TIME = scroll
        self.MOST = most

        self.driver = driver
        self.url = url
        self.comments = []
        self.count_of_comment = 0
        self.count_of_comment_all = 0
        self.count_of_view = 0

        if file_name:
            self.NAME_OF_CSV = file_name+".csv"
        else:
            self.NAME_OF_CSV = "csv_tmp_name.csv"

        if url:
            print("get_comments..", end=" ")
            self.title, self.comments = self.get_title_and_comments()
            self.count_of_comment = len(self.comments)
            print("get_frequency..", end=" ")
            self.comment_frequency = self.get_frequency_for_comments()
            self.driver = None

    def __str__(self):
        if self.url=="":
            return None
        title = self.title
        comments = self.count_of_comment_all
        views = self.count_of_view
        count = self.count_of_comment
        top_comments = self.comments[:3]
        most_nouns = self.top_n(self.MOST)
        return "{} 조회수 ({}), 댓글 수 ({}), 수집한 댓글 ({}),:\ncomments:\n{}\nmost {} nouns:\n{}"\
            .format(title, views, comments, count, top_comments, self.MOST, most_nouns)

    def is_instance(self):
        return (self.title!="" and self.url!="" and len(self.comments)!=0)

    def top_n(self, n):
        if not self.is_instance():
            return None
        return self.comment_frequency.most_common(n)

    def deo_bogi(self):
        button = self.driver.find_element(By.XPATH,'//*[@id="snippet"]')
        ActionChains(self.driver).click(button).perform()
        time.sleep(0.1)

    def get_count_of_views(self):
        self.deo_bogi()
        tmp = self.driver.find_element(By.XPATH,'//*[@id="info"]/span[1]').text
        views = tmp.split()[1][:-1].replace(",","")
        return views

    def get_count_of_comments(self):
        return self.driver.find_element(By.XPATH,'//*[@id="count"]/yt-formatted-string/span[2]').text

    def get_frequency_for_comments(self):
        if not self.is_instance():
            return None
        hannanum = Hannanum()
        print(len(self.comments))
        nouns_all = []
        for comment in self.comments:
            nouns = hannanum.nouns(comment)
            # nouns_all.extend(nouns)
            nouns_all.extend([noun for noun in nouns if (len(noun)>1 and "ㅋㅋ"not in noun and "ㅎㅎ"not in noun)])
        return Counter(nouns_all)

    def scroll_down(self, scroll=None):
        '''
        self.MAX_SCROLL_TIME 횟수대로 페이지 내림
        대기시간 self.SCROLL_WAIT_TIME
        0이면 바닥까지
        :return: 
        '''
        if not self.driver:
            return
        # last_height = driver.execute_script("return document.documentElement.scrollHeight")
        if scroll:
            scrolling = scroll
        else:
            scrolling = self.MAX_SCROLL_TIME
        last_height = 0
        while 1:
            scrolling -= 1
            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(self.SCROLL_WAIT_TIME)
            now_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            if now_height == last_height or scrolling==0:
                break
            last_height = now_height
        # for _ in range(self.MAX_SCROLL_TIME):
        #     self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        #     # ActionChains(self.driver).key_down("\ue010").perform()
        #     # self.driver.find_element_by_tag_name('body').send_keys("\ue010")
        #     time.sleep(self.SCROLL_WAIT_TIME)
        #     # self.driver.implicitly_wait(SCROLL_WAIT_TIME)

    def get_title_and_comments(self):
        '''
        self.url 에서 댓글 긁어오기
        title:str, comments:list
        '''

        self.driver.get(self.url)
        time.sleep(3)

        title = self.driver.find_element(By.XPATH, '//*[@id="title"]/h1').text
        self.count_of_view = self.get_count_of_views()
        self.scroll_down(scroll=1)
        self.count_of_comment_all = self.get_count_of_comments()
        print(self.count_of_comment_all)

        self.scroll_down()

        comment_elements = self.driver.find_elements(By.ID, "content-text")

        comments = []
        for comment in comment_elements:
            comment_str = comment.text

            comment_str = comment_str\
                .replace("𝐏𝐥𝐚𝐲𝐥𝐢𝐬𝐭","playlist")\
                .replace("\n"," ")\
                .replace("\t"," ")\
                .strip()

            comments.append(comment_str)

        return (title, comments)

    def save_to_csv(self):
        '''
        몰라 이상함
        :param contents: 
        :return: 
        '''
        if not self.is_instance():
            return None

        new_dict = {}
        max_length = max([len(i["comments"]) for i in self.contents])
        for content in self.contents:
            l = len(content["comments"])
            new_dict[content["title"]] = content["comments"]+[""]*(max_length-l)
        df = pd.DataFrame(new_dict)
        df.to_csv(self.NAME_OF_CSV, header=True, index=True, encoding="utf-16 le")
