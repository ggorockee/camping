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

    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Campsite
        fields = (
            "id",
            "name",
            "address",
            "phone_number",
            "created_at",
            "description",
            "thumbnail_url",
        )

    def get_thumbnail_url(self, obj):
        """캠핑장의 첫 번째 이미지 URL을 return"""
        # obj는 Campsite 인스턴스.
        # related_name='images'를 통해 캠핑장에 연결된 이미지들을 가져옴.
        # ordering = ["order"]에 의해 정렬되어 있으므로 .first()는 대표 이미지가 됩니다.
        first_image = obj.images.first()

        # 이미지가 없는 경우 null을 반환합니다.
        if not first_image:
            return None

        # CampsiteImageSerializer의 URL 생성 로직을 활용.
        # 성능을 위해 목록 보기용 썸네일 variant를 사용하는 것이 좋습니다. (예: "thumbnail")
        variant = "public"  # 필요에 따라 "thumbnail" 등 작은 variant로 변경
        return f"https://imagedelivery.net/{settings.CLOUDFLARE_ACCOUNT_HASH}/{first_image.cloudflare_id}/{variant}"


class CampsiteImageSerializer(serializers.ModelSerializer):
    # 응답에 포함될, 동적으로 생성되는 전체 이미지 URL 필드
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = models.CampsiteImage
        # API를 통해 보여줄 필드 목록
        # fields = ("id", "cloudflare_id", "image_url", "order")
        # 클라이언트로부터 직접 입력받는 필드
        # extra_kwargs = {"cloudflare_id": {"write_only": True}}
        fields = ("cloudflare_id", "order", "image_url")

    def get_image_url(self, obj):
        """
        Cloudflare ID와 variant 이름을 조합하여 전체 이미지 URL을 생성
        'public'은 기본 variant 이름. 필요에 따라 변경할 수 있음.
        """
        # 이 부분은 Cloudflare 대시보드의 'Images' > 'Variants'에서 확인 가능
        variant = "public"
        return f"https://imagedelivery.net/{settings.CLOUDFLARE_ACCOUNT_HASH}/{obj.cloudflare_id}/{variant}"


class CampsiteCreateSerializer(serializers.ModelSerializer):
    image_ids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        help_text="Cloudflare 이미지 ID 목록 (최소 3개 이상)",
    )

    class Meta:
        model = models.Campsite
        fields = ("name", "description", "image_ids")

    def validate_image_ids(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("최소 3장 이상의 사진 ID가 필요해요~")
        return value

    def create(self, validated_data):
        # 프론트에서 받은 'image_ids' 목록을 가져옴
        image_ids_list = validated_data.pop("image_ids")

        campsite = models.Campsite.objects.create(**validated_data)

        images_to_create = [
            models.CampsiteImage(
                campsite=campsite,
                # ⭐️ 핵심: 리스트의 각 ID를 cloudflare_id 필드에 할당
                cloudflare_id=image_id,
                order=index,
            )
            for index, image_id in enumerate(image_ids_list)
        ]
        models.CampsiteImage.objects.bulk_create(images_to_create)

        return campsite


class CampsiteDetailSerializer(serializers.ModelSerializer):
    """캠핑장 상세 정보를 위한 Serializer"""

    # owner의 username 필드를 읽기 전용으로 보여줌
    owner = serializers.ReadOnlyField(source="owner.username")

    # 1:1 관계인 policy는 중첩 Serializer로 보여줌
    policy = PolicySerializer(read_only=True)

    # M2M 관계인 amenities도 중첩 Serializer로 보여줌
    amenities = AmenitySerializer(
        many=True,
        read_only=True,
        source="amenity_set",
    )

    images = CampsiteImageSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = models.Campsite
        fields = "__all__"
