from django.utils import timezone
from django.db import models
from django.core import exceptions
from django.conf import settings
from common.models import BaseModel


class Campsite(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="campsites",
    )
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    description = models.TextField()

    price = models.PositiveIntegerField(
        help_text="총 숙박 요금 (단위: 원)",
    )

    contact_number = models.CharField(
        max_length=20,
        blank=True,
        help_text="대표 번호",
    )

    # 1) 체크인/체크아웃 날짜
    check_in = models.DateField()
    check_out = models.DateField()

    layout_image_url = models.URLField(blank=True)  # 사이트 배치도 이미지

    def __str__(self):
        return self.name  # 캠핑장 이름으로 표시

    @property
    def stay_nights(self):
        if self.check_in and self.check_out:
            return (self.check_out - self.check_in).days
        return None

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        super().clean()
        today = timezone.localdate()

        # 1) check_in < check_out
        if self.check_in and self.check_out:
            if self.check_in >= self.check_out:
                raise exceptions.ValidationError(
                    {
                        "check_in": "체크인 날짜는 체크아웃 날짜보다 이전이어야 합니다.",
                        "check_out": "체크아웃 날짜는 체크인 날짜보다 이후이어야 합니다.",
                    }
                )

        # 2) check_in, check_out 모두 오늘 이전이어야 함
        if self.check_in and self.check_in >= today:
            raise exceptions.ValidationError(
                {"check_in": "체크인 날짜는 오늘 이전이어야 합니다."}
            )
        if self.check_out and self.check_out >= today:
            raise exceptions.ValidationError(
                {"check_out": "체크아웃 날짜는 오늘 이전이어야 합니다."}
            )


class CampsiteImage(BaseModel):
    campsite = models.ForeignKey(
        Campsite, on_delete=models.CASCADE, related_name="images"
    )
    cloudflare_id = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.campsite.name} - Image (Order: {self.order})"  # "캠핑장 이름 - 이미지 (순서: 0)" 형식으로 표시


class Site(BaseModel):
    campsite = models.ForeignKey(
        Campsite, on_delete=models.CASCADE, related_name="sites"
    )
    name = models.CharField(max_length=50)  # 예: A1, B5
    camp_type = models.CharField(max_length=50)  # 예: 오토캠핑, 글램핑
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.campsite.name} - {self.name}"  # "캠핑장 이름 - 사이트 이름" 형식으로 표시


class Amenity(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    icon_url = models.URLField(blank=True)

    def __str__(self):
        return self.name  # 편의시설 이름으로 표시


class CampsiteAmenity(BaseModel):
    campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.campsite.name} has {self.amenity.name}"  # "캠핑장 이름 has 편의시설 이름" 형식으로 표시


class Policy(BaseModel):
    campsite = models.OneToOneField(
        Campsite, on_delete=models.CASCADE, related_name="policy"
    )
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    manner_time_start = models.TimeField()
    manner_time_end = models.TimeField()

    def __str__(self):
        return (
            f"Policy for {self.campsite.name}"  # "Policy for 캠핑장 이름" 형식으로 표시
        )


class PricingRule(BaseModel):
    campsite = models.ForeignKey(
        Campsite, on_delete=models.CASCADE, related_name="pricing_rules"
    )
    name = models.CharField(max_length=100)  # 예: 주말/성수기 요금
    start_date = models.DateField()
    end_date = models.DateField()
    day_of_week = models.CharField(
        max_length=15, blank=True, help_text="쉼표로 구분된 요일(0-6)"
    )
    extra_charge = models.DecimalField(max_digits=10, decimal_places=2)  # 추가 요금

    def __str__(self):
        return f"{self.campsite.name} - {self.name}"  # "캠핑장 이름 - 요금 규칙 이름" 형식으로 표시
