'''
영상 별 댓글 수집해서 json으로 저장 할 내용 정리

video{
    category         : str   (영상분류)
    id (pk)          : int   (영상 고유키)
    title            : str   (제목)
    thumbnail        : str   (썸네일 url)
    count_of_views   : int   (조회수)
    comments         : list  (샘플댓글리스트)

    metadata{
        url              : str   (영상url)
        count_of_comment : int   (전체댓글수)
        scrap_count      : int   (샘플댓글수)
    }

    ...
    빈도수, 순서있는 댓글 몇개
}
'''

import json

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

def save_to_json(data={}, name="recestly_saved_file.json"):
    with open(name, "w") as f:
        json.dump(data, f)

def read_to_json(name=""):
    di = {}
    if name:
        with open(name, "r") as f:
            di = json.load(f)
    return di

if __name__ =="__main__":
    pass