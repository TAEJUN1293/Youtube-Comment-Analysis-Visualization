from django.db import models
from django.core.exceptions import ValidationError

def validate_json_format(value):
    if not isinstance(value, dict):
        raise ValidationError("입력된 JSON 객체가 유효하지 않습니다.")
    
    required_keys = {"category", "id", "title", "thumbnail", "count_of_views", "comments", "metadata"}

    if not required_keys.issubset(value.keys()):
        raise ValidationError("필수 키가 누락되었습니다.")
    
    metadata_keys = {"url", "count_of_comment", "scrap_count"}

    if not metadata_keys.issubset(value['metadata'].keys()):
        raise ValidationError("metadata 필수 키가 누락되었습니다.")

    if not isinstance(value["category"], str):
        raise ValidationError("category는 문자열이어야 합니다.")
    
    if not isinstance(value["id"], int):
        raise ValidationError("id는 정수여야 합니다.")
    
    ## TO-DO
    ## 뒤쪽에 유효성 검사 모든 키값, 메타데이터 키값 관련해서 넣고 db 삭제한 뒤에 shell으로 샘플 데이터 몇개 만들어보기
    ## shell에서는 유효성 검사를 자동으로 실행시키지 않으니 주의
    ## .full_clean() 으로 유효성 검사 수동 실행 가능
    ## 테스트용


class Video(models.Model):
    data = models.JSONField(default=dict(), validators=[validate_json_format])
    class Meta:
        db_table = "videos"


