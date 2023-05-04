from .models import *
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import json
import glob

def load_json_to_model(json_file_path):
    """
    parameter : json 파일 경로(하나)
    type : str

    return : 삽입한 json데이터의 인스턴스
    type : Video
    """
    # JSON 파일을 Video 모델에 저장하는 과정
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)

    # JSON 데이터를 Video 인스턴스에 저장
    instance = Video(data=json_data)
    instance.save()
    return instance

def index(request):
    all_video = Video.objects.all()
    context = {'first_video': all_video[0].data}
    return render(request, 'comments/index.html', context)

def detail(request):
    all_video = Video.objects.all()
    context = {'first_video': all_video[0].data}
    return render(request, 'comments/detail.html', context)

def migrate(request):
    ## 수집한 json 데이터 전체를 읽어와서 모델에 삽입하는 과정
    data_arg = "comments\data"

    #glob을 이용하여 해당 폴더 내의 모든 json 파일의 경로를 읽어옵니다
    json_args = glob.glob(f"{data_arg}/*.json")

    #모델에 저장
    for json_file in json_args:
        sample_instance = load_json_to_model(json_file)
        # 일단은 하나만 저장하고 break
        # TO-DO
        # Video 모델의 중복성 검사 체크 추가하기
        print(json_file)
        break

    if sample_instance:
        # JSON 데이터를 클라이언트에 전송
        # ensure_ascii=False로 설정하여 한글을 그대로 출력
        json_data = json.dumps(sample_instance.data, ensure_ascii=False)

        return HttpResponse(json_data, content_type='application/json')
    else:
        # 인스턴스가 없을 경우, 404 Not Found 응답을 반환합니다.
        return JsonResponse({"error": "Not Found"}, status=404)