# Youtube-Comment-Analysis-Visualization


프로그래머스-데이터엔지니어링 데브코스 프로젝트 

- 유튜브 카테고리별 댓글 키워드 유사도 분석 진행 및 데이터 시각화를 통해 인사이트를 도출하고 이를 활용한 웹 사이트 구축하기!

# json 포맷
https://docs.djangoproject.com/en/3.0/howto/initial-data/#providing-data-with-fixtures

# Python 가상환경 생성
py -m venv project-name
# 가상환경 활성화
project-name\Scripts\activate.bat
# 가상환경 비활성화
deactivate

# Django 설치
py -m pip install Django
# Pillow 설치
python -m pip install Pillow

# Django 버전 확인
django-admin --version
django-admin version

# Django 프로젝트 생성
python -m django startproject visualizationproject
python manage.py startapp {app_name}

# 데이터베이스 생성
python manage.py makemigrations {app_name}
python manage.py migrate {app_name}

# 유저 생성
python manage.py createsuperuser

# Django 실행
python manage.py runserver

# Django DB에 저장
python manage.py loaddata genre_data.json
python manage.py loaddata wordcloud/fixtures/category.json

# Django DB를 json 파일로 저장
python -Xutf8 manage.py dumpdata animations > fixtures.json