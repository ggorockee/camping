from django.conf import settings
from rest_framework import serializers


from . import models


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Amenity
        fields = ("name", "icon_url")


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Policy
        # campsite 필드는 제외하고 나머지 정책 정보만 보여줌
        exclude = ("id", "campsite")


class CampsiteListSerializer(serializers.ModelSerializer):
    """캠핑장 목록을 위한 간단한 Serializer"""

    class Meta:
        model = models.Campsite
        fields = ("id", "name", "address", "phone_number")


class CampsiteDetailSerializer(serializers.ModelSerializer):
    """캠핑장 상세 정보를 위한 Serializer"""

    # owner의 username 필드를 읽기 전용으로 보여줌
    owner = serializers.ReadOnlyField(source="owner.username")

    # 1:1 관계인 policy는 중첩 Serializer로 보여줌
    policy = PolicySerializer(read_only=True)

    # M2M 관계인 amenities도 중첩 Serializer로 보여줌
    amenities = AmenitySerializer(many=True, read_only=True, source="amenity_set")

    class Meta:
        model = models.Campsite
        fields = "__all__"


class CampsiteImageSerializer(serializers.ModelSerializer):
    # 응답에 포함될, 동적으로 생성되는 전체 이미지 URL 필드
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = models.CampsiteImage
        # API를 통해 보여줄 필드 목록
        fields = ("id", "cloudflare_id", "image_url", "order")
        # 클라이언트로부터 직접 입력받는 필드
        extra_kwargs = {"cloudflare_id": {"write_only": True}}

    def get_image_url(self, obj):
        """
        Cloudflare ID와 variant 이름을 조합하여 전체 이미지 URL을 생성
        'public'은 기본 variant 이름입니다. 필요에 따라 변경할 수 있음.
        """
        # 이 부분은 Cloudflare 대시보드의 'Images' > 'Variants'에서 확인 가능
        variant = "public"
        return f"https://imagedelivery.net/{settings.CLOUDFLARE_ACCOUNT_HASH}/{obj.cloudflare_id}/{variant}"
