
### json파일구성
```
def for_dictionary(category="", id=0, title="", img_url="", comments=[], \
                    frequency={},comments_all=[], \
                    url="", count_of_view=0, count_of_comment=0,\
                    scrap_count=0,):
    d = json.dumps({
        'category':category,
        'id':id,
        'title':title,
        'img_url':img_url,
        'comments':comments,
        'comments_all':comments_all,
        'frequency':frequency,
        'metadata':{
            'url':url,
            'count_of_view':count_of_view,
            'count_of_comment':count_of_comment,
            'scrap_count':scrap_count,
        }
    })
    return d
```

### sub
1. Youtube_URL_Crawling.py
    - 태준님_인기급상습에서 각 부분 URL스크랩해오는 기능
    - 최신(recent), 음악(music) 부분 진행위해 해당부분만 가져옴
    - 수집내용
        - 영상url, 이미지url
2. commentary_json_format.py
    - json파일로 열고 저장하는 용도,
    - 전체 데이터 포맷 dictionary로 맞추는 용도
3. replyscrapper.py
    - url주소 주면 주 데이터 스크랩하는 클래스 Commentary() 정의
    - 수집내용
        - 제목
        - 조회수
        - 샘플댓글리스트
        - 전체댓글수
        - 샘플링한댓글수
        - 일부댓글
        - 일부댓글수
    - (일부댓글은 유실되는 데이터때문에 댓글표시용과 분석용 2개를 수집하기위함)
### main.py
먼저 sub1이용해서 전체 url목록 urls.json으로 저장.<br>
-> 파일 존재 시 스킵

이후 드라이버 세팅 후
카테고리별로 모든 url마다 콘텐츠데이터 수집하여
```<<JSON_FILE_NAME>>```으로 저장.<br>
-> url개수만큼 파일 생성.
