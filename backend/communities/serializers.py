from rest_framework import serializers
from . import models


class ReviewSerializer(serializers.ModelSerializer):

    # 리뷰를 작성한 사용자의 username을 보여주는 읽기 전용 필드
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = models.Review
        # API를 통해 보여줄 필드 목록
        fields = ["id", "user", "rating", "content", "created_at", "updated_at"]

        # 사용자가 직접 수정/입력할 수 없는 필드들
        # user와 campsite는 View에서 자동으로 설정.
        read_only_fields = ["user", "campsite"]
