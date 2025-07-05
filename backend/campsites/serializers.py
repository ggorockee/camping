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
